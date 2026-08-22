# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.user_repo import UserRepository

router = Router()


@router.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    balance = user.wallet if user else 0
    referral = 0

    await callback.answer(
        f"""
💰 TGBITZ WALLET
━━━━━━━━━━━━━━━━━━━━━━━━━━
C O M I N G  S O O N
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        show_alert=True
    )