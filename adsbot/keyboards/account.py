# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder



def accounts_keyboard(accounts):

    kb = InlineKeyboardBuilder()

    for acc in accounts:
        status = "🟢" if acc.active else "🔴"

        kb.button(
            text=f"{status} {acc.account_name}",
            callback_data=f"account_{acc.id}",
        )

    kb.button(
        text="Add Account",
        callback_data="add_account",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Refresh",
        callback_data="my_accounts",
        icon_custom_emoji_id=button_emoji_id("5391079723449209646")
                )

    kb.button(
        text="Home",
        callback_data="home",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1, 2, 1)

    return kb.as_markup()


def account_details_keyboard(account_id):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Remove Account",
        callback_data=f"remove_account_{account_id}",
        style="DANGER",
        icon_custom_emoji_id=button_emoji_id("6129486856212979482")
    )

    kb.button(
        text="Back",
        callback_data="my_accounts",
        style="DANGER",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1, 1)

    return kb.as_markup()


def account_manage_keyboard(account_id):

    return account_details_keyboard(account_id)


def back_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Home",
        callback_data="home",
        style="SUCCESS",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.button(
        text="Back",
        callback_data="home",
        style="DANGER",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(2)

    return kb.as_markup()