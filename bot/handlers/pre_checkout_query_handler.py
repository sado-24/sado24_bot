from telebot import TeleBot, types


def initializer_pre_checkout_query_handlers(bot: TeleBot):

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def checkout(pre_checkout_query: types.PreCheckoutQuery):
        bot.answer_pre_checkout_query(
            int(pre_checkout_query.id),
            True,
        )
