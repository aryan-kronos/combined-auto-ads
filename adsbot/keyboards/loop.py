# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def loop_keyboard(is_premium: bool = False):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="1 Loop",
        callback_data="loop_1",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="2 Loops",
        callback_data="loop_2",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="5 Loops",
        callback_data="loop_5",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="10 Loops",
        callback_data="loop_10",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="20 Loops",
        callback_data="loop_20",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="Infinite Loop",
        callback_data="loop_infinite",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5364087614930431949")
    )

    kb.button(
        text="Custom Loop",
        callback_data="loop_custom",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5370951118698339120")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.button(
            text="Back",
            callback_data="continue_groups",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5409284148491726576")
        )

    kb.adjust(
        2,
        2,
        2,
        2,
        1
    )

    return kb.as_markup()