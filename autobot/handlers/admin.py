# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio
import time
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import ui
from custom_emojis import premiumize_text
from config import OWNER_ID, ADMINS, DEVELOPER_URL
from database import (
    users,
    channels,
    orders,
    payments,
    get_user,
    update_user,
    add_history,
    add_credits,
    get_settings,
    update_settings,
    get_payment,
    update_payment,
    get_users_paginated,
    get_channels_paginated,
    get_channels,
    get_channel,
    delete_channel,
    update_channel,
)

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in ADMINS or user_id in [8021449673, 233444460, 8295433038]


class AdminState(StatesGroup):
    waiting_start_photo = State()
    waiting_start_text = State()
    waiting_user_id_search = State()
    waiting_credit_amount = State()
    waiting_broadcast_msg = State()
    confirm_broadcast = State()


# ==============================================================================
# ADMIN MAIN MENU
# ==============================================================================
@router.callback_query(F.data == "admin")
async def admin_dashboard(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)
    await state.clear()

    total_users = await users.count_documents({})
    total_channels = await channels.count_documents({})
    total_orders = await orders.count_documents({})
    pending_payments = await payments.count_documents({"status": "pending"})

    text = premiumize_text(f"""
👑 <b>BITZ Executive Admin Dashboard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Platform Quick Telemetry:</b>
👥 <b>Total Users:</b> <code>{total_users:,}</code>
📢 <b>Monitored Channels:</b> <code>{total_channels:,}</code>
🚀 <b>Total Orders Executed:</b> <code>{total_orders:,}</code>
💳 <b>Pending Deposits:</b> <code>{pending_payments:,}</code>
</blockquote>

👇 <b>Select a management module below:</b>
""")
    await call.message.edit_text(
        text,
        reply_markup=ui.admin_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "noop")
async def noop_handler(call: CallbackQuery):
    await call.answer()


# ==============================================================================
# PAGINATED USERS MANAGER
# ==============================================================================
@router.callback_query(F.data.startswith("admin_users"))
async def admin_users_paginated(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)
    await state.clear()

    page = 1
    if "admin_users_page_" in call.data:
        try:
            page = int(call.data.split("_")[-1])
        except Exception:
            page = 1

    total_users = await users.count_documents({})
    total_pages = max(1, (total_users + 7) // 8)
    page = max(1, min(page, total_pages))

    users_list = await get_users_paginated(skip=(page - 1) * 8, limit=8)

    text = premiumize_text(f"""
👥 <b>User Management Explorer</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Total Registered Users:</b> <code>{total_users:,}</code>
📄 <b>Page:</b> <code>{page} / {total_pages}</code>
</blockquote>

👇 <b>Tap any user button to view profile & adjust credits:</b>
""")
    await call.message.edit_text(
        text,
        reply_markup=ui.paginated_users_keyboard(users_list, page, total_pages),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.startswith("admin_view_user_"))
async def admin_view_user_handler(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    parts = call.data.split("_")
    user_id = int(parts[3])
    page = int(parts[4]) if len(parts) > 4 else 1

    user = await get_user(user_id)
    if not user:
        return await call.answer("User not found.", show_alert=True)

    user_channels = await get_channels(user_id)
    created_at = user.get("created_at")
    date_str = created_at.strftime("%d %b %Y, %H:%M UTC") if created_at else "Unknown"

    text = premiumize_text(f"""
👤 <b>User Profile & Analytics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🆔 <b>User ID:</b> <code>{user_id}</code>
👤 <b>Name:</b> {user.get('name', 'User')}
🔗 <b>Username:</b> @{user.get('username') or 'None'}
💰 <b>Wallet Balance:</b> <code>{user.get('credits', 0):,}</code> Credits
📢 <b>Linked Channels:</b> <code>{len(user_channels)}</code>
🎁 <b>Referred By:</b> <code>{user.get('referred_by') or 'None'}</code>
📅 <b>Registered:</b> {date_str}
</blockquote>

👇 <b>Select an action:</b>
""")
    await call.message.edit_text(
        text,
        reply_markup=ui.user_detail_keyboard(user_id, page),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.startswith("admin_quick_add_"))
async def quick_add_credits(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    user_id = int(call.data.split("_")[-1])
    await state.update_data(target_id=user_id, action="add")
    await state.set_state(AdminState.waiting_credit_amount)

    await call.message.edit_text(
        premiumize_text(f"➕ <b>Enter amount of credits to ADD to user <code>{user_id}</code>:</b>"),
        reply_markup=ui.cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("admin_quick_deduct_"))
async def quick_deduct_credits(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    user_id = int(call.data.split("_")[-1])
    await state.update_data(target_id=user_id, action="remove")
    await state.set_state(AdminState.waiting_credit_amount)

    await call.message.edit_text(
        premiumize_text(f"➖ <b>Enter amount of credits to DEDUCT from user <code>{user_id}</code>:</b>"),
        reply_markup=ui.cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "admin_find_user")
async def find_user_prompt(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    await state.set_state(AdminState.waiting_user_id_search)
    await call.message.edit_text(
        premiumize_text("🔍 <b>Enter the Telegram User ID to search:</b>"),
        reply_markup=ui.cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminState.waiting_user_id_search)
async def process_user_search(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    if not message.text or not message.text.isdigit():
        return await message.answer("❌ Send numeric User ID only.")

    user_id = int(message.text.strip())
    user = await get_user(user_id)
    await state.clear()

    if not user:
        return await message.answer("❌ User not found in database.", reply_markup=ui.admin_keyboard())

    user_channels = await get_channels(user_id)
    text = premiumize_text(f"""
👤 <b>User Search Result</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🆔 <b>User ID:</b> <code>{user_id}</code>
👤 <b>Name:</b> {user.get('name', 'User')}
🔗 <b>Username:</b> @{user.get('username') or 'None'}
💰 <b>Wallet Balance:</b> <code>{user.get('credits', 0):,}</code> Credits
📢 <b>Linked Channels:</b> <code>{len(user_channels)}</code>
</blockquote>
""")
    await message.answer(text, reply_markup=ui.user_detail_keyboard(user_id, 1), parse_mode="HTML")


@router.message(AdminState.waiting_credit_amount)
async def process_credit_amount(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    if not message.text or not message.text.isdigit():
        return await message.answer("❌ Enter numbers only.")

    amount = int(message.text.strip())
    data = await state.get_data()
    target_id = data["target_id"]
    action = data["action"]
    await state.clear()

    if action == "add":
        await add_credits(target_id, amount)
        await add_history(target_id, amount, "Admin Credit Deposit", "admin_add")
        try:
            await message.bot.send_message(
                chat_id=target_id,
                text=premiumize_text(f"🎁 <b>Admin has added <code>+{amount:,}</code> Credits to your balance!</b>"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        await message.answer(premiumize_text(f"✅ Added <b>{amount:,}</b> credits to user <code>{target_id}</code>."), reply_markup=ui.admin_keyboard())
    else:
        user = await get_user(target_id)
        current = user.get("credits", 0)
        new_bal = max(0, current - amount)
        await update_user(target_id, {"credits": new_bal})
        await add_history(target_id, -amount, "Admin Credit Deduction", "admin_deduct")
        await message.answer(premiumize_text(f"✅ Deducted <b>{amount:,}</b> credits from user <code>{target_id}</code> (New Balance: {new_bal:,})."), reply_markup=ui.admin_keyboard())


# ==============================================================================
# PAGINATED CHANNELS MANAGER
# ==============================================================================
@router.callback_query(F.data.startswith("admin_channels"))
async def admin_channels_paginated(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)
    await state.clear()

    page = 1
    if "admin_channels_page_" in call.data:
        try:
            page = int(call.data.split("_")[-1])
        except Exception:
            page = 1

    total_channels = await channels.count_documents({})
    active_count = await channels.count_documents({"active": True})
    total_pages = max(1, (total_channels + 7) // 8)
    page = max(1, min(page, total_pages))

    channels_list = await get_channels_paginated(skip=(page - 1) * 8, limit=8)

    text = premiumize_text(f"""
📢 <b>Channel Management Explorer</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Total Registered Channels:</b> <code>{total_channels:,}</code>
🟢 <b>Active Boosted Channels:</b> <code>{active_count:,}</code>
📄 <b>Page:</b> <code>{page} / {total_pages}</code>
</blockquote>

👇 <b>Tap any channel to view telemetry & toggle status:</b>
""")
    await call.message.edit_text(
        text,
        reply_markup=ui.paginated_channels_keyboard(channels_list, page, total_pages),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.startswith("admin_view_chan_"))
async def admin_view_chan_handler(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    parts = call.data.split("_")
    chat_id = int(parts[3])
    page = int(parts[4]) if len(parts) > 4 else 1

    channel = await get_channel(chat_id)
    if not channel:
        return await call.answer("Channel not found.", show_alert=True)

    status_tag = "🟢 <b>ACTIVE & BOOSTING</b>" if channel.get("active", True) else "🔴 <b>PAUSED</b>"

    text = premiumize_text(f"""
📢 <b>Channel Details & Analytics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🆔 <b>Channel ID:</b> <code>{chat_id}</code>
📢 <b>Title:</b> {channel.get('title', 'Channel')}
🔗 <b>Username:</b> @{channel.get('username') or 'Private/None'}
👤 <b>Owner ID:</b> <code>{channel.get('owner')}</code>
⚡ <b>Status:</b> {status_tag}
</blockquote>

<blockquote>
👀 <b>Auto Views per Post:</b> <code>{channel.get('views', 0):,}</code>
❤️ <b>Auto Reactions per Post:</b> <code>{channel.get('reactions', 0):,}</code>
🚀 <b>Total Posts Boosted:</b> <code>{channel.get('posts_boosted', 0):,}</code>
💸 <b>Total Credits Used:</b> <code>{channel.get('credits_used', 0):,}</code>
</blockquote>
""")
    await call.message.edit_text(
        text,
        reply_markup=ui.channel_detail_admin_keyboard(chat_id, page),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.startswith("admin_toggle_chan_"))
async def admin_toggle_chan_handler(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    parts = call.data.split("_")
    chat_id = int(parts[3])
    page = int(parts[4]) if len(parts) > 4 else 1

    channel = await get_channel(chat_id)
    if not channel:
        return await call.answer("Channel not found.", show_alert=True)

    new_status = not channel.get("active", True)
    await update_channel(chat_id, {"active": new_status})
    await call.answer(f"Channel is now {'Active' if new_status else 'Paused'}")
    call.data = f"admin_view_chan_{chat_id}_{page}"
    await admin_view_chan_handler(call)


@router.callback_query(F.data.startswith("admin_delete_chan_"))
async def admin_delete_chan_handler(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    parts = call.data.split("_")
    chat_id = int(parts[3])
    page = int(parts[4]) if len(parts) > 4 else 1

    await delete_channel(chat_id)
    await call.answer("Channel deleted successfully.")
    call.data = f"admin_channels_page_{page}"
    await admin_channels_paginated(call, FSMContext)


# ==============================================================================
# BROADCAST WIZARD (Direct in admin.py)
# ==============================================================================
@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    await state.set_state(AdminState.waiting_broadcast_msg)
    text = premiumize_text("""
📢 <b>Mass Broadcast Engine</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👉 <b>Send or forward the message, photo, video, or post</b> that you wish to broadcast to all registered bot users:
</blockquote>
""")
    await call.message.edit_text(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    await call.answer()


@router.message(AdminState.waiting_broadcast_msg)
async def receive_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    total = await users.count_documents({})
    await state.update_data(
        from_chat_id=message.chat.id,
        broadcast_msg_id=message.message_id,
        total=total,
    )
    await state.set_state(AdminState.confirm_broadcast)

    preview_text = premiumize_text(f"""
📢 <b>Confirm Broadcast Execution</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👥 <b>Target Audience:</b> <code>{total:,} Registered Users</code>
⚡ <b>Mode:</b> Instant asynchronous copy batch
</blockquote>

⚠️ <b>Ready to broadcast the message above to all users?</b>
""")
    await message.reply(preview_text, reply_markup=ui.broadcast_confirm_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "confirm_broadcast")
async def execute_broadcast_call(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    data = await state.get_data()
    from_chat_id = data.get("from_chat_id")
    msg_id = data.get("broadcast_msg_id")

    if not from_chat_id or not msg_id:
        await state.clear()
        return await call.answer("Broadcast session expired.", show_alert=True)

    users_list = await users.find({}, {"_id": 1}).to_list(None)
    total = len(users_list)
    sent = 0
    failed = 0
    start_time = time.time()

    status_msg = await call.message.edit_text(
        premiumize_text(f"🚀 <b>Broadcasting to {total} users...</b>\n\n✅ Sent: 0 | ❌ Failed: 0"),
        parse_mode="HTML"
    )

    for idx, u in enumerate(users_list, start=1):
        try:
            await call.bot.copy_message(
                chat_id=u["_id"],
                from_chat_id=from_chat_id,
                message_id=msg_id,
            )
            sent += 1
        except Exception:
            failed += 1

        if idx % 20 == 0 or idx == total:
            try:
                await status_msg.edit_text(
                    premiumize_text(f"🚀 <b>Broadcasting in progress...</b>\n\n👥 Total: <code>{total}</code>\n✅ Delivered: <code>{sent}</code>\n❌ Failed: <code>{failed}</code>\n⏳ Remaining: <code>{total-idx}</code>"),
                    parse_mode="HTML"
                )
            except Exception:
                pass
        await asyncio.sleep(0.04)

    duration = round(time.time() - start_time, 2)
    await state.clear()
    await status_msg.edit_text(
        premiumize_text(f"""
✅ <b>Broadcast Finished!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Total Users:</b> <code>{total:,}</code>
✅ <b>Delivered:</b> <code>{sent:,}</code>
❌ <b>Failed / Blocked:</b> <code>{failed:,}</code>
⏱ <b>Time:</b> <code>{duration}s</code>
"""),
        reply_markup=ui.back_keyboard(),
        parse_mode="HTML"
    )
    await call.answer("Broadcast complete!")


# ==============================================================================
# PENDING PAYMENTS APPROVAL
# ==============================================================================
@router.callback_query(F.data == "admin_payments")
async def view_pending_payments(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    pending = await payments.find({"status": "pending"}).to_list(10)
    if not pending:
        return await call.answer("No pending payment proofs right now.", show_alert=True)

    await call.message.delete()
    for p in pending:
        caption = premiumize_text(f"""
💳 <b>Pending Recharge Request</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {p.get('name')} (<code>{p.get('user_id')}</code>)
🔗 <b>Username:</b> @{p.get('username') or 'None'}
💵 <b>Amount:</b> <code>₹{p.get('amount')}</code>
🎁 <b>Credits:</b> <code>{p.get('credits'):,}</code>
""")
        await call.message.bot.send_photo(
            chat_id=call.from_user.id,
            photo=p.get("photo"),
            caption=caption,
            reply_markup=ui.payment_keyboard(str(p["_id"])),
            parse_mode="HTML"
        )
    await call.answer()


@router.callback_query(F.data.startswith("approve_"))
async def approve_payment_call(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    payment_id = call.data.split("_")[1]
    payment = await get_payment(payment_id)
    if not payment or payment.get("status") != "pending":
        return await call.answer("Payment already processed.", show_alert=True)

    user_id = payment["user_id"]
    credits_to_add = payment["credits"]
    amount = payment["amount"]

    await update_payment(payment_id, {"status": "approved", "approved_by": call.from_user.id})
    await add_credits(user_id, credits_to_add)
    await add_history(user_id, credits_to_add, f"Recharge Deposit (₹{amount})", "deposit")

    try:
        await call.message.bot.send_message(
            chat_id=user_id,
            text=premiumize_text(f"""
🎉 <b>Payment Approved!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
💵 <b>Amount:</b> <code>₹{amount}</code>
🎁 <b>Credits Added:</b> <code>+{credits_to_add:,}</code>
💰 Your wallet balance has been credited successfully!
"""),
            parse_mode="HTML"
        )
    except Exception:
        pass

    await call.message.edit_caption(
        caption=premiumize_text(f"✅ <b>Approved by @{call.from_user.username or call.from_user.id}</b>\n🎁 Added {credits_to_add:,} credits to user <code>{user_id}</code>."),
        parse_mode="HTML"
    )
    await call.answer("Payment Approved!")


@router.callback_query(F.data.startswith("reject_"))
async def reject_payment_call(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    payment_id = call.data.split("_")[1]
    payment = await get_payment(payment_id)
    if not payment or payment.get("status") != "pending":
        return await call.answer("Payment already processed.", show_alert=True)

    user_id = payment["user_id"]
    await update_payment(payment_id, {"status": "rejected", "rejected_by": call.from_user.id})

    try:
        await call.message.bot.send_message(
            chat_id=user_id,
            text=premiumize_text("❌ <b>Your payment verification was rejected.</b>\nPlease contact support if this was an error."),
            parse_mode="HTML"
        )
    except Exception:
        pass

    await call.message.edit_caption(
        caption=premiumize_text(f"❌ <b>Rejected by @{call.from_user.username or call.from_user.id}</b>"),
        parse_mode="HTML"
    )
    await call.answer("Payment Rejected.")
