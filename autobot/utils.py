from aiogram.types import LinkPreviewOptions
# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto
from custom_emojis import premiumize_text

from config import FORCE_JOIN_CHANNEL, OWNER_ID, ADMINS


async def joined(bot, user_id: int) -> bool:
    if user_id == OWNER_ID or user_id in ADMINS or user_id in [8021449673, 233444460, 8295433038]:
        return True

    try:
        member = await bot.get_chat_member(
            FORCE_JOIN_CHANNEL,
            user_id,
        )
        return member.status not in (
            "left",
            "kicked",
        )
    except TelegramBadRequest:
        return False


async def edit_or_send(
    call,
    text: str,
    keyboard=None,
):
    """
    Smart editor that automatically converts emojis to animated Telegram custom emojis!
    """
    formatted_text = premiumize_text(text)

    try:
        if call.message.photo:
            await call.message.edit_caption(
                caption=formatted_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await call.message.edit_text(
                text=formatted_text,
                reply_markup=keyboard,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    except TelegramBadRequest:
        try:
            await call.message.answer(
                formatted_text,
                reply_markup=keyboard,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        except Exception:
            pass
