# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import CallbackQuery


async def loading(
    callback: CallbackQuery,
    text="⏳ Loading..."
):

    try:
        await callback.answer(text)
    except Exception:
        pass