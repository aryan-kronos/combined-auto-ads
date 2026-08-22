# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def target_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="All Joined Groups",
        callback_data="target_all_groups",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5409111052719767901")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.button(
            text="Back",
            callback_data="create_campaign",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5409284148491726576")
        )
    

    kb.adjust(
        1,
        1,
        1
    )

    return kb.as_markup()