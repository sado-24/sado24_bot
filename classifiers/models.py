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
        default="<b>Top 10</b>\n\n{episodes}",
    )
    newest_text = models.TextField(
        default="<b>Eng yangi 10 ta epizod</b>\n\n{episodes}",
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
        default="<a href='{image}'>&#8203;&#8203;</a><b>{name}</b>\n\n<i>{description}</i>\n\n{episodes}",
    )
    search_result_text = models.TextField(
        default="<b>Natijalar {start}-{end} {total}dan</b>\n\n{episodes}"
    )
    search_result_is_empty = models.TextField(
        default="Sizning so'rovingiz bo'yicha bironta ham epizod topilmadi, iltimos so'rov matnini o'zgartirib qayta urinib ko'ring."
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
    language_command_description = models.TextField(
        default="Tilni o'zgartirish.",
    )

    subscribe_to_the_podcast = models.CharField(
        max_length=63,
        default="➕ Obuna bo'lish",
    )
    unsubscribe_from_the_podcast = models.CharField(
        max_length=63,
        default="➖ Obunani bekor qilish",
    )
    enable_notification = models.CharField(
        max_length=63,
        default="🔔 Bildirishnomani yoqish",
    )
    disable_notification = models.CharField(
        max_length=63,
        default="🔕 Bildirishnomani o'chirish",
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
        default="🎙 Podkast",
    )
    opening_the_timelapse = models.CharField(
        max_length=63,
        default="📂 Boblarni ochish"
    )
    closing_the_timelapse = models.CharField(
        max_length=63,
        default="📁 Boblarni yopish"
    )
    like_it = models.CharField(
        max_length=63,
        default="❤️",
    )
    unlike_it = models.CharField(
        max_length=63,
        default="💔",
    )
    delete_the_episode = models.CharField(
        max_length=63,
        default="❌",
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
    name = models.CharField(
        max_length=31,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

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
