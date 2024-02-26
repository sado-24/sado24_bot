from typing import List

from telebot import types

from basics.models import User
from classifiers.models import Category
from configurations.constants import CALLBACK, BOT
from contents.models import Episode

reply_keyboard_remove = types.ReplyKeyboardRemove()


def get_keyboard_markup(buttons, on_time=True, row_width=3):
    keyboard_markup = types.ReplyKeyboardMarkup(True, on_time, row_width=row_width)
    for row in buttons:
        if type(row) is list:
            keyboard_markup.add(
                *[
                    types.KeyboardButton(
                        str(button),
                        request_contact=True if button.startswith("📞 ") else None,
                        request_location=True if button.startswith("📍 ") else None
                    ) if type(button) in [str, int] else button for button in row if not None
                ]
            )
        elif row is not None:
            keyboard_markup.add(
                types.KeyboardButton(
                    str(row),
                    request_contact=True if row.startswith("📞 ") else None,
                    request_location=True if row.startswith("📍 ") else None
                ) if type(row) in [str, int] else row
            )
    return keyboard_markup


def get_texts_inline_keyboard(texts):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            text.name,
            callback_data=f"{CALLBACK.SELECT_THE_TEXT} {text.id}"
        ) for text in texts
    ])
    return inline_keyboard


def get_interested_categories_inline_keyboard(user: User, interested_categories: List[int]):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            f"{'✅' if category.id in interested_categories else '☑️'} {category.name(user.text.code)}",
            callback_data=f"{CALLBACK.CHANGE_THE_CATEGORY_INTERESTED_STATE} {category.id}"
        ) for category in Category.objects.filter(is_active=True)[:100]
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}"
        ),
        types.InlineKeyboardButton(
            user.text.confirm,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE} 0"
        )
    )
    return inline_keyboard


def get_top_episodes_inline_keyboard(user, episodes, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(episodes[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_TOP_EPISODES_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_TOP_EPISODES_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_newest_episodes_inline_keyboard(user, episodes, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(episodes[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_NEWEST_EPISODES_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_NEWEST_EPISODES_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_subscriptions_inline_keyboard(user: User, subscriptions, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST} {subscription.podcast_id}"
        ) for sequence, subscription in enumerate(subscriptions[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_SUBSCRIPTIONS_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_SUBSCRIPTIONS_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_collections_inline_keyboard(user: User, collections, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_COLLECTION} {collection.id}"
        ) for sequence, collection in enumerate(collections[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_COLLECTIONS_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_COLLECTIONS_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_channels_inline_keyboard(user: User, channels, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_CHANNEL} {channel.id}"
        ) for sequence, channel in enumerate(channels[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_CHANNELS_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_CHANNELS_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_podcasts_inline_keyboard(user: User, podcasts, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST} {podcast.id}"
        ) for sequence, podcast in enumerate(podcasts[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_PODCASTS_PAGE} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_PODCASTS_PAGE} {page + 1}",
        ),
    )
    return inline_keyboard


def get_the_podcast_episodes_inline_keyboard(user: User, podcast, subscription, total, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    row = []
    if subscription:
        row.append(
            types.InlineKeyboardButton(
                user.text.notification_is_enabled if subscription.is_notification_enabled else user.text.notification_is_disabled,
                callback_data=f"{CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_NOTIFICATION_STATE} {podcast.id} {total} {page}",
            ),
        )
    inline_keyboard.add(
        *row,
        types.InlineKeyboardButton(
            user.text.subscribed_to_the_podcast if subscription else user.text.unsubscribed_from_the_podcast,
            callback_data=f"{CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_STATE} {podcast.id} {total} {page}"
        ),
        types.InlineKeyboardButton(
            user.text.download_all_episodes_of_the_podcast,
            callback_data=f"{CALLBACK.DOWNLOAD_ALL_EPISODES_OF_THE_PODCAST} {podcast.id}"
        )
    )
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(podcast.episodes.filter(is_active=True).order_by('-id')[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST_EPISODES_PAGE} {podcast.id} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST_EPISODES_PAGE} {podcast.id} {page + 1}",
        ),
    )
    return inline_keyboard


def get_the_collection_podcasts_inline_keyboard(user: User, collection, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST} {podcast.id}"
        ) for sequence, podcast in enumerate(collection.podcasts.filter(is_active=True)[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_THE_COLLECTION_PODCASTS_PAGE} {collection.id} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_THE_COLLECTION_PODCASTS_PAGE} {collection.id} {page + 1}",
        ),
    )
    return inline_keyboard


def get_the_channel_podcasts_inline_keyboard(user: User, channel, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST} {podcast.id}"
        ) for sequence, podcast in enumerate(channel.podcasts.filter(is_active=True)[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_THE_CHANNEL_PODCASTS_PAGE} {channel.id} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_THE_CHANNEL_PODCASTS_PAGE} {channel.id} {page + 1}",
        ),
    )
    return inline_keyboard


def get_search_query_episodes_inline_keyboard(user: User, search_query, episodes, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(episodes[start - 1: end], 1)
    ])
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.previous,
            callback_data=f"{CALLBACK.SELECT_THE_SEARCH_QUERY_EPISODES_PAGE} {search_query.id} {page - 1}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_message,
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}",
        ),
        types.InlineKeyboardButton(
            user.text.next,
            callback_data=f"{CALLBACK.SELECT_THE_SEARCH_QUERY_EPISODES_PAGE} {search_query.id} {page + 1}",
        ),
    )
    return inline_keyboard


def get_the_episode_inline_keyboard(user: User, episode: Episode, is_timelapse_open=False, is_liked=False):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.the_podcast,
            callback_data=f"{CALLBACK.SELECT_THE_PODCAST} {episode.podcast_id}",
        ),
        types.InlineKeyboardButton(
            user.text.closing_the_timelapse,
            callback_data=f"{CALLBACK.CLOSE_THE_TIMELAPSE} {episode.id}",
        ) if is_timelapse_open else types.InlineKeyboardButton(
            user.text.opening_the_timelapse,
            callback_data=f"{CALLBACK.OPEN_THE_TIMELAPSE} {episode.id}"
        ),
    )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.liked if is_liked else user.text.unliked,
            callback_data=f"{CALLBACK.CHANGE_THE_EPISODE_LIKE_STATE} {episode.id} {'1' if is_liked else '0'}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_episode,
            callback_data=f"{CALLBACK.DELETE_THE_EPISODE} {episode.id}",
        ),
    )
    return inline_keyboard


def get_the_episode_deeplink_inline_keyboard(user: User, episode: Episode):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.go_to_the_bot,
            url=f"https://t.me/{BOT.USERNAME}?start={episode.id}"
        ),
    )
    return inline_keyboard


def new_episode_notification_inline_keyboard(episode: Episode):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(
            '🎧',
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ),
        types.InlineKeyboardButton(
            '❌',
            callback_data=f"{CALLBACK.DELETE_THE_MESSAGE}"
        )
    )
    return inline_keyboard
