# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def send_mode_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Copy",
        callback_data="send_copy",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5212921495008845628")
    )

    kb.button(
        text="Forward",
        callback_data="send_forward",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6129802875611651951")
    )

    kb.adjust(2)

    return kb.as_markup()