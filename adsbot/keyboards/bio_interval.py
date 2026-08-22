# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder

def interval_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Continue",
        callback_data="bio_enable_confirm",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="Custom Time",
        callback_data="bio_custom_time",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5370951118698339120")
    )

    kb.button(
        text="Back",
        callback_data="bio_enable",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(
        1,
        1,
        1
    )

    return kb.as_markup()