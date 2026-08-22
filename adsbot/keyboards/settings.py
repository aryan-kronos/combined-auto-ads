# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🌐 Language",
        callback_data="language_menu"
    )

    kb.button(
        text="ℹ️ About",
        callback_data="about"
    )

    kb.button(
        text="Back",
        callback_data="home"
    )

    kb.adjust(1)

    return kb.as_markup()


def language_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🇬🇧 English",
        callback_data="lang_en"
    )

    kb.button(
        text="🇷🇺 Русский",
        callback_data="lang_ru"
    )

    kb.button(
        text="🇨🇳 中文",
        callback_data="lang_zh"
    )

    kb.button(
        text="🇸🇦 العربية",
        callback_data="lang_ar"
    )

    kb.button(
        text="Back",
        callback_data="settings"
    )

    kb.adjust(1)

    return kb.as_markup()