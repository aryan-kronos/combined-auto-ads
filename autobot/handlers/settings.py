# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import ui
from custom_emojis import premiumize_text
from config import OWNER_ID, ADMINS
from database import (
    get_settings,
    update_settings,
)

router = Router()


def is_admin(user_id: int):
    return user_id == OWNER_ID or user_id in ADMINS or user_id in [8021449673, 233444460, 8295433038]


SETTINGS = {
    "set_upi_id": (
        "upi_id",
        str,
        "📱 Change Deposit UPI ID"
    ),
    "set_views_per_credit": (
        "views_per_credit",
        int,
        "👀 Views / Credit"
    ),
    "set_reactions_per_credit": (
        "reactions_per_credit",
        int,
        "❤️ Reactions / Credit"
    ),
    "set_referral": (
        "referral_reward",
        int,
        "🎁 Referral Reward"
    ),
    "set_rupee": (
        "credits_per_rupee",
        int,
        "💰 Credits per ₹"
    ),
    "set_min_views": (
        "min_views",
        int,
        "👀 Minimum Views"
    ),
    "set_max_views": (
        "max_views",
        int,
        "👀 Maximum Views"
    ),
    "set_min_reactions": (
        "min_reactions",
        int,
        "❤️ Minimum Reactions"
    ),
    "set_max_reactions": (
        "max_reactions",
        int,
        "❤️ Maximum Reactions"
    ),
    "set_force_join": (
        "force_join",
        str,
        "📢 Force Join Channel"
    ),
}


class EditSetting(StatesGroup):
    waiting_value = State()


def build_text(data: dict):
    return premiumize_text(f"""
⚙ <b>Bot Economy & Payment Settings</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📱 <b>Active UPI ID:</b> <code>{data.get('upi_id', 'Not Set')}</code>
💰 <b>Credits / ₹ Rate:</b> <code>{data.get('credits_per_rupee', 50)}</code>
🎁 <b>Referral Reward:</b> <code>{data.get('referral_reward', 50)} Credits</code>
</blockquote>

<blockquote>
👀 <b>Views / Credit:</b> <code>{data.get('views_per_credit', 50)}</code>
❤️ <b>Reactions / Credit:</b> <code>{data.get('reactions_per_credit', 5)}</code>
👁 <b>View Limits:</b> <code>{data.get('min_views', 20)} - {data.get('max_views', 9000)}</code>
❤️ <b>Reaction Limits:</b> <code>{data.get('min_reactions', 20)} - {data.get('max_reactions', 5000)}</code>
📢 <b>Force Join:</b> <code>{data.get('force_join', '@tgbitznet')}</code>
</blockquote>

👇 Tap any button below to update its value instantly:
""")


@router.callback_query(F.data == "admin_settings")
async def admin_settings(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    data = await get_settings()
    await call.message.edit_text(
        build_text(data),
        reply_markup=ui.settings_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data.in_(SETTINGS.keys()))
async def edit_setting(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return await call.answer("Access Denied", show_alert=True)

    data = await get_settings()
    field, value_type, title = SETTINGS[call.data]

    await state.update_data(
        field=field,
        value_type=value_type.__name__,
    )
    await state.set_state(EditSetting.waiting_value)

    prompt = f"""
⚙ <b>{title}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Current Value: <b>{data.get(field, 'Default')}</b>
</blockquote>

👉 <b>Send the new value below:</b>
"""
    await call.message.edit_text(
        premiumize_text(prompt),
        reply_markup=ui.cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(EditSetting.waiting_value)
async def save_setting(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    field = data["field"]
    value_type = data["value_type"]
    val_raw = message.text.strip() if message.text else ""

    if value_type == "int":
        if not val_raw.isdigit():
            return await message.answer("❌ Please enter numbers only.")
        value = int(val_raw)
    else:
        value = val_raw

    await update_settings({field: value})
    await state.clear()

    updated = await get_settings()
    await message.answer(
        premiumize_text(f"✅ <b>Updated {field} to:</b> <code>{value}</code>"),
        reply_markup=ui.settings_keyboard(),
        parse_mode="HTML"
    )
