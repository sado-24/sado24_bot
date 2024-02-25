import traceback
import sys
from threading import Thread

from django.utils.html import strip_tags
from django.db.models import Count, Q

from telebot import types, TeleBot
from telebot.handler_backends import ContinueHandling

from bot.utils import helpers, keyboards

from classifiers.models import Text
from contents.models import Channel, Podcast, Episode, Collection
from actions.models import SearchQuery

from configurations.constants import STEP, CONSTANT, ERROR
from basics.models import User, Error


def initializer_message_handlers(bot: TeleBot):
    def auth(*steps):
        def inner(handler):
            def wrapper(message: types.Message):
                try:
                    user: User = User.objects.get(telegram_id=message.from_user.id)
                    if user and user.text:
                        if not user.is_banned:
                            try:
                                if helpers.get_constant(CONSTANT.IS_BOT_WORKING):
                                    if user.step in steps or len(steps) == 0:
                                        return handler(message, user)
                                    else:
                                        return ContinueHandling()
                                else:
                                    bot.send_message(
                                        message.chat.id,
                                        user.text.bot_is_not_available,
                                    )
                                    user.set_step()
                                    bot.send_message(
                                        message.chat.id,
                                        user.text.main_text.format(
                                            commands='\n'.join([
                                                f"/{command.key} - {command.description}" for command in helpers.get_available_commands(user)
                                            ])
                                        ),
                                        reply_markup=keyboards.reply_keyboard_remove,
                                    )
                            except Exception as e:
                                Error.objects.create(
                                    user=user,
                                    type=ERROR.TYPE.GENERAL,
                                    text=traceback.format_exc() or sys.exc_info()[2] or e.args or "No error message"
                                )
                        else:
                            bot.send_message(
                                message.chat.id,
                                user.text.you_are_banned,
                                reply_markup=keyboards.reply_keyboard_remove,
                            )
                    else:
                        raise User.DoesNotExist()
                except User.DoesNotExist:
                    start_handler(message)

            return wrapper
        return inner

    def go_to_main(message: types.Message, user: User):
        user.set_step()
        bot.send_message(
            message.chat.id,
            user.text.main_text.format(
                commands='\n'.join([
                    f"/{command.key} - {command.description}" for command in helpers.get_available_commands(user)
                ])
            ),
            reply_markup=keyboards.reply_keyboard_remove,
        )

    @bot.message_handler(commands=['start'])
    def start_handler(message: types.Message):
        try:
            user: User = User.objects.get(telegram_id=message.from_user.id)
            if not user.is_active:
                user.is_active = True
                user.save()
        except User.DoesNotExist:
            full_name = helpers.extract_full_name(message.from_user)
            user: User = User.objects.create(
                telegram_id=message.from_user.id,
                full_name=full_name,
                username=message.from_user.username,
            )
        if not user.text:
            texts = Text.objects.filter(is_active=True)
            if not texts:
                text = Text.objects.create(
                    sequence=0,
                    code='uz',
                    name="O'zbekcha",
                )
                texts = Text.objects.filter(is_active=True)
            else:
                text = texts.first()
            bot.send_message(
                message.chat.id,
                text.selecting_language_text,
                reply_markup=keyboards.get_texts_inline_keyboard(texts),
            )
        else:
            _ = message.text.split()
            if len(_) > 1:
                episode_id = _[1]
                if episode_id.isdigit():
                    try:
                        episode = Episode.objects.get(id=episode_id)
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
                        return
                    except Episode.DoesNotExist:
                        pass
            go_to_main(message, user)

    @bot.message_handler(commands=['top'])
    @auth(STEP.MAIN)
    def top_handler(message: types.Message, user: User):
        episodes = Episode.objects.filter(is_active=True).annotate(
            matched_interested_categories_count=Count(
                'podcast__categories',
                filter=Q(podcast__categories__in=user.interested_categories.all()),
                distinct=True,
            ),
        ).order_by('-matched_interested_categories_count', '-total_listens_count', '-total_likes_count', '-id')
        if episodes:
            total = episodes.count()
            start = 1
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.top_text.format(
                    total=total,
                    start=start,
                    end=end,
                    episodes='\n'.join([
                        f"{sequence}. {episode.name} <i>{episode.total_listens_count:,} 📥</i>"
                        for sequence, episode in enumerate(episodes[start - 1: end], 1)
                    ])
                ),
                reply_markup=keyboards.get_top_episodes_inline_keyboard(user, episodes, start, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.bot_is_not_available,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['newest'])
    @auth(STEP.MAIN)
    def newest_handler(message: types.Message, user: User):
        episodes = Episode.objects.filter(is_active=True).order_by('-added_time')
        if episodes:
            total = episodes.count()
            start = 1
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.newest_text.format(
                    total=total,
                    start=start,
                    end=end,
                    episodes='\n'.join([
                        f"{sequence}. {episode.name} <i>{episode.total_listens_count:,} 📥</i>"
                        for sequence, episode in enumerate(episodes[start - 1: end], 1)
                    ])
                ),
                reply_markup=keyboards.get_newest_episodes_inline_keyboard(user, episodes, start, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.bot_is_not_available,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['subscriptions'])
    @auth(STEP.MAIN)
    def subscriptions_handler(message: types.Message, user: User):
        subscriptions = user.subscriptions.filter(podcast__is_active=True)
        if subscriptions:
            total = subscriptions.count()
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.subscriptions_text.format(
                    total=total,
                    start=1,
                    end=end,
                    subscriptions='\n'.join([
                        f"{sequence}. {subscription.podcast.name}"
                        for sequence, subscription in enumerate(subscriptions[:10], 1)
                    ])
                ),
                reply_markup=keyboards.get_subscriptions_inline_keyboard(user, subscriptions, 1, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.subscriptions_not_found,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['collections'])
    @auth(STEP.MAIN)
    def collections_handler(message: types.Message, user: User):
        collections = Collection.objects.filter(is_active=True)
        if collections:
            total = collections.count()
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.collections_text.format(
                    total=total,
                    start=1,
                    end=end,
                    collections='\n'.join([
                        f"{sequence}. {collection.name}"
                        for sequence, collection in enumerate(collections[:10], 1)
                    ])
                ),
                reply_markup=keyboards.get_collections_inline_keyboard(user, collections, 1, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.collections_not_found,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['channels'])
    @auth(STEP.MAIN)
    def channels_handler(message: types.Message, user: User):
        channels = Channel.objects.filter(is_active=True)
        if channels:
            total = channels.count()
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.channels_text.format(
                    total=total,
                    start=1,
                    end=end,
                    channels='\n'.join([
                        f"{sequence}. {channel.name}"
                        for sequence, channel in enumerate(channels[:10], 1)
                    ])
                ),
                reply_markup=keyboards.get_channels_inline_keyboard(user, channels, 1, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.channels_not_found,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['podcasts'])
    @auth(STEP.MAIN)
    def podcasts_handler(message: types.Message, user: User):
        podcasts = Podcast.objects.filter(is_active=True).annotate(
            matched_interested_categories_count=Count(
                'categories',
                filter=Q(categories__in=user.interested_categories.all()),
                distinct=True,
            ),
        ).order_by('-matched_interested_categories_count')
        if podcasts:
            total = podcasts.count()
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.podcasts_text.format(
                    total=total,
                    start=1,
                    end=end,
                    podcasts='\n'.join([
                        f"{sequence}. {podcast.name}"
                        for sequence, podcast in enumerate(podcasts[:10], 1)
                    ])
                ),
                reply_markup=keyboards.get_podcasts_inline_keyboard(user, podcasts, 1, end),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.podcasts_not_found,
                reply_markup=keyboards.reply_keyboard_remove,
            )
            go_to_main(message, user)

    @bot.message_handler(commands=['interests'])
    @auth(STEP.MAIN)
    def interests_handler(message: types.Message, user: User):
        bot.send_message(
            message.chat.id,
            user.text.selecting_interested_categories,
            reply_markup=keyboards.get_interested_categories_inline_keyboard(
                user,
                list(user.interested_categories.values_list('id', flat=True)),
            ),
        )

    @bot.message_handler(commands=['language'])
    @auth(STEP.MAIN)
    def language_handler(message: types.Message, user: User):
        bot.send_message(
            message.chat.id,
            user.text.selecting_language_text,
            reply_markup=keyboards.get_texts_inline_keyboard(Text.objects.filter(is_active=True)),
        )

    @bot.message_handler(commands=['developer'])
    @auth(STEP.MAIN)
    def developer_handler(message: types.Message, user: User):
        bot.send_message(
            message.chat.id,
            "👨🏻‍💻 @anvarjamgirov",
        )

    @bot.message_handler(commands=['post'])
    @auth(STEP.MAIN)
    def post_handler(message: types.Message, user: User):
        if user.is_admin:
            user.set_step(STEP.GETTING_POST_MESSAGE)
            bot.send_message(
                message.chat.id,
                user.text.send_me_post_message,
                reply_markup=keyboards.get_keyboard_markup([user.text.back])
            )

    @bot.message_handler(regexp="^🔙 ")
    @auth()
    def back_handler(message: types.Message, user: User):
        go_to_main(message, user)

    @bot.message_handler(func=lambda message: True)
    @auth(STEP.GETTING_POST_MESSAGE)
    def getting_post_message_handler(message: types.Message, user: User):
        user.set_step()
        bot.reply_to(
            message,
            user.text.posting_starts_please_wait,
        )
        thread = Thread(target=helpers.sending_post, args=(bot, message, user))
        thread.start()

    @bot.message_handler(func=lambda message: True)
    @auth()
    def all_message_handler(message: types.Message, user: User):
        original_query = strip_tags(message.text.lower())
        search_query, _ = SearchQuery.objects.get_or_create(
            original_query=original_query,
            defaults={
                'latin_query': helpers.convert_to_latin(original_query),
                'cyrillic_query': helpers.convert_to_cyrillic(original_query),
            }
        )
        episodes = Episode.filter_by_search_query(search_query)
        if episodes.count():
            total = episodes.count()
            start = 1
            end = 10 if total > 10 else total
            bot.send_message(
                message.chat.id,
                user.text.search_result_text.format(
                    total=total,
                    start=start,
                    end=end,
                    episodes='\n'.join([
                        f"{sequence}. {episode.name} <i>{episode.total_listens_count:,} 📥</i>"
                        for sequence, episode in enumerate(episodes[:10], 1)
                    ])
                ),
                reply_markup=keyboards.get_search_query_episodes_inline_keyboard(
                    user,
                    search_query,
                    episodes,
                    start,
                    end,
                ),
            )
        else:
            bot.send_message(
                message.chat.id,
                user.text.search_result_is_empty,
                reply_markup=keyboards.reply_keyboard_remove,
            )

    @bot.message_handler(content_types=['audio'])
    @auth(STEP.GETTING_POST_MESSAGE)
    def audio_for_post_handler(message: types.Message, user: User):
        user.set_step()
        bot.reply_to(
            message,
            user.text.posting_starts_please_wait,
        )
        thread = Thread(target=helpers.sending_post, args=(bot, message, user))
        thread.start()

    @bot.message_handler(content_types=['audio'])
    @auth()
    def audio_handler(message: types.Message, user: User):
        if user.is_admin or user.is_moderator:
            if not message.audio.title:
                bot.send_message(
                    message.chat.id,
                    "<b>This audio file is not valid.</b>\n\nPlease enter audio file <b>with title</b>.",
                )
            elif not message.audio.performer:
                bot.send_message(
                    message.chat.id,
                    "<b>This audio file is not valid.</b>\n\nPlease enter audio file <b>with performer</b>.",
                )
            else:
                bot.reply_to(
                    message,
                    "Title: <code>{title}</code>\nPerformer: <code>{performer}</code>\n\nFile ID: <code>{file_id}</code>\n\nDuration: <code>{duration}</code>".format(
                        title=message.audio.title,
                        performer=message.audio.performer,
                        file_id=message.audio.file_id,
                        duration=message.audio.duration,
                    )
                )

    @bot.message_handler(content_types=['voice'])
    @auth(STEP.GETTING_POST_MESSAGE)
    def voice_for_post_handler(message: types.Message, user: User):
        user.set_step()
        bot.reply_to(
            message,
            user.text.posting_starts_please_wait,
        )
        thread = Thread(target=helpers.sending_post, args=(bot, message, user))
        thread.start()

    @bot.message_handler(content_types=['voice'])
    @auth()
    def voice_handler(message: types.Message, user: User):
        if user.is_admin or user.is_moderator:
            bot.reply_to(
                message,
                f"<code>{message.voice.file_id}</code>"
            )

    @bot.message_handler(content_types=['video'])
    @auth(STEP.GETTING_POST_MESSAGE)
    def video_for_post_handler(message: types.Message, user: User):
        user.set_step()
        bot.reply_to(
            message,
            user.text.posting_starts_please_wait,
        )
        thread = Thread(target=helpers.sending_post, args=(bot, message, user))
        thread.start()

    @bot.message_handler(content_types=['video'])
    @auth()
    def video_handler(message: types.Message, user: User):
        if user.is_admin or user.is_moderator:
            bot.reply_to(
                message,
                f"<code>{message.video.file_id}</code>"
            )

    @bot.message_handler(content_types=['photo'])
    @auth(STEP.GETTING_POST_MESSAGE)
    def photo_for_post_handler(message: types.Message, user: User):
        user.set_step()
        bot.reply_to(
            message,
            user.text.posting_starts_please_wait,
        )
        thread = Thread(target=helpers.sending_post, args=(bot, message, user))
        thread.start()

    @bot.message_handler(content_types=['photo'])
    @auth()
    def photo_handler(message: types.Message, user: User):
        if user.is_admin or user.is_moderator:
            bot.reply_to(
                message,
                f"<code>{helpers.upload_file(bot, message.photo[-1].file_id)}</code>"
            )
