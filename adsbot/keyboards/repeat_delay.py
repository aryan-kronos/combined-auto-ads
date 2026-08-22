# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def repeat_delay_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="1 Minute",
        callback_data="repeat_60",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5040034664614462519")
    )

    kb.button(
        text="10 Minutes",
        callback_data="repeat_600",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6024035324512964552")
    )

    kb.button(
        text="20 Minutes",
        callback_data="repeat_1200",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5915735340437474837")
    )

    kb.button(
        text="30 Minutes",
        callback_data="repeat_1800",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5913241115489734452")
    )

    kb.button(
        text="60 Minutes",
        callback_data="repeat_3600",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5805523262691611326")
    )

    kb.button(
        text="Custom Interval",
        callback_data="repeat_custom",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5370951118698339120")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.button(
            text="Back",
            callback_data="back_loop",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5409284148491726576")
        )
    

    kb.adjust(
        2,
        2,
        2,
        1,
        1
    )

    return kb.as_markup()