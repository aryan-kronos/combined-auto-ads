# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config


def support_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Report Problem",
        callback_data="report_problem",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5420323339723881652")
    )

    kb.button(
        text="Support Lead",
        url=config.SUPPORT_URL,
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5866185084427572234")
    )

    kb.button(
        text="Developer (Aryan)",
        url=config.DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )

    kb.button(
        text="Back",
        callback_data="home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1)
    return kb.as_markup()


def submit_report_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Submit Report",
        callback_data="submit_report",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4943195336911881191")
    )

    kb.button(
        text="Cancel",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5846210329700217522")
    )

    kb.adjust(1)
    return kb.as_markup()
