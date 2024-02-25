from telebot import TeleBot

from bot.handlers.inline_query import initializer_inline_query_handlers
from bot.handlers.message import initializer_message_handlers
from bot.handlers.callback_query import initializer_callback_query_handlers
from bot.handlers.pre_checkout_query_handler import initializer_pre_checkout_query_handlers


def initializer(token: str) -> TeleBot:
    bot = TeleBot(token, 'html')

    initializer_message_handlers(bot)
    initializer_callback_query_handlers(bot)
    initializer_inline_query_handlers(bot)
    initializer_pre_checkout_query_handlers(bot)

    return bot
