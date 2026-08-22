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
from utils.smart_edit import smart_edit
from loader import bot

router = Router()
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
ADMIN_IDS = set(config.ADMINS + [8021449673, 233444460, 8295433038])

MAINTENANCE_MODE = False

class AdminBroadcastState(StatesGroup):
    waiting_message = State()
    confirm_broadcast = State()


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
    kb.adjust(1, 2, 1)
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

    text = f"""
👑 <b>TGBITZ Ads Bot Control Panel</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
⚙️ <b>System Status:</b> {m_status}
</blockquote>

<blockquote>
👥 <b>User Telemetry:</b>
• <b>Total Users:</b> <code>{total_users:,}</code>
• 💎 <b>VIP Members:</b> <code>{premium_users:,}</code>
• 🚫 <b>Banned Users:</b> <code>{banned_users:,}</code>
</blockquote>

<blockquote>
📱 <b>Session Pool Telemetry:</b>
• <b>Total Connected Accounts:</b> <code>{total_accounts:,}</code>
• 🟢 <b>Active & Ready:</b> <code>{active_accounts:,}</code>
• 🔴 <b>Expired / Dead:</b> <code>{max(0, total_accounts - active_accounts):,}</code>
</blockquote>

<blockquote>
📢 <b>Broadcast Engine Telemetry:</b>
• <b>Total Campaigns:</b> <code>{total_campaigns:,}</code>
• 🟢 <b>Active Running:</b> <code>{running_campaigns:,}</code>
• ⏸ <b>Paused:</b> <code>{paused_campaigns:,}</code> | ✅ <b>Completed:</b> <code>{completed_campaigns:,}</code>
• 📤 <b>Delivered Messages:</b> <code>{total_sent:,}</code> | ❌ <b>Failed:</b> <code>{total_failed:,}</code>
</blockquote>

{config.BRAND_FOOTER}
"""
    if isinstance(event, CallbackQuery):
        await smart_edit(event, text, admin_keyboard())
    else:
        await event.answer(
            text=premiumize_text(text),
            reply_markup=admin_keyboard(),
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await render_admin_panel(callback)


@router.message(Command("admin"))
async def admin_panel_command(message: Message, state: FSMContext):
    await state.clear()
    await render_admin_panel(message)


# ----------------------------------------------------
# 1. RUNNING CAMPAIGNS VIEWER
# ----------------------------------------------------
@router.callback_query(F.data == "admin_running")
async def admin_running_callback(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("⛔ Access Denied.", show_alert=True)

    campaigns = []
    async for d in db.campaigns.find({"running": True}):
        c = await CampaignRepository.get_campaign(d["id"])
        if c:
            campaigns.append(c)

    kb = InlineKeyboardBuilder()

    if not campaigns:
        text = f"""
🚀 <b>Active Running Campaigns</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
✅ <b>No campaigns are currently executing in the background.</b>
All user queues are idle or completed.
</blockquote>

{config.BRAND_FOOTER}
"""
        kb.button(text="Back to Admin Panel", callback_data="admin_panel", style="primary", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
        await smart_edit(callback, text, kb.as_markup())
        return

    camp_lines = []
    for c in campaigns:
        acc = await AccountRepository.get_account(c.account_id)
        camp_lines.append(f"• 🆔 <b>Campaign #{c.id}</b> | 📱 {acc.account_name if acc else 'Acc'} | 📤 Sent: <code>{c.total_sent}</code> | ❌ Failed: <code>{c.failed_sent}</code>")
        kb.button(text=f"⏹ Stop #{c.id}", callback_data=f"admin_stop_camp_{c.id}", style="danger")

    kb.button(text="Back to Admin Panel", callback_data="admin_panel", style="primary", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
    kb.adjust(2, 2, 1)

    c_str = "\n".join(camp_lines)
    text = f"""
🚀 <b>Active Running Campaigns</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🟢 <b>Live Active Campaigns:</b> <code>{len(campaigns)}</code>
</blockquote>

<blockquote>
{c_str}
</blockquote>

{config.BRAND_FOOTER}
"""
    await smart_edit(callback, text, kb.as_markup())


@router.callback_query(F.data.startswith("admin_stop_camp_"))
async def admin_stop_camp_callback(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("⛔ Access Denied.", show_alert=True)

    camp_id = int(callback.data.split("_")[3])
    await CampaignRepository.update_status(camp_id, running=False, paused=False)
    await callback.answer(f"Campaign #{camp_id} stopped.", show_alert=True)
    await admin_running_callback(callback)


# ----------------------------------------------------
# 2. MAINTENANCE TOGGLE
# ----------------------------------------------------
@router.callback_query(F.data == "admin_maintenance")
async def admin_maintenance_callback(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("⛔ Access Denied.", show_alert=True)

    global MAINTENANCE_MODE
    MAINTENANCE_MODE = not MAINTENANCE_MODE
    state_str = "ENABLED (Users restricted)" if MAINTENANCE_MODE else "DISABLED (Bot online)"
    await callback.answer(f"Maintenance Mode {state_str}!", show_alert=True)
    await render_admin_panel(callback)


# ----------------------------------------------------
# 3. MASS BROADCAST WIZARD
# ----------------------------------------------------
@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("⛔ Access Denied.", show_alert=True)

    await state.set_state(AdminBroadcastState.waiting_message)
    text = f"""
📢 <b>Global Mass Broadcast Wizard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send or forward the message you want to broadcast to <b>all registered users</b>.
</blockquote>

<blockquote>
📎 <b>Supports:</b> Text, Photos, Videos, Documents, Voice Notes, Buttons, and Media Groups!
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(text="Cancel", callback_data="admin_panel", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
    await smart_edit(callback, text, kb.as_markup())
    await state.update_data(broadcast_prompt_id=callback.message.message_id)


@router.message(AdminBroadcastState.waiting_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    await state.update_data(
        b_chat_id=message.chat.id,
        b_msg_id=message.message_id,
    )
    await state.set_state(AdminBroadcastState.confirm_broadcast)

    total_recipients = await db.users.count_documents({})

    confirm_text = premiumize_text(f"""
⚠️ <b>Confirm Mass Broadcast Dispatch</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👥 <b>Total Target Recipients:</b> <code>{total_recipients:,}</code>
📨 <b>Message Type:</b> {message.content_type.capitalize()}
</blockquote>

<blockquote>
Are you ready to dispatch this broadcast to all users?
</blockquote>
""")

    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 Confirm & Send", callback_data="confirm_b_send", style="success", icon_custom_emoji_id=button_emoji_id("5389057356493511934"))
    kb.button(text="❌ Cancel", callback_data="admin_panel", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
    kb.adjust(1, 1)

    await message.reply(
        text=confirm_text,
        reply_markup=kb.as_markup(),
        parse_mode="HTML",
        link_preview_options=NO_PREVIEW,
    )


@router.callback_query(F.data == "confirm_b_send")
async def execute_broadcast(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("⛔ Access Denied.", show_alert=True)

    data = await state.get_data()
    b_chat_id = data.get("b_chat_id")
    b_msg_id = data.get("b_msg_id")
    await state.clear()

    if not b_chat_id or not b_msg_id:
        return await callback.answer("Broadcast data expired.", show_alert=True)

    users = [d["telegram_id"] async for d in db.users.find({}, {"telegram_id": 1})]
    total = len(users)

    progress_msg = await callback.message.edit_text(
        f"📢 <b>Broadcasting in Progress...</b>\n\nProgress: <code>0/{total}</code> (0%)",
        parse_mode="HTML"
    )

    sent = 0
    failed = 0

    for i, u_id in enumerate(users, start=1):
        try:
            await bot.copy_message(chat_id=u_id, from_chat_id=b_chat_id, message_id=b_msg_id)
            sent += 1
        except Exception:
            failed += 1

        if i % 15 == 0 or i == total:
            pct = int((i / total) * 100) if total else 100
            try:
                await progress_msg.edit_text(
                    f"📢 <b>Broadcasting in Progress...</b>\n\n"
                    f"📊 <b>Progress:</b> <code>{i}/{total}</code> (<b>{pct}%</b>)\n"
                    f"✅ <b>Delivered:</b> <code>{sent}</code> | ❌ <b>Failed:</b> <code>{failed}</code>",
                    parse_mode="HTML"
                )
            except Exception:
                pass
        await asyncio.sleep(0.05)

    report_text = premiumize_text(f"""
✅ <b>Broadcast Completed Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👥 <b>Total Users Target:</b> <code>{total:,}</code>
📤 <b>Successfully Delivered:</b> <code>{sent:,}</code>
❌ <b>Failed / Blocked:</b> <code>{failed:,}</code>
</blockquote>

{config.BRAND_FOOTER}
""")
    kb = InlineKeyboardBuilder()
    kb.button(text="Back to Admin Panel", callback_data="admin_panel", style="primary", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
    await progress_msg.edit_text(report_text, reply_markup=kb.as_markup(), parse_mode="HTML", link_preview_options=NO_PREVIEW)
