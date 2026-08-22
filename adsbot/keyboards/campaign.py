# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.utils.keyboard import InlineKeyboardBuilder


def campaigns_keyboard(accounts):

    kb = InlineKeyboardBuilder()

    free_accounts = 0

    for acc in accounts:

        if getattr(acc, "running_campaign", False):

            kb.button(
                text=f"{acc.account_name} • Running",
                callback_data=f"campaign_busy_{acc.id}",
                 style="primary",
                icon_custom_emoji_id=button_emoji_id("5330066942755615469")
            )

        else:

            free_accounts += 1

            kb.button(
                text=f"{acc.account_name}",
                callback_data=f"campaign_account_{acc.id}",
                 style="primary",
                icon_custom_emoji_id=button_emoji_id("5346136537123801643")
            )

    kb.button(
        text=" Add Telegram Account",
        callback_data="add_account",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1)

    return kb.as_markup()


def campaign_manage_keyboard(
    campaign_id,
    running=False,
    completed=False,
    paused=False
):

    kb = InlineKeyboardBuilder()

    # ==========================
    # COMPLETED
    # ==========================

    if completed:

        kb.button(
            text="Remove Campaign",
            callback_data=f"delete_campaign_{campaign_id}",
             style="danger",
            icon_custom_emoji_id=button_emoji_id("6129486856212979482")
        )

        kb.button(
            text="My Campaigns",
            callback_data="my_campaigns",
             style="primary",
            icon_custom_emoji_id=button_emoji_id("5409111052719767901")
        )

        kb.button(
            text="Home",
            callback_data="home",
            style="success",
            icon_custom_emoji_id=button_emoji_id("5193119436621494267")
        )

        kb.adjust(1)

        return kb.as_markup()

    # ==========================
    # RUNNING / PAUSED / STOPPED
    # ==========================

    if paused:

        kb.button(
            text="Resume",
            callback_data=f"resume_campaign_{campaign_id}",
             style="success",
            icon_custom_emoji_id=button_emoji_id("6233329974200241806")
        )

        kb.button(
            text="Stop",
            callback_data=f"stop_campaign_{campaign_id}",
             style="danger",
            icon_custom_emoji_id=button_emoji_id("5974083768233760323")
        )

    elif running:

        kb.button(
            text="Pause",
            callback_data=f"pause_campaign_{campaign_id}",
             style="primary",
            icon_custom_emoji_id=button_emoji_id("5116447063432758252")
        )

        kb.button(
            text="Stop",
            callback_data=f"stop_campaign_{campaign_id}",
             style="danger",
            icon_custom_emoji_id=button_emoji_id("5974083768233760323")
        )

    else:

        kb.button(
            text=" Start",
            callback_data=f"start_campaign_{campaign_id}",
             style="success",
            icon_custom_emoji_id=button_emoji_id("6233329974200241806")
        )

    kb.button(
        text="Loop",
        callback_data=f"loop_campaign_{campaign_id}",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("5426961104305664338")
    )

    kb.button(
        text="nterval",
        callback_data=f"interval_campaign_{campaign_id}",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("5305251768475592088")
    )

    kb.button(
        text="Schedule",
        callback_data=f"schedule_campaign_{campaign_id}",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("6014861794059752708")
    )

    kb.button(
        text="Statistics",
        callback_data=f"stats_campaign_{campaign_id}",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("5190806721286657692")
    )

    kb.button(
        text="Remove campaign",
        callback_data=f"delete_campaign_{campaign_id}",
         style="danger",
        icon_custom_emoji_id=button_emoji_id("6129486856212979482")
    )

    kb.button(
        text="New Campaign",
        callback_data="create_campaign",
         style="success",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="My Campaigns",
        callback_data="my_campaigns",
         style="primary",
        icon_custom_emoji_id=button_emoji_id("5409111052719767901")
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
        1,
        2,
        1
    )

    return kb.as_markup()



def my_campaigns_keyboard(campaigns):

    kb = InlineKeyboardBuilder()

    for campaign in campaigns:
        kb.button(
            text=f"Campaign #{campaign.id}",
            callback_data=f"open_campaign_{campaign.id}",
             style="primary",
            icon_custom_emoji_id=button_emoji_id("5399967660052081305")
        )

    kb.button(
        text="New Campaign",
        callback_data="create_campaign",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1)

    return kb.as_markup()


def campaign_list_keyboard(campaigns=None):

    kb = InlineKeyboardBuilder()

    if campaigns:

        for campaign in campaigns:
            kb.button(
                text=f"Campaign #{campaign.id}",
                callback_data=f"open_campaign_{campaign.id}",
                style="primary",
                icon_custom_emoji_id=button_emoji_id("5399967660052081305")
            )

    kb.button(
        text="New Campaign",
        callback_data="create_campaign",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5287354223141342798")
    )

    kb.button(
        text="Home",
        callback_data="home",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1)

    return kb.as_markup()