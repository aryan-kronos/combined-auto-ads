# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_campaign_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Start Campaign",
        callback_data="start_campaign",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5389057356493511934")
    )

    kb.button(
        text="Cancel",
        callback_data="cancel_campaign",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5974083768233760323")
    )

    kb.button(
        text="Back",
        callback_data="back_delay",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(
        1,
        2,
        1
    )

    return kb.as_markup()