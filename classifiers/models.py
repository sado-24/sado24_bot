from django.db import models

from configurations.abstracts import AbstractModel
from configurations.constants import CONSTANT


class Text(AbstractModel):
    sequence = models.IntegerField()
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text='uz, ru, en and etc.'
    )
    name = models.CharField(
        max_length=31,
    )
    selecting_language_text = models.TextField(
        default="Kerakli tilni tanlang",
    )
    selecting_interested_categories = models.TextField(
        default="Qaysi sohalarga qiziqasiz ?\n\n<i>Quyidagilardan sizni qiziqtirganlarini tanlang.</i>",
    )
    hello_text = models.TextField(
        default="Assalom aleykum <b>{full_name}</b>.",
    )
    main_text = models.TextField(
        default="Botdan foydalanishda ushbu buyruqlardan foydalanishingiz mumkin.\n\n{commands}",
    )
    you_are_banned = models.TextField(
        default="Siz hozirda tizimdan foydalanolmaysiz, qo'shimcha ma'lumot uchun @username ga murojaat qiling."
    )
    bot_is_not_available = models.TextField(
        default="Bot ish faoliyatida emas, iltimos keyinroq urinib ko'ring.",
    )
    send_me_post_message = models.TextField(
        default="Foydalanuvchilarga yubormoqchi bo‘lgan xabaringizni menga yuboring.\n\n<b>Diqqat foydalanuvchilarga oddiy textli, fotosuratli(faqat bitta fotosurat bo‘lishi kerak), videoli, ovozli xabarli yoki audioli xabar yuborishingiz mumkin.</b>\n\n<i>Xabar yuborish boshlanganidan so‘ng uni to‘xtatish imkonsiz, shu sababli yuborayotgan xabaringiz to‘g‘riligiga ishoch hosil qiling.</i>",
    )
    posting_starts_please_wait = models.TextField(
        default="⏳ Xabar yuborish jarayoni boshlandi, iltimos kutib turing, barchaga yuborib bo‘lgach sizga xabar beraman.",
    )
    posting_end = models.TextField(
        default="✅ Xabar foydalanuvchilarga yuborildi.\n\nBarcha foydalanuvchilar: {user_counts} ta\nXabar yuborilgan foydalanuvchilar: {total} ta",
    )
    getting_comment_text = models.TextField(
        default="Bizning bot haqida o'z fikrlaringizni qoldirishingiz mumkin, bu bizga tizimni yaxshilashda katta yordam beradi.",
    )

    subscriptions_not_found = models.TextField(
        default="Siz hozircha bironta ham podkastga obuna bo'lmagansiz.",
    )
    collections_not_found = models.TextField(
        default="Hozirda tizimda bironta ham to'plam mavjud emas, iltimos keyinroq qayta urinib ko'ring.",
    )
    channels_not_found = models.TextField(
        default="Hozirda tizimda bironta ham kanal mavjud emas, iltimos keyinroq qayta urinib ko'ring.",
    )
    podcasts_not_found = models.TextField(
        default="Hozirda tizimda bironta ham podkast mavjud emas, iltimos keyinroq qayta urinib ko'ring.",
    )
    collection_not_found = models.TextField(
        default="🤷🏻‍♂️ Siz ko'rmoqchi bo'lgan to'plam tizimdan o'chirib yuborilgan.",
    )
    channel_not_found = models.TextField(
        default="🤷🏻‍♂️ Siz ko'rmoqchi bo'lgan kanal tizimdan o'chirib yuborilgan.",
    )
    podcast_not_found = models.TextField(
        default="🤷🏻‍♂️ Siz ko'rmoqchi bo'lgan podkast tizimdan o'chirib yuborilgan.",
    )
    episode_not_found = models.TextField(
        default="🤷🏻‍♂️ Siz yuklamoqchi bo'lgan epizod tizimdan o'chirib yuborilgan.",
    )
    search_query_not_found = models.TextField(
        default="🤷🏻‍♂️ Qidiruv vaqti eskirgan iltimos qaytadan urinib ko'ring.",
    )

    new_episode_text = models.TextField(
        default="Assalom aleykum <b>{full_name}</b>, siz obuna bo'lgan <b>{podcast}</b> podkastida yangi <b>{episode}</b> epizodi paydo bo'ldi.\n\n<i>Tinglash uchun quyidagi tugmadan foydalaning.</i>"
    )

    top_text = models.TextField(
        default="<b>Top {start}-{end} {total}ta dan</b>\n\n{episodes}",
    )
    newest_text = models.TextField(
        default="<b>Eng yangi {start}-{end} {total}ta dan</b>\n\n{episodes}",
    )
    subscriptions_text = models.TextField(
        default="<b>Obunalar {start}-{end} {total}dan</b>\n\n{subscriptions}",
    )
    collections_text = models.TextField(
        default="<b>To'plamlar {start}-{end} {total}dan</b>\n\n{collections}",
    )
    the_collection_text = models.TextField(
        default="<a href='{image}'>&#8203;&#8203;</a><b>{name}</b>\n\n{podcasts}",
    )
    channels_text = models.TextField(
        default="<b>Kanallar {start}-{end} {total}dan</b>\n\n{channels}",
    )
    the_channel_text = models.TextField(
        default="<a href='{image}'>&#8203;&#8203;</a><b>{name}</b>\n\n{podcasts}",
    )
    podcasts_text = models.TextField(
        default="<b>Podkastlar {start}-{end} {total}dan</b>\n\n{podcasts}",
    )
    the_podcast_text = models.TextField(
        default="<a href='{image}'>&#8203;&#8203;</a><b>{name}</b>\n<u>{channel}</u><i>{description}</i>\n\n<b>Epizodlar {start}-{end} {total}dan<b>\n\n{episodes}",
    )
    search_result_text = models.TextField(
        default="<b>Natijalar {start}-{end} {total}dan</b>\n\n{episodes}"
    )
    search_result_is_empty = models.TextField(
        default="Sizning so'rovingiz bo'yicha bironta ham epizod topilmadi, iltimos so'rov matnini o'zgartirib qayta urinib ko'ring."
    )

    you_have_subscribed = models.TextField(
        default="✅ Obuna bo'ldingiz."
    )
    you_have_unsubscribed = models.TextField(
        default="☑️ Obunani bekor qildingiz."
    )
    you_have_enabled_notification = models.TextField(
        default="🔔 Bildirishnomani yoqdingiz."
    )
    you_have_disabled_notification = models.TextField(
        default="🔕 Bildirishnomani o'chirdingiz."
    )
    you_liked_the_episode = models.TextField(
        default="❤️ Siz ushbu epizodni yoqtirishingizni belgiladingiz.",
    )
    you_unliked_the_episode = models.TextField(
        default="💔 Siz ushbu epizodni yoqtirishingizni bekor qildingiz.",
    )

    you_already_in_the_first_page = models.TextField(
        default="Siz allaqachon birinchi sahifadasiz",
    )
    you_already_in_the_last_page = models.TextField(
        default="Siz allaqachon oxirgi sahifadasiz",
    )

    start_command_description = models.TextField(
        default="Foydalanishni boshlash yoki qayta ishga tushirish.",
    )
    top_command_description = models.TextField(
        default="Top (eshitishlar soni bo'yicha)",
    )
    newest_command_description = models.TextField(
        default="Yangi epizodlar",
    )
    subscriptions_command_description = models.TextField(
        default="Obuna bo'lingan podkastlar",
    )
    collections_command_description = models.TextField(
        default="To'plamlar",
    )
    channels_command_description = models.TextField(
        default="Kanallar ro'yxati",
    )
    podcasts_command_description = models.TextField(
        default="Mavjud podkastlar",
    )
    interests_command_description = models.TextField(
        default="Qiziqishlarni tanlash.",
    )
    language_command_description = models.TextField(
        default="Tilni o'zgartirish.",
    )

    subscribed_to_the_podcast = models.CharField(
        max_length=63,
        default="✅ Obuna",
    )
    unsubscribed_from_the_podcast = models.CharField(
        max_length=63,
        default="☑️ Obuna",
    )
    notification_is_enabled = models.CharField(
        max_length=63,
        default="🔔",
    )
    notification_is_disabled = models.CharField(
        max_length=63,
        default="🔕",
    )
    download_all_episodes_of_the_podcast = models.CharField(
        max_length=63,
        default="📥",
    )
    previous = models.CharField(
        max_length=63,
        default="⬅️",
    )
    delete_the_message = models.CharField(
        max_length=63,
        default="❌",
    )
    next = models.CharField(
        max_length=63,
        default="➡️",
    )
    the_podcast = models.CharField(
        max_length=63,
        default="🎙 Epizodlar",
    )
    opening_the_timelapse = models.CharField(
        max_length=63,
        default="📂 Boblarni ochish"
    )
    closing_the_timelapse = models.CharField(
        max_length=63,
        default="📁 Boblarni yopish"
    )
    liked = models.CharField(
        max_length=63,
        default="❤️",
    )
    unliked = models.CharField(
        max_length=63,
        default="💔",
    )
    delete_the_episode = models.CharField(
        max_length=63,
        default="❌",
    )
    confirm = models.CharField(
        max_length=63,
        default="📌 Tasdiqlash"
    )
    go_to_the_bot = models.CharField(
        max_length=63,
        default="🤖 Botda to'liq ko'rish",
    )

    back = models.CharField(
        max_length=15,
        default="🔙 ortga"
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"[{self.code}] {self.name}"

    class Meta:
        ordering = ['sequence', ]


class Category(AbstractModel):
    sequence = models.IntegerField()
    name_uz = models.CharField(
        max_length=31,
    )
    name_ru = models.CharField(
        max_length=31,
    )
    name_en = models.CharField(
        max_length=31,
    )
    name_tr = models.CharField(
        max_length=31,
    )
    name_kz = models.CharField(
        max_length=31,
    )
    name_kg = models.CharField(
        max_length=31,
    )
    name_tj = models.CharField(
        max_length=31,
    )
    name_tm = models.CharField(
        max_length=31,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def name(self, language: str):
        if language.endswith('ru'):
            return self.name_ru
        elif language.endswith('en'):
            return self.name_en
        elif language.endswith('tr'):
            return self.name_tr
        elif language.endswith('kz'):
            return self.name_kz
        elif language.endswith('kg'):
            return self.name_kg
        elif language.endswith('tj'):
            return self.name_tj
        elif language.endswith('tm'):
            return self.name_tm
        return self.name_uz

    def __str__(self):
        return self.name_uz

    class Meta:
        ordering = ['sequence', ]


class Constant(AbstractModel):
    key = models.CharField(
        max_length=15,
        unique=True,
        choices=CONSTANT.CHOICES,
        verbose_name="Ключ",
    )
    data = models.TextField(
        verbose_name="Данные",
        null=True,
        blank=True,
    )

    @property
    def actual_data(self):
        if self.data.isdigit():
            return int(self.data)
        return self.data

    def __str__(self):
        return f"{self.key}: {self.data}"
