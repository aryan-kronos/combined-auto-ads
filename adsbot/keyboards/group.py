# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


def groups_keyboard(groups, selected=None):

    kb = InlineKeyboardBuilder()

    selected = selected or []

    selected_count = 0

    for group in groups:

        group_id = group["id"]

        if group_id in selected:
            text = f"✅ {group['title']}"
            selected_count += 1
        else:
            text = f"⬜ {group['title']}"

        kb.button(
            text=text,
            callback_data=f"select_group_{group_id}",
            style="primary"
        )

    kb.button(
        text="Select All",
        callback_data="select_all_groups",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="Unselect All",
        callback_data="unselect_all_groups",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5904542823167824187")
    )

    kb.button(
        text=f"Selected ({selected_count})",
        callback_data="selected_count",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5780420810934063338")
    )

    kb.button(
        text="Refresh",
        callback_data="refresh_groups",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5391079723449209646")
    )

    kb.button(
        text="Continue",
        callback_data="continue_groups",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="Back",
        callback_data="target_all_groups",
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
        2,
        2
    )

    return kb.as_markup()