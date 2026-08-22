# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import CallbackQuery, LinkPreviewOptions
from aiogram.exceptions import TelegramBadRequest
from custom_emojis import premiumize_text

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


async def smart_edit(
    event,
    text: str,
    reply_markup=None,
):
    formatted_text = premiumize_text(text)

    if isinstance(event, CallbackQuery):
        msg = event.message
        callback = event
    else:
        msg = event
        callback = None

    result = msg

    try:
        result = await msg.edit_text(
            text=formatted_text,
            reply_markup=reply_markup,
            link_preview_options=NO_PREVIEW,
        )
    except TelegramBadRequest as e:
        error = str(e).lower()
        if "message is not modified" in error:
            pass
        elif (
            "there is no text in the message to edit" in error
            or "message can't be edited" in error
        ):
            try:
                result = await msg.edit_caption(
                    caption=formatted_text,
                    reply_markup=reply_markup,
                )
            except TelegramBadRequest:
                result = await msg.answer(
                    text=formatted_text,
                    reply_markup=reply_markup,
                    link_preview_options=NO_PREVIEW,
                )
        elif "message to edit not found" in error:
            result = await msg.answer(
                text=formatted_text,
                reply_markup=reply_markup,
                link_preview_options=NO_PREVIEW,
            )
        else:
            raise

    if callback:
        try:
            await callback.answer()
        except Exception:
            pass

    return result
