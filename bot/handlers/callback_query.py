import sys
import traceback

from django.db.models import Count, Q
from telebot import types, TeleBot
from telebot.apihelper import ApiException

from actions.models import SearchQuery, Subscription
from bot.utils import keyboards, helpers
from classifiers.models import Text, Category
from configurations.constants import CALLBACK, ERROR
from basics.models import User, Error
from contents.models import Episode, Podcast, Collection, Channel


def initializer_callback_query_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda query: True)
    def callback_query_handler(query: types.CallbackQuery):

        def select_the_text(user: User, query: types.CallbackQuery, message: types.Message, text_id: int):
            try:
                text = Text.objects.get(id=text_id)
                is_new_user = True if not user.text else False
                user.text = text
                user.save()
                bot.delete_message(
                    message.chat.id,
                    message.message_id,
                )
                if is_new_user:
                    bot.send_message(
                        message.chat.id,
                        text.hello_text.format(
                            full_name=user.full_name,
                        ),
                        reply_markup=keyboards.reply_keyboard_remove,
                    )
                bot.send_message(
                    message.chat.id,
                    user.text.main_text.format(
                        commands='\n'.join([
                            f"/{command.key} - {command.description}" for command in
                            helpers.get_available_commands(user)
                        ])
                    ),
                    reply_markup=keyboards.reply_keyboard_remove,
                )
                if is_new_user:
                    bot.send_message(
                        message.chat.id,
                        user.text.selecting_interested_categories,
                        reply_markup=keyboards.get_interested_categories_inline_keyboard(
                            user,
                            list(user.interested_categories.values_list('id', flat=True)),
                        ),
                    )
                helpers.reset_commands(bot, user)
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    "🤷🏻‍♂️",
                )

        def change_the_category_interested_state(user: User, query: types.CallbackQuery, message: types.Message, category_id: int):
            try:
                category = Category.objects.get(id=category_id)
                interested_categories = list(user.interested_categories.values_list('id', flat=True))
                if category_id in interested_categories:
                    user.interested_categories.remove(category)
                    interested_categories.remove(category_id)
                else:
                    user.interested_categories.add(category_id)
                    interested_categories.append(category_id)
                bot.edit_message_reply_markup(
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_interested_categories_inline_keyboard(user, interested_categories),
                )
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    "🤷🏻‍♂️",
                )

        def select_top_episodes_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            episodes = Episode.objects.filter(is_active=True).annotate(
                matched_interested_categories_count=Count(
                    'podcast__categories',
                    filter=Q(podcast__categories__in=user.interested_categories.all()),
                    distinct=True,
                ),
            ).order_by('-matched_interested_categories_count', '-total_listens_count', '-total_likes_count', '-id')
            total = episodes.count()
            if total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            elif page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.top_text.format(
                        total=total,
                        start=start,
                        end=end,
                        episodes='\n'.join([
                            f"{sequence}. {episode.name} <b>(<i>{episode.total_listens_count:,} 📥</i>)</b>"
                            for sequence, episode in enumerate(episodes[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_top_episodes_inline_keyboard(user, episodes, start, end, page),
                )

        def select_newest_episodes_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            episodes = Episode.objects.filter(is_active=True).order_by('-added_time')
            total = episodes.count()
            if total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            elif page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.newest_text.format(
                        total=total,
                        start=start,
                        end=end,
                        episodes='\n'.join([
                            f"{sequence}. {episode.name} <b>(<i>{episode.total_listens_count:,} 📥</i>)</b>"
                            for sequence, episode in enumerate(episodes[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_newest_episodes_inline_keyboard(user, episodes, start, end, page),
                )

        def select_subscriptions_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            subscriptions = user.subscriptions.filter(podcast__is_active=True)
            total = subscriptions.count()
            if total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            elif page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.subscriptions_text.format(
                        total=total,
                        start=start,
                        end=end,
                        subscriptions='\n'.join([
                            f"{sequence}. {subscription.podcast.name}"
                            for sequence, subscription in enumerate(subscriptions[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_subscriptions_inline_keyboard(user, subscriptions, start, end, page),
                )

        def select_collections_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            collections = Collection.objects.filter(is_active=True)
            total = collections.count()
            if page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            elif total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.collections_text.format(
                        start=start,
                        end=end,
                        total=total,
                        collections='\n'.join([
                            f"{sequence}. {collection.name}"
                            for sequence, collection in enumerate(collections[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_collections_inline_keyboard(user, collections, start, end, page),
                )

        def select_the_collection(user: User, query: types.CallbackQuery, message: types.Message, collection_id: int):
            try:
                collection = Collection.objects.get(id=collection_id, is_active=True)
                podcasts = collection.podcasts.filter(is_active=True)
                total = podcasts.count()
                start = 1
                end = 10 if total > 10 else total
                bot.send_message(
                    message.chat.id,
                    user.text.the_collection_text.format(
                        image='',
                        name=collection.name,
                        podcasts='\n'.join([
                            f"{sequence}. {podcast.name}" for sequence, podcast in enumerate(podcasts[start - 1:end], 1)
                        ])
                    ),
                    reply_markup=keyboards.get_the_collection_podcasts_inline_keyboard(user, collection, start, end),
                    link_preview_options=helpers.link_preview_options,
                )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.collection_not_found,
                )

        def select_the_collection_podcasts_page(user: User, query: types.CallbackQuery, message: types.Message, collection_id: int, page: int):
            try:
                collection = Collection.objects.get(id=collection_id)
                podcasts = collection.podcasts.filter(is_active=True)
                total = podcasts.count()
                if page < 1:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_first_page,
                    )
                elif total <= (page - 1) * 10:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_last_page,
                    )
                else:
                    start = (page - 1) * 10 + 1
                    end = page * 10 if total > page * 10 else total
                    bot.edit_message_text(
                        user.text.the_collection_text.format(
                            image='',
                            name=collection.name,
                            podcasts='\n'.join([
                                f"{sequence}. {podcast.name}"
                                for sequence, podcast in enumerate(podcasts[start - 1:end], 1)
                            ])
                        ),
                        message.chat.id,
                        message.message_id,
                        reply_markup=keyboards.get_the_collection_podcasts_inline_keyboard(
                            user,
                            collection,
                            start,
                            end,
                            page,
                        ),
                        link_preview_options=helpers.link_preview_options,
                    )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.collection_not_found,
                )

        def select_channels_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            channels = Channel.objects.filter(is_active=True)
            total = channels.count()
            if page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            elif total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.channels_text.format(
                        start=start,
                        end=end,
                        total=total,
                        channels='\n'.join([
                            f"{sequence}. {channel.name}"
                            for sequence, channel in enumerate(channels[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_channels_inline_keyboard(user, channels, start, end, page),
                )

        def select_the_channel(user: User, query: types.CallbackQuery, message: types.Message, channel_id: int):
            try:
                channel = Channel.objects.get(id=channel_id, is_active=True)
                podcasts = channel.podcasts.filter(is_active=True)
                total = podcasts.count()
                start = 1
                end = 10 if total > 10 else total
                bot.send_message(
                    message.chat.id,
                    user.text.the_channel_text.format(
                        image='',
                        name=channel.name,
                        podcasts='\n'.join([
                            f"{sequence}. {podcast.name}" for sequence, podcast in enumerate(podcasts[start - 1:end], 1)
                        ])
                    ),
                    reply_markup=keyboards.get_the_channel_podcasts_inline_keyboard(user, channel, start, end),
                    link_preview_options=helpers.link_preview_options,
                )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.channel_not_found,
                )

        def select_the_channel_podcasts_page(user: User, query: types.CallbackQuery, message: types.Message, channel_id: int, page: int):
            try:
                channel = Channel.objects.get(id=channel_id)
                podcasts = channel.podcasts.filter(is_active=True)
                total = podcasts.count()
                if page < 1:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_first_page,
                    )
                elif total <= (page - 1) * 10:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_last_page,
                    )
                else:
                    start = (page - 1) * 10 + 1
                    end = page * 10 if total > page * 10 else total
                    bot.edit_message_text(
                        user.text.the_channel_text.format(
                            image='',
                            name=channel.name,
                            podcasts='\n'.join([
                                f"{sequence}. {podcast.name}"
                                for sequence, podcast in enumerate(podcasts[start - 1:end], 1)
                            ])
                        ),
                        message.chat.id,
                        message.message_id,
                        reply_markup=keyboards.get_the_channel_podcasts_inline_keyboard(user, channel, start, end, page),
                        link_preview_options=helpers.link_preview_options,
                    )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.channel_not_found,
                )

        def select_podcasts_page(user: User, query: types.CallbackQuery, message: types.Message, page: int):
            podcasts = Podcast.objects.filter(is_active=True).annotate(
                matched_interested_categories_count=Count(
                    'categories',
                    filter=Q(categories__in=user.interested_categories.all()),
                    distinct=True,
                ),
            ).order_by('-matched_interested_categories_count')
            total = podcasts.count()
            if page < 1:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_first_page,
                )
            elif total <= (page - 1) * 10:
                bot.answer_callback_query(
                    query.id,
                    user.text.you_already_in_the_last_page,
                )
            else:
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_text(
                    user.text.podcasts_text.format(
                        start=start,
                        end=end,
                        total=total,
                        podcasts='\n'.join([
                            f"{sequence}. {podcast.name}"
                            for sequence, podcast in enumerate(podcasts[start - 1:end], 1)
                        ])
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_podcasts_inline_keyboard(user, podcasts, start, end, page),
                )

        def select_the_podcast(user: User, query: types.CallbackQuery, message: types.Message, podcast_id: int):
            try:
                podcast = Podcast.objects.get(id=podcast_id, is_active=True)
                subscription = user.subscriptions.filter(podcast=podcast).first()
                episodes = podcast.episodes.filter(is_active=True).order_by('-id')
                total = episodes.count()
                start = 1
                end = 10 if total > 10 else total
                bot.send_message(
                    message.chat.id,
                    user.text.the_podcast_text.format(
                        image='',
                        name=podcast.name,
                        channel=podcast.channel.name,
                        description=f"\n\n{podcast.description}" if podcast.description else '',
                        start=start,
                        end=end,
                        total=total,
                        episodes='\n'.join([
                            f"{sequence}. {episode.name} <b>(<i>{episode.total_listens_count:,} 📥</i>)</b>"
                            for sequence, episode in enumerate(episodes[start - 1:end], 1)
                        ])
                    ),
                    reply_markup=keyboards.get_the_podcast_episodes_inline_keyboard(
                        user,
                        podcast,
                        subscription,
                        total,
                        start,
                        end,
                    ),
                    link_preview_options=types.LinkPreviewOptions(
                        prefer_large_media=True,
                        show_above_text=True,
                    )
                )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.podcast_not_found,
                )

        def change_the_podcast_subscription_state(user: User, query: types.CallbackQuery, message: types.Message, podcast_id: int, total: int, page: int):
            try:
                podcast = Podcast.objects.get(id=podcast_id)
                subscription, added = user.subscriptions.get_or_create(podcast=podcast)
                if not added:
                    subscription.delete()
                    subscription = None
                start = (page - 1) * 10 + 1
                end = page * 10 if total > page * 10 else total
                bot.edit_message_reply_markup(
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_the_podcast_episodes_inline_keyboard(user, podcast, subscription, total, start, end, page),
                )
                bot.answer_callback_query(
                    query.id,
                    user.text.you_have_subscribed if subscription else user.text.you_have_unsubscribed,
                )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.podcast_not_found,
                )

        def change_the_podcast_subscription_notification_state(user: User, query: types.CallbackQuery, message: types.Message, podcast_id: int, total: int, page: int):
            try:
                podcast = Podcast.objects.get(id=podcast_id)
                try:
                    subscription = user.subscriptions.get(podcast=podcast)
                    subscription.is_notification_enabled = not subscription.is_notification_enabled
                    subscription.save()
                    start = (page - 1) * 10 + 1
                    end = page * 10 if total > page * 10 else total
                    bot.edit_message_reply_markup(
                        message.chat.id,
                        message.message_id,
                        reply_markup=keyboards.get_the_podcast_episodes_inline_keyboard(user, podcast, subscription, total, start, end, page),
                    )
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_have_enabled_notification if subscription.is_notification_enabled else user.text.you_have_disabled_notification,
                    )
                except Subscription.DoesNotExist:
                    bot.answer_callback_query(
                        query.id,
                        user.text.podcast_not_found,
                    )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.podcast_not_found,
                )

        def download_all_episodes_of_the_podcast(user: User, query: types.CallbackQuery, message: types.Message, podcast_id: int):
            try:
                podcast = Podcast.objects.get(id=podcast_id)
                episodes = podcast.episodes.filter(is_active=True).order_by('-added_time')
                if episodes.count() > 1:
                    medias = []
                    for episode in episodes:
                        medias.append(
                            types.InputMediaAudio(
                                episode.file_id,
                                duration=episode.duration,
                                performer=episode.podcast.channel.name,
                                title=episode.name,
                            )
                        )
                        episode.total_listens_count += 1
                        episode.save()
                    medias = [medias[i * 10:(i + 1) * 10] for i in range((len(medias) + 10 - 1) // 10)]
                    for media in medias:
                        bot.send_media_group(
                            message.chat.id,
                            media,
                        )
                elif episodes.count() == 1:
                    select_the_episode(user, query, message, episodes.first().id)
                else:
                    bot.answer_callback_query(
                        query.id,
                        user.text.episode_not_found,
                    )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.podcast_not_found,
                )

        def select_the_podcast_episodes_page(user: User, query: types.CallbackQuery, message: types.Message, podcast_id: int, page: int):
            try:
                podcast = Podcast.objects.get(id=podcast_id)
                subscription = user.subscriptions.filter(podcast=podcast).first()
                episodes = podcast.episodes.filter(is_active=True).order_by('-id')
                total = episodes.count()
                if page < 1:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_first_page,
                    )
                elif total <= (page - 1) * 10:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_last_page,
                    )
                else:
                    start = (page - 1) * 10 + 1
                    end = page * 10 if total > page * 10 else total
                    bot.edit_message_text(
                        user.text.the_podcast_text.format(
                            image='',
                            name=podcast.name,
                            channel=podcast.channel,
                            description=f"\n\n{podcast.description}" if podcast.description else '',
                            start=start,
                            end=end,
                            total=total,
                            episodes='\n'.join([
                                f"{sequence}. {episode.name} <b>(<i>{episode.total_listens_count:,} 📥</i>)</b>"
                                for sequence, episode in enumerate(episodes[start - 1:end], 1)
                            ])
                        ),
                        message.chat.id,
                        message.message_id,
                        reply_markup=keyboards.get_the_podcast_episodes_inline_keyboard(user, podcast, subscription, total, start, end, page),
                        link_preview_options=types.LinkPreviewOptions(
                            prefer_large_media=True,
                            show_above_text=True,
                        ),
                    )
            except Podcast.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.podcast_not_found,
                )

        def select_the_episode(user: User, query: types.CallbackQuery, message: types.Message, episode_id: int):
            try:
                episode = Episode.objects.get(id=episode_id, file_id__isnull=False)
                bot.send_audio(
                    message.chat.id,
                    episode.file_id,
                    "<b>{name}</b>\n\n<i>{description}</i>".format(
                        name=episode.name,
                        description=episode.description,
                    ),
                    reply_markup=keyboards.get_the_episode_inline_keyboard(
                        user,
                        episode,
                        False,
                        episode.liked_users.filter(id=user.id).exists(),
                    ),
                )
                episode.total_listens_count += 1
                episode.save()
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.episode_not_found,
                )

        def open_the_timelapse(user: User, query: types.CallbackQuery, message: types.Message, episode_id: int):
            try:
                episode = Episode.objects.get(id=episode_id, file_id__isnull=False)
                bot.edit_message_caption(
                    episode.timelapse,
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_the_episode_inline_keyboard(
                        user,
                        episode,
                        True,
                        episode.liked_users.filter(id=user.id).exists(),
                    ),
                )
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.episode_not_found,
                )

        def close_the_timelapse(user: User, query: types.CallbackQuery, message: types.Message, episode_id: int):
            try:
                episode = Episode.objects.get(id=episode_id, file_id__isnull=False)
                bot.edit_message_caption(
                    "<b>{name}</b>\n\n{description}".format(
                        name=episode.name,
                        description=episode.description,
                    ),
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_the_episode_inline_keyboard(
                        user,
                        episode,
                        False,
                        episode.liked_users.filter(id=user.id).exists(),
                    ),
                )
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.episode_not_found,
                )

        def change_the_episode_like_state(user: User, query: types.CallbackQuery, message: types.Message, episode_id: int, is_liked: int):
            try:
                episode = Episode.objects.get(id=episode_id, file_id__isnull=False)
                if is_liked:
                    episode.liked_users.remove(user)
                    episode.total_likes_count -= 1
                    is_liked = False
                else:
                    episode.liked_users.add(user)
                    episode.total_likes_count += 1
                    is_liked = True
                bot.edit_message_reply_markup(
                    message.chat.id,
                    message.message_id,
                    reply_markup=keyboards.get_the_episode_inline_keyboard(
                        user,
                        episode,
                        "<i>" not in message.html_caption,
                        is_liked,
                    ),
                )
                episode.save()
                bot.answer_callback_query(
                    query.id,
                    user.text.you_liked_the_episode if is_liked else user.text.you_unliked_the_episode,
                )
            except Episode.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.episode_not_found,
                )

        def delete_the_episode(user: User, query: types.CallbackQuery, message: types.Message, episode_id: int):
            bot.delete_message(
                message.chat.id,
                message.message_id,
            )

        def select_the_search_query_episodes_page(user: User, query: types.CallbackQuery, message: types.Message, search_query_id: int, page: int):
            try:
                search_query = SearchQuery.objects.get(id=search_query_id)
                episodes = Episode.filter_by_search_query(search_query)
                total = episodes.count()
                if page < 1:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_first_page,
                    )
                elif total <= (page - 1) * 10:
                    bot.answer_callback_query(
                        query.id,
                        user.text.you_already_in_the_last_page,
                    )
                else:
                    start = (page - 1) * 10 + 1
                    end = page * 10 if total > page * 10 else total
                    bot.edit_message_caption(
                        user.text.search_result_text.format(
                            total=total,
                            start=start,
                            end=end,
                            episodes='\n'.join([
                                f"{sequence}. {episode.name} <b>(<i>{episode.total_listens_count:,} 📥</i>)</b>"
                                for sequence, episode in enumerate(episodes[start - 1:end], 1)
                            ])
                        ),
                        message.chat.id,
                        message.message_id,
                        reply_markup=keyboards.get_search_query_episodes_inline_keyboard(
                            user,
                            search_query,
                            episodes,
                            start,
                            end,
                            page,
                        ),
                    )
            except SearchQuery.DoesNotExist:
                bot.answer_callback_query(
                    query.id,
                    user.text.search_query_not_found,
                )

        def delete_the_message(user: User, query: types.CallbackQuery, message: types.Message, *args):
            bot.delete_message(
                message.chat.id,
                message.message_id,
            )

        try:
            user: User = User.objects.get(telegram_id=query.from_user.id)
        except User.DoesNotExist:
            full_name = helpers.extract_full_name(query.from_user)
            user = User.objects.create(
                telegram_id=query.from_user.id,
                full_name=full_name,
                username=query.from_user.username,
                text=Text.objects.filter(is_active=True).first(),
            )
        if query.data:
            step, *data = map(int, query.data.split())
            try:
                {
                    CALLBACK.SELECT_THE_TEXT: select_the_text,
                    CALLBACK.CHANGE_THE_CATEGORY_INTERESTED_STATE: change_the_category_interested_state,

                    CALLBACK.SELECT_TOP_EPISODES_PAGE: select_top_episodes_page,
                    CALLBACK.SELECT_NEWEST_EPISODES_PAGE: select_newest_episodes_page,
                    CALLBACK.SELECT_SUBSCRIPTIONS_PAGE: select_subscriptions_page,

                    CALLBACK.SELECT_COLLECTIONS_PAGE: select_collections_page,
                    CALLBACK.SELECT_THE_COLLECTION: select_the_collection,
                    CALLBACK.SELECT_THE_COLLECTION_PODCASTS_PAGE: select_the_collection_podcasts_page,

                    CALLBACK.SELECT_CHANNELS_PAGE: select_channels_page,
                    CALLBACK.SELECT_THE_CHANNEL: select_the_channel,
                    CALLBACK.SELECT_THE_CHANNEL_PODCASTS_PAGE: select_the_channel_podcasts_page,

                    CALLBACK.SELECT_PODCASTS_PAGE: select_podcasts_page,
                    CALLBACK.SELECT_THE_PODCAST: select_the_podcast,
                    CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_STATE: change_the_podcast_subscription_state,
                    CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_NOTIFICATION_STATE: change_the_podcast_subscription_notification_state,
                    CALLBACK.DOWNLOAD_ALL_EPISODES_OF_THE_PODCAST: download_all_episodes_of_the_podcast,
                    CALLBACK.SELECT_THE_PODCAST_EPISODES_PAGE: select_the_podcast_episodes_page,

                    CALLBACK.SELECT_THE_EPISODE: select_the_episode,
                    CALLBACK.OPEN_THE_TIMELAPSE: open_the_timelapse,
                    CALLBACK.CLOSE_THE_TIMELAPSE: close_the_timelapse,
                    CALLBACK.CHANGE_THE_EPISODE_LIKE_STATE: change_the_episode_like_state,
                    CALLBACK.DELETE_THE_EPISODE: delete_the_episode,

                    CALLBACK.SELECT_THE_SEARCH_QUERY_EPISODES_PAGE: select_the_search_query_episodes_page,

                    CALLBACK.DELETE_THE_MESSAGE: delete_the_message,
                }[step](user, query, query.message, *data)
                bot.answer_callback_query(query.id)
            except ApiException as e:
                Error.objects.create(
                    user=user,
                    type=ERROR.TYPE.API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER,
                    text=traceback.format_exc() or sys.exc_info()[2] or e.args or "Log does not exist"
                )
                bot.answer_callback_query(query.id)
            except Exception as e:
                Error.objects.create(
                    user=user,
                    type=ERROR.TYPE.EXCEPTION_ON_CALLBACK_QUERY_HANDLER,
                    text=traceback.format_exc() or sys.exc_info()[2] or e.args or "Log does not exist"
                )
                bot.answer_callback_query(query.id)
