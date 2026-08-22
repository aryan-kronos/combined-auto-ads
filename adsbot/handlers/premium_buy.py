# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import io
import qrcode
from custom_emojis import button_emoji_id, premiumize_text
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    BufferedInputFile,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from handlers.premium.state import PremiumState
from database.repository.user_repo import UserRepository
from database.repository.bot_setting_repo import BotSettingRepository
from utils.smart_edit import smart_edit
from config import config

router = Router()


def generate_upi_qr(upi_id: str, upi_name: str, amount: str = "499", note: str = "Premium Membership") -> bytes:
    clean_upi = (upi_id or config.UPI_ID).strip()
    name = (upi_name or config.UPI_NAME).replace(" ", "%20")
    upi_uri = f"upi://pay?pa={clean_upi}&pn={name}&cu=INR&am={amount}&tn={note.replace(' ', '%20')}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    upi_id, upi_name = await BotSettingRepository.get_upi()

    kb = InlineKeyboardBuilder()
    kb.button(
        text="Upload Payment Screenshot",
        callback_data="premium_paid",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )
    kb.adjust(1, 1)

    qr_bytes = generate_upi_qr(upi_id=upi_id, upi_name=upi_name, amount="499")
    photo = BufferedInputFile(qr_bytes, filename="premium_qr.png")

    caption = premiumize_text(f"""
👑 <b>{config.BRAND_NAME} Lifetime Premium VIP</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💎 <b>Plan:</b> Lifetime VIP Access
💵 <b>Price:</b> <code>₹499</code> (or $6 USDT)
⚡ <b>Perks:</b> Unlimited Accounts, Zero Delays, 5 Bio Slots
</blockquote>

<blockquote>
📱 <b>UPI ID:</b> <code>{upi_id}</code> (Tap to copy)
👤 <b>Merchant:</b> <code>{upi_name}</code>
</blockquote>

<blockquote>
1️⃣ Scan QR with <b>Google Pay, PhonePe, or Paytm</b>.
2️⃣ Pay exactly <b>₹499</b>.
3️⃣ Tap <b>"Upload Payment Screenshot"</b> below and send receipt.
</blockquote>

{config.BRAND_FOOTER}
""")

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "premium_paid")
async def premium_paid(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PremiumState.waiting_screenshot)

    kb = InlineKeyboardBuilder()
    kb.button(
        text="Cancel",
        callback_data="buy_premium",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )

    text = premiumize_text(f"""
📸 <b>Upload Payment Screenshot</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send the screenshot / receipt of your successful transaction.
Our administration team will verify and activate your VIP subscription within minutes!
</blockquote>

{config.BRAND_FOOTER}
""")

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        text=text,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(PremiumState.waiting_screenshot)
async def process_screenshot(message: Message, state: FSMContext):
    if not message.photo and not message.document:
        await message.reply(premiumize_text("⚠️ <b>Please send a valid image or screenshot receipt.</b>"), parse_mode="HTML")
        return

    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else f"<a href='tg://user?id={user_id}'>User {user_id}</a>"

    caption = premiumize_text(f"""
👑 <b>NEW LIFETIME PREMIUM VIP ORDER</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>User:</b> {username}
🆔 <b>User ID:</b> <code>{user_id}</code>
💵 <b>Plan:</b> Lifetime Premium VIP (₹499)
</blockquote>

{config.BRAND_FOOTER}
""")

    kb = InlineKeyboardBuilder()
    kb.button(
        text="Approve VIP",
        callback_data=f"approve_vip_{user_id}",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Reject Order",
        callback_data=f"reject_vip_{user_id}",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(2)

    for admin_id in config.ADMINS:
        try:
            if message.photo:
                await message.bot.send_photo(
                    chat_id=admin_id,
                    photo=message.photo[-1].file_id,
                    caption=caption,
                    reply_markup=kb.as_markup(),
                    parse_mode="HTML"
                )
            elif message.document:
                await message.bot.send_document(
                    chat_id=admin_id,
                    document=message.document.file_id,
                    caption=caption,
                    reply_markup=kb.as_markup(),
                    parse_mode="HTML"
                )
        except Exception:
            pass

    await state.clear()

    home_kb = InlineKeyboardBuilder()
    home_kb.button(
        text="Home",
        callback_data="home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    await message.reply(
        premiumize_text(f"""
✅ <b>Receipt Received Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Your transaction has been submitted to the management team.
Your account will be upgraded to <b>Lifetime VIP</b> shortly after verification.
</blockquote>

{config.BRAND_FOOTER}
"""),
        reply_markup=home_kb.as_markup(),
        parse_mode="HTML"
    )
