# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id, premiumize_text
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, LinkPreviewOptions
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import config
from database.session import db
from database.repository.campaign_repo import CampaignRepository
from database.repository.account_repo import AccountRepository
from database.repository.bot_setting_repo import BotSettingRepository
from utils.smart_edit import smart_edit
from loader import bot

router = Router()
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
ADMIN_IDS = set(config.ADMINS + [8021449673, 233444460, 8295433038])

MAINTENANCE_MODE = False

class AdminBroadcastState(StatesGroup):
    waiting_message = State()
    confirm_broadcast = State()

class AdminUpiState(StatesGroup):
    waiting_upi_details = State()


def is_maintenance():
    return MAINTENANCE_MODE


def admin_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Broadcast Message",
        callback_data="admin_broadcast",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="Running Campaigns",
        callback_data="admin_running",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5913241115489734452")
    )
    kb.button(
        text="UPI Payment Config",
        callback_data="admin_upi_settings",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5408854995359524419")
    )
    m_badge = "🔴 Disable Maintenance" if MAINTENANCE_MODE else "🟢 Enable Maintenance"
    kb.button(
        text=m_badge,
        callback_data="admin_maintenance",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5863945989127148135")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(1, 2, 1, 1)
    return kb.as_markup()


async def render_admin_panel(event):
    user_id = event.from_user.id
    if user_id not in ADMIN_IDS:
        if isinstance(event, CallbackQuery):
            await event.answer("⛔ Access Denied: Administrators only.", show_alert=True)
        return

    total_users = await db.users.count_documents({})
    premium_users = await db.users.count_documents({"is_premium": True})
    banned_users = await db.users.count_documents({"is_banned": True})

    total_accounts = await db.accounts.count_documents({})
    active_accounts = await db.accounts.count_documents({"active": True})

    total_campaigns = await db.campaigns.count_documents({})
    running_campaigns = await db.campaigns.count_documents({"running": True})
    paused_campaigns = await db.campaigns.count_documents({"paused": True})
    completed_campaigns = await db.campaigns.count_documents({"completed": True})

    total_sent = 0
    total_failed = 0
    async for d in db.campaigns.find({}, {"total_sent": 1, "failed_sent": 1}):
        total_sent += int(d.get("total_sent", 0) or 0)
        total_failed += int(d.get("failed_sent", 0) or 0)

    m_status = "🔴 <b>ACTIVE (Under Maintenance)</b>" if MAINTENANCE_MODE else "🟢 <b>OPERATIONAL (Online)</b>"

    upi_id, upi_name = await BotSettingRepository.get_upi()

    text = f"""
👑 <b>TGBITZ Ads Bot Control Panel</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
⚙️ <b>System Status:</b> {m_status}
💳 <b>Active UPI:</b> <code>{upi_id}</code> ({upi_name})
</blockquote>

<blockquote>
👥 <b>User Telemetry:</b>
• Total Users: <code>{total_users}</code>
• Premium VIP Users: <code>{premium_users}</code>
• Banned Users: <code>{banned_users}</code>
</blockquote>

<blockquote>
📱 <b>Connected Account Telemetry:</b>
• Total User Sessions: <code>{total_accounts}</code>
• Active Logged In: <code>{active_accounts}</code>
</blockquote>

<blockquote>
📢 <b>Campaign Telemetry:</b>
• Total Campaigns: <code>{total_campaigns}</code>
• 🚀 Running: <code>{running_campaigns}</code>
• ⏸️ Paused: <code>{paused_campaigns}</code>
• ✅ Completed: <code>{completed_campaigns}</code>
• 📤 Messages Dispatched: <code>{total_sent:,}</code>
• ⚠️ Failed Dispatches: <code>{total_failed:,}</code>
</blockquote>

{config.BRAND_FOOTER}
"""
    formatted = premiumize_text(text)
    kb = admin_keyboard()

    if isinstance(event, Message):
        await event.answer(formatted, reply_markup=kb, parse_mode="HTML", link_preview_options=NO_PREVIEW)
    elif isinstance(event, CallbackQuery):
        await smart_edit(event.message, formatted, reply_markup=kb, link_preview_options=NO_PREVIEW)
        await event.answer()


@router.message(Command("admin"))
async def admin_command(msg: Message, state: FSMContext):
    await state.clear()
    await render_admin_panel(msg)


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await render_admin_panel(call)


# ------------------ UPI SETTINGS ------------------ #

@router.callback_query(F.data == "admin_upi_settings")
async def admin_upi_settings(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)
    await state.clear()

    upi_id, upi_name = await BotSettingRepository.get_upi()

    text = premiumize_text(f"""
💳 <b>Admin Control — UPI Payment Settings</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📱 <b>Current Deposit UPI ID:</b>
<code>{upi_id}</code> (Tap to copy)

👤 <b>Current Merchant Name:</b>
<code>{upi_name}</code>
</blockquote>

<blockquote>
💡 <i>Any changes made here take effect immediately across all QR codes and user checkout screens without restarting the bot.</i>
</blockquote>

{config.BRAND_FOOTER}
""")
    kb = InlineKeyboardBuilder()
    kb.button(
        text="✏️ Change UPI ID / Name",
        callback_data="admin_change_upi",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5816539591812845173")
    )
    kb.button(
        text="⬅️ Back to Admin Panel",
        callback_data="admin_panel",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(1, 1)

    await smart_edit(call.message, text, reply_markup=kb.as_markup(), link_preview_options=NO_PREVIEW)
    await call.answer()


@router.callback_query(F.data == "admin_change_upi")
async def admin_change_upi(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    await state.set_state(AdminUpiState.waiting_upi_details)

    text = premiumize_text(f"""
✏️ <b>Update Payment UPI Configuration</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send the new <b>UPI ID</b> and <b>Merchant Name</b> separated by a vertical bar (<code>|</code>).

<b>Format:</b>
<code>upi_id | merchant_name</code>

<b>Example:</b>
<code>devanshsingh2@fam | BITZ NETWORK</code>
</blockquote>

<blockquote>
<i>Tap Cancel below to abort.</i>
</blockquote>

{config.BRAND_FOOTER}
""")
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Cancel", callback_data="admin_upi_settings", style="danger")

    await smart_edit(call.message, text, reply_markup=kb.as_markup(), link_preview_options=NO_PREVIEW)
    await call.answer()


@router.message(AdminUpiState.waiting_upi_details)
async def process_new_upi(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMIN_IDS:
        return

    raw = (msg.text or "").strip()
    if not raw:
        return await msg.answer("❌ Please send valid text. Example: <code>devanshsingh2@fam | BITZ NETWORK</code>", parse_mode="HTML")

    if "|" in raw:
        parts = raw.split("|", 1)
        upi_id = parts[0].strip()
        upi_name = parts[1].strip() or config.UPI_NAME
    else:
        upi_id = raw.strip()
        upi_name = config.UPI_NAME

    await BotSettingRepository.set_upi(upi_id, upi_name, msg.from_user.id)
    await state.clear()

    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Back to UPI Settings", callback_data="admin_upi_settings", style="primary")
    kb.button(text="👑 Admin Panel", callback_data="admin_panel", style="primary")
    kb.adjust(1, 1)

    await msg.answer(
        premiumize_text(f"""
✅ <b>UPI Configuration Updated Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📱 <b>New UPI ID:</b> <code>{upi_id}</code>
👤 <b>New Merchant:</b> <code>{upi_name}</code>
</blockquote>

<blockquote>
🎉 <i>All future QR codes and checkout screens will now immediately use this new UPI ID.</i>
</blockquote>

{config.BRAND_FOOTER}
"""),
        reply_markup=kb.as_markup(),
        parse_mode="HTML",
        link_preview_options=NO_PREVIEW
    )


# ------------------ MAINTENANCE MODE ------------------ #

@router.callback_query(F.data == "admin_maintenance")
async def toggle_maintenance(call: CallbackQuery):
    global MAINTENANCE_MODE
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    MAINTENANCE_MODE = not MAINTENANCE_MODE
    state_desc = "ACTIVATED" if MAINTENANCE_MODE else "DEACTIVATED"
    await call.answer(f"⚙️ Maintenance Mode has been {state_desc}!", show_alert=True)
    await render_admin_panel(call)


# ------------------ RUNNING CAMPAIGNS ------------------ #

@router.callback_query(F.data == "admin_running")
async def admin_running_campaigns(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    cursor = db.campaigns.find({"running": True})
    running_list = await cursor.to_list(length=20)

    if not running_list:
        text = premiumize_text(f"""
📢 <b>Live Running Campaigns Monitor</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
• <i>No active broadcasting campaigns are running right now.</i>
• <i>All accounts are currently idle and ready.</i>
</blockquote>

{config.BRAND_FOOTER}
""")
        kb = InlineKeyboardBuilder()
        kb.button(text="⬅️ Back to Admin Panel", callback_data="admin_panel", style="primary")
        await smart_edit(call.message, text, reply_markup=kb.as_markup(), link_preview_options=NO_PREVIEW)
        return await call.answer()

    text = f"""
📢 <b>Live Running Campaigns Monitor ({len(running_list)})</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    kb = InlineKeyboardBuilder()
    for c in running_list:
        c_id = c.get("id") or str(c.get("_id"))
        user_id = c.get("user_id")
        sent = c.get("total_sent", 0)
        text += f"""
<blockquote>
🔹 <b>Campaign #{c_id}</b>
• 👤 Owner: <code>{user_id}</code>
• 📤 Sent: <code>{sent}</code> messages
</blockquote>
"""
        kb.button(
            text=f"⏹ Stop Campaign #{c_id}",
            callback_data=f"admin_stop_camp_{c_id}",
            style="danger"
        )

    text += f"\n{config.BRAND_FOOTER}"
    kb.button(text="⬅️ Back to Admin Panel", callback_data="admin_panel", style="primary")
    kb.adjust(1)

    await smart_edit(call.message, premiumize_text(text), reply_markup=kb.as_markup(), link_preview_options=NO_PREVIEW)
    await call.answer()


@router.callback_query(F.data.startswith("admin_stop_camp_"))
async def admin_stop_campaign(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    camp_id_str = call.data.replace("admin_stop_camp_", "")
    try:
        camp_id = int(camp_id_str)
        await db.campaigns.update_one({"id": camp_id}, {"$set": {"running": False, "paused": True}})
    except Exception:
        await db.campaigns.update_one({"_id": camp_id_str}, {"$set": {"running": False, "paused": True}})

    await call.answer(f"🛑 Campaign #{camp_id_str} has been halted!", show_alert=True)
    await admin_running_campaigns(call)


# ------------------ BROADCAST WIZARD ------------------ #

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    await state.set_state(AdminBroadcastState.waiting_message)
    text = premiumize_text(f"""
📣 <b>Global Broadcast Message Wizard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send or forward the message you want to broadcast to <b>ALL bot users</b>.

Supported Content:
• 📝 Formatted Text
• 🖼️ Photos & Captions
• 🎥 Videos & Documents
• 🔘 Inline Buttons (if forwarded)
</blockquote>

<blockquote>
<i>Tap Cancel below to abort.</i>
</blockquote>

{config.BRAND_FOOTER}
""")
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Cancel Broadcast", callback_data="admin_panel", style="danger")
    await smart_edit(call.message, text, reply_markup=kb.as_markup(), link_preview_options=NO_PREVIEW)
    await call.answer()


@router.message(AdminBroadcastState.waiting_message)
async def preview_broadcast(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMIN_IDS:
        return

    await state.update_data(
        from_chat_id=msg.chat.id,
        message_id=msg.message_id
    )
    await state.set_state(AdminBroadcastState.confirm_broadcast)

    total_recipients = await db.users.count_documents({"is_banned": {"$ne": True}})

    kb = InlineKeyboardBuilder()
    kb.button(
        text=f"🚀 Dispatch to {total_recipients:,} Users",
        callback_data="admin_broadcast_confirm",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5389057356493511934")
    )
    kb.button(
        text="❌ Discard",
        callback_data="admin_panel",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(1, 1)

    await msg.reply(
        premiumize_text(f"""
⚠️ <b>Confirm Broadcast Dispatch</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Target Audience: <b>{total_recipients:,} active users</b>
</blockquote>

<blockquote>
Are you sure you want to send this broadcast immediately?
</blockquote>

{config.BRAND_FOOTER}
"""),
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_broadcast_confirm")
async def execute_broadcast(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return await call.answer("⛔ Access Denied", show_alert=True)

    data = await state.get_data()
    from_chat_id = data.get("from_chat_id")
    message_id = data.get("message_id")

    if not from_chat_id or not message_id:
        await state.clear()
        return await call.answer("Broadcast session expired. Please retry.", show_alert=True)

    await state.clear()
    await call.message.edit_text(premiumize_text("🚀 <b>Broadcasting in progress...</b>"), parse_mode="HTML")

    success = 0
    failed = 0

    async for user in db.users.find({"is_banned": {"$ne": True}}, {"user_id": 1, "id": 1, "_id": 1}):
        uid = user.get("user_id") or user.get("id") or user.get("_id")
        if not uid or not isinstance(uid, int):
            continue

        try:
            await bot.copy_message(
                chat_id=uid,
                from_chat_id=from_chat_id,
                message_id=message_id
            )
            success += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1

    kb = InlineKeyboardBuilder()
    kb.button(text="👑 Back to Admin Panel", callback_data="admin_panel", style="primary")

    await call.message.edit_text(
        premiumize_text(f"""
✅ <b>Broadcast Completed!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Delivery Results:</b>
• 🟢 Delivered: <code>{success:,}</code>
• 🔴 Failed / Blocked: <code>{failed:,}</code>
• 👥 Total Attempted: <code>{success + failed:,}</code>
</blockquote>

{config.BRAND_FOOTER}
"""),
        reply_markup=kb.as_markup(),
        parse_mode="HTML",
        link_preview_options=NO_PREVIEW
    )
