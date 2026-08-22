# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import CallbackQuery


async def info(
    callback: CallbackQuery,
    text: str,
):
    try:
        await callback.answer(
            text,
            show_alert=True
        )
    except Exception:
        pass


async def success(
    callback: CallbackQuery,
    text: str,
):
    try:
        await callback.answer(
            f"✅ SUCCESS\n\n{text}",
            show_alert=True
        )
    except Exception:
        pass


async def error(
    callback: CallbackQuery,
    text: str,
):
    try:
        await callback.answer(
            f"❌ ERROR\n\n{text}",
            show_alert=True
        )
    except Exception:
        pass


async def warning(
    callback: CallbackQuery,
    text: str,
):
    try:
        await callback.answer(
            f"⚠ WARNING\n\n{text}",
            show_alert=True
        )
    except Exception:
        pass


async def loading(
    callback: CallbackQuery,
    title: str,
    seconds: str = "1–3 seconds",
):
    try:
        await callback.answer(
            f"""
⏳ {title}

Please wait...

This usually takes {seconds}.
""",
            show_alert=True
        )
    except Exception:
        pass


async def premium(
    callback: CallbackQuery,
):
    try:
        await callback.answer(
            """
👑 PREMIUM FEATURE

This feature is available only
for Premium Members.

Upgrade to unlock all premium
features of TGBITZ Ads Bot.
""",
            show_alert=True
        )
    except Exception:
        pass


async def maintenance(
    callback: CallbackQuery,
):
    try:
        await callback.answer(
            """
🛠 UNDER MAINTENANCE

This feature is temporarily unavailable.

Please try again later.
""",
            show_alert=True
        )
    except Exception:
        pass


async def coming_soon(
    callback: CallbackQuery,
):
    try:
        await callback.answer(
            """
🚀 COMING SOON

This feature is currently under development.

Stay tuned for future updates.
""",
            show_alert=True
        )
    except Exception:
        pass


async def permission(
    callback: CallbackQuery,
):
    try:
        await callback.answer(
            """
🚫 ACCESS DENIED

You don't have permission
to perform this action.
""",
            show_alert=True
        )
    except Exception:
        pass


async def campaign_risk(
    callback: CallbackQuery,
    level: str,
    message: str,
):
    try:
        await callback.answer(
            f"{level}\n\n{message}",
            show_alert=True
        )
    except Exception:
        pass