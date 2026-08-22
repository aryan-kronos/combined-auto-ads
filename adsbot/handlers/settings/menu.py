# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.settings import settings_keyboard
from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):

    await smart_edit(
        callback,
        """
⚙️ <b>Settings</b>

━━━━━━━━━━━━━━━━━━━━

Customize your bot experience.

Choose an option below.
""",
        settings_keyboard()
    )