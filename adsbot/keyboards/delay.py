# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delay_keyboard(is_premium: bool = False):

    kb = InlineKeyboardBuilder()

    kb.button(text="60 Sec", callback_data="delay_60", style="primary",)
    kb.button(text="5 Min", callback_data="delay_300", style="primary",)

    kb.button(text="10 Min", callback_data="delay_600", style="primary",)
    kb.button(text="20 Min", callback_data="delay_1200", style="primary",)

    kb.button(text="30 Min", callback_data="delay_1800", style="primary",)
    kb.button(text="60 Min", callback_data="delay_3600", style="primary",)

    kb.button(text="180 Min", callback_data="delay_10800", style="primary",)
    kb.button(text="24 Hours", callback_data="delay_86400", style="primary",)

    if is_premium:

        kb.button(
            text="Custom Delay",
            callback_data="delay_custom",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5370951118698339120")
        )

    else:

        kb.button(
            text="Custom Delay",
            callback_data="premium_delay",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5370951118698339120")
        )

    kb.button(
        text="Lower delay = Higher spam risk",
        callback_data="ignore",
        style="success",
        icon_custom_emoji_id=button_emoji_id("6129782440157256336")
    )

    kb.button(
        text="Back",
        callback_data="back_loop",
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
        2,
        2,
        2,
        2,
        1,
        1,
        2
    )

    return kb.as_markup()