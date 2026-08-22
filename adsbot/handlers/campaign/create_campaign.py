# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from database.repository.account_repo import AccountRepository
from database.repository.campaign_repo import CampaignRepository
from database.repository.target_repo import TargetRepository
from utils.progress import campaign_progress

from keyboards.campaign import (
    campaigns_keyboard,
    campaign_manage_keyboard,
)

from keyboards.target import target_keyboard
from keyboards.group import groups_keyboard


from services.campaign.group_fetcher import get_joined_groups

from services.campaign.campaign_worker import run_single_campaign
from keyboards.loop import loop_keyboard
from utils.smart_edit import smart_edit
from database.repository.user_repo import UserRepository
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline import home_keyboard
from services.sessions.session_checker import check_session
from keyboards.no_account import no_account_keyboard


router = Router()



class CampaignState(StatesGroup):

    waiting_target = State()
    waiting_group = State()
    waiting_manual_group = State()
    waiting_post = State()
    waiting_loop = State()
    waiting_delay = State()

    waiting_custom_loop = State()
    waiting_custom_repeat = State()

    waiting_confirm = State()


import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from database.repository.account_repo import AccountRepository
from database.repository.campaign_repo import CampaignRepository
from database.repository.target_repo import TargetRepository


from keyboards.campaign import (
    campaigns_keyboard,
    campaign_manage_keyboard,
)

from keyboards.target import target_keyboard
from keyboards.group import groups_keyboard


from services.campaign.group_fetcher import get_joined_groups

from services.campaign.campaign_worker import run_single_campaign
from keyboards.loop import loop_keyboard
from utils.smart_edit import smart_edit
from database.repository.user_repo import UserRepository
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline import home_keyboard
from services.sessions.session_checker import check_session
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.no_account import no_account_keyboard

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
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1, 1)

    return kb.as_markup()

router = Router()



class CampaignState(StatesGroup):

    waiting_target = State()
    waiting_group = State()
    waiting_post = State()
    waiting_loop = State()
    waiting_delay = State()

    waiting_custom_loop = State()
    waiting_custom_repeat = State()

    waiting_confirm = State()



# ==============================
# CREATE CAMPAIGN
# ==============================

@router.callback_query(F.data == "create_campaign")
async def create_campaign(callback: CallbackQuery):

    await callback.answer(
        """
⏳ Please Wait

Checking your active
Telegram accounts...

This usually takes 1–3 seconds.
""",
        show_alert=True
    )

    user = await AccountRepository.get_user(
        callback.from_user.id
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    # No account added
    if not accounts:

        await smart_edit(
            callback,
            """
❌ <b>No Active Account</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
• No Telegram account
has been added yet.

• Please add a Telegram
account to continue.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
            no_account_keyboard()
        )
        return

    valid_accounts = []
    busy_accounts = []

    for account in accounts:
        status = await check_session(account.session_string)

        await AccountRepository.update_status(account.id, status)

        if not status:
            continue

        running_campaigns = [
            c for c in await CampaignRepository.get_user_campaigns(user.id)
            if c.account_id == account.id and c.running
        ]

        if running_campaigns:
            account.running_campaign = True
            busy_accounts.append(account)
        else:
            account.running_campaign = False
            valid_accounts.append(account)

    # No active Telegram sessions
    if not valid_accounts and not busy_accounts:

        await smart_edit(
            callback,
            """
❌ <b>No Active Account</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
No active Telegram account
is available.

Possible reasons:

• All Telegram sessions
  have expired.
• Your account was logged out.
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please remove the expired
account and add a new one.
""",
            no_account_keyboard()
        )
        return

    # =====================================
    # ALL ACCOUNTS ARE BUSY
    # =====================================

    if not valid_accounts:

        kb = InlineKeyboardBuilder()

        kb.button(
            text="➕ Add Telegram Account",
            callback_data="add_account",
            icon_custom_emoji_id=button_emoji_id("5193119436621494267")
        )

        kb.button(
            text="📊 My Campaigns",
            callback_data="my_campaigns",
            icon_custom_emoji_id=button_emoji_id("5193119436621494267")
        )

        kb.button(
            text="Home",
            callback_data="home",
            style="success",
            icon_custom_emoji_id=button_emoji_id("5193119436621494267")

        )

        kb.adjust(1)

        await smart_edit(
    callback,
            """
⚠️ <b>All Accounts Busy</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
All your Telegram accounts
are already running campaigns.

Stop an existing campaign
or add another Telegram
account to continue.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
            reply_markup=kb.as_markup()
        )

        await callback.answer()
        return

    # =====================================
    # SHOW ACCOUNT LIST
    # =====================================

    from utils.progress import campaign_progress

    await smart_edit(
        callback,
        f"""
📢 <b>Create Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Step 1 / 5</b>
{campaign_progress(1)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Select Telegram Account</b>

• Choose the Telegram account
you want to use for this
campaign.
""",
        campaigns_keyboard(
            valid_accounts + busy_accounts
        )
    )
# ==============================
# SELECT ACCOUNT
# ==============================

@router.callback_query(
    F.data.startswith("campaign_account_")
)
async def select_account(
    callback: CallbackQuery,
    state: FSMContext
):

    account_id = int(
        callback.data.split("_")[2]
    )


    await state.update_data(
        account_id=account_id
    )


    await state.set_state(
        CampaignState.waiting_target
    )


    await smart_edit(
    callback,
    f"""
📢 <b>Create Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Step 2 / 5</b>
{campaign_progress(2)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Select Campaign Target</b>

• Choose where you want to send your campaign.

""",
    reply_markup=target_keyboard()
)


    await callback.answer()

@router.callback_query(F.data.startswith("campaign_busy_"))
async def campaign_busy(callback: CallbackQuery):

    await callback.answer(
        """
⚠️ Account Already In Use

•This Telegram account is already
running an active campaign.
•Stop the current campaign first
or use another Telegram account.
""",
        show_alert=True
    )



@router.callback_query(
    F.data == "target_all_groups"
)
async def all_groups(
    callback: CallbackQuery,
    state: FSMContext
):

    await callback.answer(
        """
⏳ Fetching Groups...

• Collecting all groups joined by this account.
• This usually takes 2–5 seconds.
""",
        show_alert=True
    )

    data = await state.get_data()

    account = await AccountRepository.get_account(
        data["account_id"]
    )

    if not account:

        await smart_edit(
            callback,
            "❌ Account not found."
        )

        return

    groups = await get_joined_groups(
        account.session_string
    )

    if not groups:

        await smart_edit(
            callback,
            "❌ No groups found."
        )

        return

    await state.update_data(
        target_type="all_groups",
        groups=groups,
        selected_groups=[],
        group_message_id=callback.message.message_id
    )

    await state.set_state(
        CampaignState.waiting_group
    )

    await smart_edit(
        callback,
        f"""
📢 <b>Create Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Step 3 / 5</b>
{campaign_progress(3)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 <b>Select Groups</b>

• Choose one or more groups for this campaign.
""",
        groups_keyboard(
            groups,
            []
        )
    )

    await callback.answer()


# ==============================
# SELECT ALL GROUPS
# ==============================

@router.callback_query(
    F.data == "select_all_groups"
)
async def select_all_groups(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()


    groups = data.get(
        "groups",
        []
    )


    selected = [
        group["id"]
        for group in groups
    ]


    await state.update_data(
        selected_groups=selected
    )


    await callback.message.edit_reply_markup(
        reply_markup=groups_keyboard(
            groups,
            selected
        )
    )


    await callback.answer()



@router.callback_query(
    F.data == "unselect_all_groups"
)
async def unselect_all_groups(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    await state.update_data(
        selected_groups=[]
    )

    await callback.message.edit_reply_markup(
        reply_markup=groups_keyboard(
            data["groups"],
            []
        )
    )

    await callback.answer("Selection cleared")



@router.callback_query(
    F.data.startswith("select_group_")
)
async def select_group(
    callback: CallbackQuery,
    state: FSMContext
):
    group_id = int(
        callback.data.replace("select_group_", "")
    )

    data = await state.get_data()

    selected = data.get("selected_groups", [])

    if group_id in selected:
        selected.remove(group_id)
    else:
        selected.append(group_id)

    await state.update_data(
        selected_groups=selected
    )

    await callback.message.edit_reply_markup(
        reply_markup=groups_keyboard(
            data["groups"],
            selected
        )
    )

    await callback.answer()





@router.callback_query(
    F.data == "refresh_groups"
)
async def refresh_groups(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    account = await AccountRepository.get_account(
        data["account_id"]
    )

    if not account:

        await callback.answer(
            "❌ Account not found.",
            show_alert=True
        )
        return

    await callback.answer(
    """
🔄 Refreshing...
•Fetching your latest joined groups.
•Please wait...
""",
    show_alert=True
)
    
    groups = await get_joined_groups(
        account.session_string
    )

    group_ids = {
        group["id"]
        for group in groups
    }

    selected_groups = [
        group_id
        for group_id in data.get(
            "selected_groups",
            []
        )
        if group_id in group_ids
    ]

    await state.update_data(
        groups=groups,
        selected_groups=selected_groups
    )

    await callback.message.edit_reply_markup(
        reply_markup=groups_keyboard(
            groups,
            selected_groups
        )
    )


# ==============================
# CONTINUE
# ==============================

@router.callback_query(
    F.data == "continue_groups"
)
async def continue_groups(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()


    if not data.get("selected_groups"):

        await callback.answer(
            "❌ Select at least one group.",
            show_alert=True
        )

        return



    await state.set_state(
        CampaignState.waiting_post
    )

    await smart_edit(
    
    callback,
    f"""
📢 <b>Create Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Step 4 / 5</b>
{campaign_progress(4)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 <b>Send Campaign Post</b>

Supported:
• Text only for now
"""
)


    await state.update_data(
    post_message_id=callback.message.message_id
)

    await callback.answer()




# ==============================
# RECEIVE POST
# ==============================

@router.message(CampaignState.waiting_post)
async def receive_post(
    message: Message,
    state: FSMContext
):
    post_data = message.html_text or message.text or ""

    await state.update_data(
        post_data=post_data
    )

    data = await state.get_data()

    await state.set_state(
        CampaignState.waiting_loop
    )

    await message.delete()

    await message.bot.edit_message_caption(
    chat_id=message.chat.id,
    message_id=data["post_message_id"],
    caption=f"""
📢 <b>Create Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Step 5 / 5</b>
{campaign_progress(5)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 <b>Select Campaign Loop</b>

Choose how many times this campaign should run.
""",
    reply_markup=loop_keyboard(False),
    parse_mode="HTML"
)





@router.callback_query(F.data == "loop_custom")
async def custom_loop(
    callback: CallbackQuery,
    state: FSMContext
):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    if not user.is_premium:

        await callback.answer(
            """
🔒 PREMIUM FEATURE

Custom Loop is available only for Premium Members.

✨ Premium Benefits:
• 10 Telegram Accounts
• Custom Loop
• Custom Send Delay
• Custom Bio
• Bio Rotation

Upgrade from the Premium section.
""",
            show_alert=True
        )
        return

    await state.set_state(
        CampaignState.waiting_loop
    )

    await callback.message.answer(
        """
🔁 <b>Custom Loop</b>

•Send the number of loops.
↪ Example:<code>35</code>
↪ Maximum:<code>1000</code>
"""
    )

    await callback.answer()





# ==============================
# SELECT LOOP
# ==============================

@router.callback_query(
    F.data.startswith("loop_")
)
async def select_loop(
    callback: CallbackQuery,
    state: FSMContext
):

    data = callback.data.replace(
        "loop_",
        ""
    )

    if data == "custom":
        return

    if data == "infinite":

        await state.update_data(
            loop_count=999999999,
            infinite=True
        )

    else:

        await state.update_data(
            loop_count=int(data),
            infinite=False
        )

    await state.set_state(
        CampaignState.waiting_delay
    )

    from keyboards.repeat_delay import repeat_delay_keyboard

    await smart_edit(
    callback,
        """
⏱ <b>Select Loop Interval</b>

Choose how long the bot should wait before starting the next campaign loop.
━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ <b>Risk Guide</b>

🔴 1 Minute → Very High Risk
🟠 10 Minutes → High Risk
🟡 20 Minutes → Medium Risk
🟢 30 Minutes → Low Risk
🛡 60 Minutes → Very Low Risk

━━━━━━━━━━━━━━━━━━━━━━━━━
Lower intervals may increase the chance of Telegram detecting spam activity.
Choose wisely.
""",
        reply_markup=repeat_delay_keyboard()
    )

    await state.update_data(
     post_message_id=callback.message.message_id
)

    await callback.answer()




# ==============================
# REPEAT DELAY
# ==============================

@router.callback_query(
    F.data.startswith("repeat_")
)
async def repeat_delay(
    callback: CallbackQuery,
    state: FSMContext
):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    # Premium Custom Interval
    if callback.data == "repeat_custom":

        if not user.is_premium:

            await callback.answer(
                """
🔒 PREMIUM FEATURE

Custom Loop Interval is available
only for Premium Members.
""",
                show_alert=True
            )
            return

        await state.set_state(
            CampaignState.waiting_custom_repeat
        )

        await smart_edit(
    callback,
            """
⭐ <b>Custom Loop Interval</b>
━━━━━━━━━━━━━━━━━━━━━━━━━
•Send the interval in minutes.
Examples : <code>5</code> ,<code>15</code>,<code>60</code>
"""
        )

        await callback.answer()
        return

    delay = int(
        callback.data.replace(
            "repeat_",
            ""
        )
    )

    if delay == 60:

        delay_text = "1 Minute"

        await callback.answer(
            """
🔴 VERY HIGH RISK

Telegram may detect repeated messaging as spam.

Your account has a much higher chance of getting freezed.
""",
            show_alert=True
        )

    elif delay == 600:

        delay_text = "10 Minutes"

        await callback.answer(
            """
🟠 HIGH RISK

Frequent looping increases the chance of Telegram detecting spam activity.
""",
            show_alert=True
        )

    elif delay == 1200:

        delay_text = "20 Minutes"

        await callback.answer(
            """
🟡 MEDIUM RISK

•Balanced speed and account safety.
""",
            show_alert=True
        )

    elif delay == 1800:

        delay_text = "30 Minutes"

        await callback.answer(
            """
🟢 LOW RISK

•Recommended for regular campaigns.
""",
            show_alert=True
        )

    else:

        delay_text = "60 Minutes"

        await callback.answer(
            """
🛡 VERY LOW RISK

Recommended for long-term campaigns.

Safest option.
""",
            show_alert=True
        )

    await state.update_data(
        send_delay=3,
        repeat_delay=delay
    )

    data = await state.get_data()

    infinite = data.get("infinite", False)

    loops = (
        "♾ Infinite"
        if infinite
        else str(data.get("loop_count", 0))
)

    await state.set_state(
        CampaignState.waiting_confirm
    )

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Start Campaign",
        callback_data="confirm_campaign",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5389057356493511934")
    )

    kb.button(
        text="Back",
        callback_data="back_loop_interval",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    await smart_edit(
    callback,
        f"""
🚀 <b>Campaign Ready</b>
━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 Loops :<code>{loops}</code>
⏱ Loop Interval :<code>{delay_text}</code>
⚡ Send Delay :<code>3 Seconds (Optimized)</code>
━━━━━━━━━━━━━━━━━━━━━━━━━
Ready to start your campaign?
""",
        reply_markup=kb.as_markup()
    )
    await state.update_data(
      post_message_id=callback.message.message_id
)


# ==============================
# CONTINUE (FREE = 3 SEC)
# ==============================

@router.callback_query(
    F.data == "delay_continue"
)
async def delay_continue(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        send_delay=3,
        repeat_delay=86400
    )

    data = await state.get_data()

    loops = (
        "♾ Infinite"
        if data.get("infinite")
        else data["loop_count"]
    )

    await state.set_state(
        CampaignState.waiting_confirm
    )

    await smart_edit(
    callback,
        f"""
📋 <b>Confirm Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━
📢 Account :<code>{data['account_id']}</code>
👥 Groups :<code>{len(data.get("selected_groups", []))}</code>
🔁 Loops :<code>{loops}</code>
⚡ Send Delay :<code>3 Second</code>
⏳ Repeat Delay :<code>24 Hours</code>
━━━━━━━━━━━━━━━━━━━━━━━━━
Start this campaign?
""",
        reply_markup=InlineKeyboardBuilder()
        .button(
            text="Start Campaign",
            callback_data="confirm_campaign",
            style="success",
            icon_custom_emoji_id=button_emoji_id("4987757216040747796")
        )
        .button(
            text="Cancel",
            callback_data="home",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5846210329700217522")
        )
        .adjust(1)
        .as_markup()
    )

    await callback.answer()


# ==============================
# SAVE & START CAMPAIGN
# ==============================

@router.callback_query(
    F.data == "confirm_campaign"
)
async def confirm_campaign(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    campaign = await CampaignRepository.create(
    account_id=data["account_id"],
    post_data=data["post_data"],
 )

    await CampaignRepository.update_loop(
        campaign.id,
        loops=data["loop_count"],
        infinite=data["infinite"]
    )

    await CampaignRepository.update_send_delay(
        campaign.id,
        data["send_delay"]
    )

    await CampaignRepository.update_repeat_delay(
        campaign.id,
        data["repeat_delay"]
    )

    # Save Targets
    if data.get("selected_groups"):

        groups = data["groups"]

        selected = set(
            data["selected_groups"]
        )

        for group in groups:

            if group["id"] not in selected:
                continue

            await CampaignRepository.add_target(
                campaign.id,
                group["id"],
                group.get("username"),
                group.get("title")
            )


    await CampaignRepository.update_status(
        campaign.id,
        True
    )

    asyncio.create_task(
        run_single_campaign(
            campaign.id
        )
    )

    from aiogram.utils.keyboard import InlineKeyboardBuilder

    post_message_id = data["post_message_id"]

    await state.clear()

    kb = InlineKeyboardBuilder()

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

    await smart_edit(
    callback,
    """
✅ <b>Campaign Created Successfully</b>
━━━━━━━━━━━━━━━━━━━━━━

Your campaign has been created successfully.

Thank you for using
<b>TGBITZ Ads Bot</b>.

━━━━━━━━━━━━━━━━━━━━━━
""",
    reply_markup=kb.as_markup()
)
    
    await callback.answer()



@router.message(
    CampaignState.waiting_custom_repeat
)
async def custom_repeat_interval(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "❌ Please send only numbers."
        )
        return

    minutes = int(message.text)

    if minutes < 1:

        await message.answer(
            "❌ Minimum interval is 1 minute."
        )
        return

    delay = minutes * 60

    if minutes <= 5:

        risk = "🔴 VERY HIGH RISK"

    elif minutes <= 15:

        risk = "🟠 HIGH RISK"

    elif minutes <= 30:

        risk = "🟡 MEDIUM RISK"

    elif minutes <= 60:

        risk = "🟢 LOW RISK"

    else:

        risk = "🛡 VERY LOW RISK"

    await message.answer(risk)

    await state.update_data(
        send_delay=3,
        repeat_delay=delay
    )

    data = await state.get_data()

    loops = (
        "♾ Infinite"
        if data["infinite"]
        else str(data["loop_count"])
    )

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Start Campaign",
        callback_data="confirm_campaign",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.adjust(1)

    await state.set_state(
        CampaignState.waiting_confirm
    )

    await message.answer(
        f"""
📋 <b>Confirm Campaign</b>
━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 Loops :<code>{loops}</code>
⏱ Loop Interval :<code>{minutes} Minutes</code>
⚡ Send Delay :<code>3 Seconds (Optimized)</code>

Ready to start your campaign?
""",
        reply_markup=kb.as_markup()
    )
