from collections import namedtuple
from time import sleep
from typing import List

from django.utils import timezone
from requests import post

from telebot import TeleBot, types
from telebot.apihelper import ApiException
from transliterate import translit

from bot.utils import keyboards
from configurations.constants import CONSTANT

from basics.models import User
from classifiers.models import Constant


link_preview_options = types.LinkPreviewOptions(
    prefer_large_media=True,
    show_above_text=True,
)


def upload_file(bot, file_id):
    downloaded_file = bot.download_file(bot.get_file(file_id).file_path)
    file_path = post('https://telegra.ph/upload', files={'file': ('file', downloaded_file, 'image/jpeg')}).json()[0]['src']
    return f"https://telegra.ph{file_path}"


def extract_full_name(from_user: types.User):
    return f"{from_user.first_name}{f' {from_user.last_name}' if from_user.last_name else ''}".replace('<', '').replace('>', '')


def convert_to_latin(text: str):
    if not text.isascii():
        text = translit(text, 'ru', reversed=True)
    return text


def convert_to_cyrillic(text: str):
    return translit(text, 'ru')


def get_constant(key):
    constant, _ = Constant.objects.get_or_create(
        key=key,
        defaults={
            'data': CONSTANT.DEFAULT.get(key),
        },
    )
    return constant.actual_data


Command = namedtuple('Command', ['key', 'description'])


language_to_commands = {}


def get_available_commands(user: User) -> List[Command]:
    if not language_to_commands.get(user.text.code):
        language_to_commands[user.text.code] = [
            Command('start', user.text.start_command_description),
            Command('top', user.text.top_command_description),
            # Command('newest', user.text.newest_command_description),
            Command('subscriptions', user.text.subscriptions_command_description),
            # Command('collections', user.text.collections_command_description),
            # Command('channels', user.text.channels_command_description),
            Command('podcasts', user.text.podcasts_command_description),
            Command('interests', user.text.interests_command_description),
            Command('language', user.text.language_command_description),
        ]
    return language_to_commands.get(user.text.code)


def reset_commands(bot: TeleBot, user: User):
    bot.set_my_commands(
        [
            types.BotCommand(command.key, command.description) for command in get_available_commands(user)
        ],
        types.BotCommandScopeChat(
            user.telegram_id,
        ),
    )


def is_birth_date(raw: str):
    try:
        timezone.datetime.fromisoformat(raw)
        return True
    except ValueError:
        pass


def sending_new_episode_notification_to_subscribers(bot, episode):
    inline_markup = keyboards.new_episode_notification_inline_keyboard(episode)
    for subscription in episode.podcast.subscriptions.filter(
        user__is_active=True,
        is_notification_enabled=True,
    ):
        try:
            bot.send_message(
                subscription.user.telegram_id,
                subscription.user.text.new_episode_text.format(
                    full_name=subscription.user.full_name,
                    podcast=episode.podcast.name,
                    episode=episode.name,
                ),
                reply_markup=inline_markup,
            )
            sleep(0.05)
        except ApiException as e:
            error = str(e.args)
            if "deactivated" in error or "blocked by the user" in error:
                subscription.user.is_active = False
                subscription.user.save()
                continue
            print(error)


def sending_post(bot: TeleBot, message: types.Message, sender: User):
    total = 0
    users = list(User.objects.all())
    for user in users:
        try:
            if message.audio:
                bot.send_audio(
                    user.telegram_id,
                    message.audio.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.voice:
                bot.send_voice(
                    user.telegram_id,
                    message.voice.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.video:
                bot.send_video(
                    user.telegram_id,
                    message.video.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.photo:
                bot.send_photo(
                    user.telegram_id,
                    message.photo[-1].file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            else:
                bot.send_message(
                    user.telegram_id,
                    message.html_text,
                    reply_markup=message.reply_markup
                )
            total += 1
            sleep(0.05)
        except ApiException as e:
            error = str(e.args)
            if "deactivated" in error or "blocked by the user" in error:
                user.is_active = False
                user.save()
                continue
            else:
                users.append(user)
    bot.send_message(
        sender.telegram_id,
        sender.text.posting_end.format(
            user_counts=len(users),
            total=total
        )
    )
