from telebot import types

from basics.models import User
from configurations.constants import CALLBACK
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


def get_top_episodes_inline_keyboard(episodes):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(episodes, 1)
    ])
    return inline_keyboard


def get_newest_episodes_inline_keyboard(episodes):
    return get_top_episodes_inline_keyboard(episodes)


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


def get_the_podcast_episodes_inline_markup(user: User, podcast, subscription, total, start, end, page=1):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    if subscription:
        inline_keyboard.add(
            types.InlineKeyboardButton(
                user.text.disable_notification if subscription.is_notification_enabled else user.text.enable_notification,
                callback_data=f"{CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_NOTIFICATION_STATE} {podcast.id} {total} {page}",
            ),
        )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            user.text.unsubscribe_from_the_podcast if subscription else user.text.subscribe_to_the_podcast,
            callback_data=f"{CALLBACK.CHANGE_THE_PODCAST_SUBSCRIPTION_STATE} {podcast.id} {total} {page}"
        )
    )
    inline_keyboard.add(*[
        types.InlineKeyboardButton(
            str(sequence),
            callback_data=f"{CALLBACK.SELECT_THE_EPISODE} {episode.id}"
        ) for sequence, episode in enumerate(podcast.episodes.filter(is_active=True)[start - 1: end], 1)
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


def get_the_collection_podcasts_inline_markup(user: User, collection, start, end, page=1):
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


def get_the_channel_podcasts_inline_markup(user: User, channel, start, end, page=1):
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


def get_search_query_episodes_inline_markup(user: User, search_query, episodes, start, end, page=1):
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
            user.text.unlike_it,
            callback_data=f"{CALLBACK.UNLIKE_IT} {episode.id}",
        ) if is_liked else types.InlineKeyboardButton(
            user.text.like_it,
            callback_data=f"{CALLBACK.LIKE_IT} {episode.id}",
        ),
        types.InlineKeyboardButton(
            user.text.delete_the_episode,
            callback_data=f"{CALLBACK.DELETE_THE_EPISODE} {episode.id}",
        ),
    )
    return inline_keyboard


def new_episode_notification_inline_markup(episode: Episode):
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
