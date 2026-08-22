# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import io
import os
import qrcode
from datetime import datetime
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    BufferedInputFile,
    InputMediaPhoto,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import ui
from custom_emojis import premiumize_text
from config import (
    DEFAULT_UPI_ID,
    DEFAULT_UPI_NAME,
    OWNER_ID,
    ADMINS,
    SUPPORT_USERNAME,
    BRAND_FOOTER,
)
from database import (
    get_balance,
    get_history,
    create_payment,
    get_settings,
)

router = Router()


def generate_upi_qr(upi_id: str = DEFAULT_UPI_ID, amount: str = None, note: str = "Deposit Credits") -> bytes:
    clean_upi = (upi_id or DEFAULT_UPI_ID).strip()
    name = (DEFAULT_UPI_NAME or "BITZ NETWORK").replace(" ", "%20")
    upi_uri = f"upi://pay?pa={clean_upi}&pn={name}&cu=INR"
    if amount:
        upi_uri += f"&am={amount}"
    if note:
        upi_uri += f"&tn={note.replace(' ', '%20')}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


class PaymentState(StatesGroup):
    waiting_custom_amount = State()
    waiting_screenshot = State()


@router.callback_query(F.data == "wallet")
async def wallet_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    balance = await get_balance(call.from_user.id)
    settings = await get_settings()
    rate = settings.get("credits_per_rupee", 50)

    text = premiumize_text(f"""
💳 <b>Your Personal Wallet</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💰 <b>Current Balance:</b> <code>{balance:,}</code> Credits
💎 <b>Exchange Rate:</b> <code>₹1 = {rate} Credits</code>
</blockquote>

<blockquote>
👉 Tap <b>Add Credits</b> below to top up your balance using instant dynamic UPI QR code!
</blockquote>

""")
    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=ui.wallet_keyboard(), parse_mode="HTML")
        else:
            await call.message.edit_text(text, reply_markup=ui.wallet_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=ui.wallet_keyboard(), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "wallet_history")
async def view_history(call: CallbackQuery):
    history = await get_history(call.from_user.id)
    if not history:
        return await call.answer("No transaction history yet.", show_alert=True)

    lines = []
    for item in history[:10]:
        t_type = item.get("type", "transaction")
        amount = item.get("amount", 0)
        desc = item.get("description", "Credit Transaction")
        sign = "+" if amount > 0 else ""
        lines.append(f"• <b>{desc}:</b> <code>{sign}{amount:,} Credits</code>")

    history_text = "\n".join(lines)
    text = premiumize_text(f"""
📜 <b>Recent Transaction History</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
{history_text}
</blockquote>
""")
    try:
        await call.message.edit_text(text, reply_markup=ui.wallet_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=ui.wallet_keyboard(), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "buy")
async def buy_packages_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    settings = await get_settings()
    rate = settings.get("credits_per_rupee", 50)

    text = premiumize_text(f"""
💰 <b>Purchase Credits Packages</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💎 <b>Rate:</b> <code>₹1 = {rate} Credits</code>
⚡ <b>Instant Verification:</b> Automated UPI QR with manual admin review
</blockquote>

👇 <b>Select a deposit package or enter custom amount:</b>
""")
    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=ui.buy_keyboard(), parse_mode="HTML")
        else:
            await call.message.edit_text(text, reply_markup=ui.buy_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=ui.buy_keyboard(), parse_mode="HTML")
    await call.answer()


async def send_payment_qr(event, state: FSMContext, amount_inr: int):
    settings = await get_settings()
    rate = settings.get("credits_per_rupee", 50)
    credits = amount_inr * rate

    await state.update_data(amount=amount_inr, credits=credits)
    active_upi = settings.get("upi_id", DEFAULT_UPI_ID)
    qr_bytes = generate_upi_qr(upi_id=active_upi, amount=str(amount_inr))
    photo = BufferedInputFile(qr_bytes, filename="upi_qr.png")

    caption = premiumize_text(f"""
💳 <b>Complete Your Payment</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🎁 <b>Credits to Receive:</b> <code>{credits:,}</code>
💵 <b>Amount to Pay:</b> <code>₹{amount_inr}</code>
</blockquote>

<blockquote>
📱 <b>UPI ID:</b> <code>{settings.get("upi_id", DEFAULT_UPI_ID)}</code> (Tap to copy)
👤 <b>Payee:</b> <code>{DEFAULT_UPI_NAME}</code>
</blockquote>

<blockquote>
1️⃣ Scan QR with <b>Google Pay, PhonePe, or Paytm</b>.
2️⃣ Pay exactly <b>₹{amount_inr}</b>.
3️⃣ Tap <b>"Upload Payment Screenshot"</b> below and send screenshot.
</blockquote>
""")

    if isinstance(event, CallbackQuery):
        await event.message.delete()
        sent = await event.message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=ui.payment_confirm_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(bot_message=sent.message_id)
        await event.answer()
    else:
        sent = await event.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=ui.payment_confirm_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(bot_message=sent.message_id)


@router.callback_query(F.data == "buy_100")
async def buy_100(call: CallbackQuery, state: FSMContext):
    await send_payment_qr(call, state, 100)


@router.callback_query(F.data == "buy_250")
async def buy_250(call: CallbackQuery, state: FSMContext):
    await send_payment_qr(call, state, 250)


@router.callback_query(F.data == "buy_500")
async def buy_500(call: CallbackQuery, state: FSMContext):
    await send_payment_qr(call, state, 500)


@router.callback_query(F.data == "buy_1000")
async def buy_1000(call: CallbackQuery, state: FSMContext):
    await send_payment_qr(call, state, 1000)


@router.callback_query(F.data == "buy_custom")
async def buy_custom(call: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.waiting_custom_amount)
    text = premiumize_text("""
💰 <b>Enter Custom Amount in Rupees (₹)</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
• Minimum: <b>₹50</b>
• Example: Send <code>150</code> or <code>750</code>
</blockquote>
""")
    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
        else:
            await call.message.edit_text(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    await call.answer()


@router.message(PaymentState.waiting_custom_amount)
async def process_custom_amount(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        return await message.answer("❌ Please send a valid numeric amount (e.g. 150).")

    amount = int(message.text.strip())
    if amount < 50:
        return await message.answer("❌ Minimum deposit is ₹50.")

    await send_payment_qr(message, state, amount)


@router.callback_query(F.data == "payment_done")
async def prompt_screenshot(call: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.waiting_screenshot)
    await state.update_data(bot_message=call.message.message_id)

    text = premiumize_text("""
📸 <b>Upload Payment Screenshot</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send the payment screenshot now from your gallery.
Our admin team will verify it and add your credits instantly!
</blockquote>
""")
    try:
        await call.message.edit_caption(caption=text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=ui.cancel_keyboard(), parse_mode="HTML")
    await call.answer()


@router.message(PaymentState.waiting_screenshot)
async def receive_payment_screenshot(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer("❌ Please send a screenshot as a photo.")

    data = await state.get_data()
    amount = data.get("amount", 100)
    credits = data.get("credits", 5000)

    payment_id = await create_payment({
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "name": message.from_user.full_name,
        "amount": amount,
        "credits": credits,
        "photo": message.photo[-1].file_id,
        "status": "pending",
        "created_at": datetime.utcnow(),
    })

    # Alert ALL admins
    admin_targets = list(set([OWNER_ID] + ADMINS + [8021449673, 233444460, 8295433038]))
    admin_caption = premiumize_text(f"""
💳 <b>New Recharge Proof Submitted</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {message.from_user.full_name} (<code>{message.from_user.id}</code>)
🔗 <b>Username:</b> @{message.from_user.username or 'None'}
💵 <b>Amount Paid:</b> <code>₹{amount}</code>
🎁 <b>Credits to Add:</b> <code>{credits:,}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Approve or Reject using buttons below:
""")

    for admin_id in admin_targets:
        try:
            await message.bot.send_photo(
                chat_id=admin_id,
                photo=message.photo[-1].file_id,
                caption=admin_caption,
                reply_markup=ui.payment_keyboard(str(payment_id)),
                parse_mode="HTML"
            )
        except Exception:
            pass

    success_text = premiumize_text(f"""
✅ <b>Payment Submitted for Verification!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💵 <b>Amount:</b> <code>₹{amount}</code>
🎁 <b>Credits:</b> <code>{credits:,}</code>
</blockquote>

<blockquote>
⏳ Your payment request has been received. Our team will approve it shortly and your balance will update automatically!
</blockquote>

👤 <b>Support:</b> @{SUPPORT_USERNAME}
""")
    await message.answer(success_text, reply_markup=ui.home_only_keyboard(), parse_mode="HTML")
    await state.clear()
