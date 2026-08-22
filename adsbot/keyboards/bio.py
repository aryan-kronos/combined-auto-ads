# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def bio_home_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Add Bio",
        callback_data="bio_add",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Delete Bio",
        callback_data="bio_delete",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("6129486856212979482")
    )

    kb.button(
        text="Enable Rotation",
        callback_data="bio_enable",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4997002730145842282")
    
    )

    kb.button(
        text="Disable Rotation",
        callback_data="bio_disable",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5949785428843302949")
    )

    kb.button(
        text="Change Interval",
        callback_data="bio_change_interval",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5305251768475592088")
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
        1,
        1
    )

    return kb.as_markup()


def back_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    return kb.as_markup()


def no_account_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Add Account",
        callback_data="add_account",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(
        1,
        1
    )

    return kb.as_markup()


def continue_keyboard(
    buttons,
    selected
):

    kb = InlineKeyboardBuilder()

    for text, data in buttons:

        kb.button(
            text=text,
            callback_data=data
        )

    kb.button(
        text=f"Continue ({selected})",
        callback_data="bio_continue",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="Back",
        callback_data="bio_enable",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    return kb.as_markup()


def minimum_bio_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Add Bio",
        callback_data="bio_add",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    return kb.as_markup()