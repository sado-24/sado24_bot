import random
import sys
import traceback

from django.utils.html import strip_tags
from telebot import types, TeleBot

from actions.models import SearchQuery
from basics.models import User, Error
from bot.utils import helpers, keyboards
from classifiers.models import Text
from contents.models import Episode

from configurations.constants import ERROR


def initializer_inline_query_handlers(_: TeleBot):
    @_.inline_handler(lambda query: True)
    def inline_query_handler(query: types.InlineQuery, bot=_):
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
            try:
                offset = int(query.offset) if query.offset else 0
                if len(query.query) >= 3:
                    original_query = strip_tags(query.query.lower())
                    search_query, _ = SearchQuery.objects.get_or_create(
                        original_query=original_query,
                        defaults={
                            'latin_query': helpers.convert_to_latin(original_query),
                            'cyrillic_query': helpers.convert_to_cyrillic(original_query),
                        }
                    )
                    episodes = Episode.filter_by_search_query(search_query)
                else:
                    episodes = Episode.objects.filter(is_active=True)
                total = episodes.count()
                if offset < total:
                    results = [
                        types.InlineQueryResultCachedAudio(
                            random.randint(100000000, 999999999),
                            episode.file_id,
                            caption="<b>{name}</b>\n\n<i>{description}</i>".format(
                                name=episode.name,
                                description=episode.description,
                            ),
                            parse_mode='html',
                            reply_markup=keyboards.get_the_episode_deeplink_inline_keyboard(user, episode),
                        ) for episode in episodes[offset: offset + 10]
                    ]
                    bot.answer_inline_query(
                        str(query.id),
                        results,
                        cache_time=0,
                        is_personal=True,
                        next_offset=offset + 10 if offset + 10 <= total else None
                    )
            except Exception as e:
                Error.objects.create(
                    user=user,
                    type=ERROR.TYPE.EXCEPTION_ON_INLINE_QUERY_HANDLER,
                    text=traceback.format_exc() or sys.exc_info()[2] or e.args or "Log does not exist"
                )

