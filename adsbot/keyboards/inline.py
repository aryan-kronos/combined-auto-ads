# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config


async def home_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Create Campaign",
        callback_data="create_campaign",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5389057356493511934")
    )
    kb.button(
        text="My Campaigns",
        callback_data="my_campaigns",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5409111052719767901")
    )
    kb.button(
        text="My Accounts",
        callback_data="my_accounts",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5346136537123801643")
    )
    kb.button(
        text="Buy Accounts",
        callback_data="buy_tg_acc",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6296218646284863141")
    )
    kb.button(
        text="Add Account",
        callback_data="add_account",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )
    kb.button(
        text="Auto Bio",
        callback_data="bio_home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5296447931627352804")
    )
    kb.button(
        text="Premium",
        callback_data="subscription",
        style="success",
        icon_custom_emoji_id=button_emoji_id("6276092098823327414")
    )
    kb.button(
        text="Dashboard",
        callback_data="dashboard",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6084477132254218612")
    )
    kb.button(
        text="Wallet",
        callback_data="wallet",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5417924076503062111")
    )
    kb.button(
        text="Guide",
        callback_data="guide",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5237714391293520323")
    )
    kb.button(
        text="Support",
        callback_data="support",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5866185084427572234")
    )
    kb.button(
        text="Developer (Aryan)",
        url=config.DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )

    if user_id in config.ADMINS or user_id in [8021449673, 233444460, 8295433038]:
        kb.button(
            text="Admin Panel",
            callback_data="admin_panel",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5816539591812845173")
        )
        kb.adjust(2, 2, 2, 2, 2, 1, 1)
    else:
        kb.adjust(2, 2, 2, 2, 2, 1)

    return kb.as_markup()


async def success_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.button(
        text="My Accounts",
        callback_data="my_accounts",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5346136537123801643")
    )
    kb.button(
        text="Create Campaign",
        callback_data="create_campaign",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )
    kb.adjust(1, 2)
    return kb.as_markup()


async def back_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(2)
    return kb.as_markup()


def force_join_keyboard():
    kb = InlineKeyboardBuilder()

    if config.FORCE_JOIN_1:
        kb.button(
            text="Join Official Channel",
            url=f"https://t.me/{config.FORCE_JOIN_1.replace('@','')}",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5399967660052081305")
        )

    if config.FORCE_JOIN_2:
        kb.button(
            text="Channel 2",
            url=f"https://t.me/{config.FORCE_JOIN_2.replace('@','')}",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5399967660052081305")
        )

    kb.button(
        text="I've Joined",
        callback_data="verify_join",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )
    kb.adjust(1)
    return kb.as_markup()
