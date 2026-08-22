# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def time_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="5 Minutes",
        callback_data="time_300",
        style="primary"
    )

    kb.button(
        text="10 Minutes",
        callback_data="time_600",
        style="primary"
    )

    kb.button(
        text="30 Minutes",
        callback_data="time_1800",
        style="primary"
    )

    kb.button(
        text="1 Hour (Recommended)",
        callback_data="time_3600",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="2 Hours",
        callback_data="time_7200",
        style="primary"
    )

    kb.button(
        text="6 Hours",
        callback_data="time_21600",
        style="primary"
    )

    kb.button(
        text="12 Hours",
        callback_data="time_43200",
        style="primary"
    )

    kb.button(
        text="Custom Minutes",
        callback_data="time_custom",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5370951118698339120")
    )

    kb.button(
        text="Back",
        callback_data="bio_continue",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(2, 2, 2, 1, 1, 1)

    return kb.as_markup()