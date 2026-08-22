# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config


def dashboard_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Developer (Aryan)",
        url=config.DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )

    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)
    return kb.as_markup()
