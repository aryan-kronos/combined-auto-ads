# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import config

router = Router()


class ReplyState(StatesGroup):
    waiting_reply = State()


@router.callback_query(F.data.startswith("reply_support_"))
async def reply_support(
    callback: CallbackQuery,
    state: FSMContext
):

    if callback.from_user.id not in config.ADMINS:
        return

    user_id = int(
        callback.data.split("_")[2]
    )

    await state.update_data(
        user_id=user_id
    )

    await state.set_state(
        ReplyState.waiting_reply
    )

    await callback.message.reply(
        f"""
💬 <b>Reply to User</b>

User ID:
<code>{user_id}</code>

━━━━━━━━━━━━━━━━━━━━━━

Reply with any message (text, photo, video, document, etc.).
"""
    )

    await callback.answer()


@router.message(ReplyState.waiting_reply)
async def send_reply(
    message: Message,
    state: FSMContext
):

    if message.from_user.id not in config.ADMINS:
        return

    data = await state.get_data()

    user_id = data["user_id"]

    caption = f"""
💬 <b>Reply from TGBITZ Support Team</b>
━━━━━━━━━━━━━━━━━━━━━━

Our support team has reviewed the issue you shared.

<b>Response:</b>

{message.html_text or message.caption_html or ""}

━━━━━━━━━━━━━━━━━━━━━━
If your issue is still not resolved, you can contact support again anytime.

❤️ Thank you for using <b>TGBITZ Ads Bot</b>.
"""

    try:

        if message.photo:

            await message.bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.video:

            await message.bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.document:

            await message.bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.animation:

            await message.bot.send_animation(
                chat_id=user_id,
                animation=message.animation.file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.audio:

            await message.bot.send_audio(
                chat_id=user_id,
                audio=message.audio.file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.voice:

            await message.bot.send_voice(
                chat_id=user_id,
                voice=message.voice.file_id,
                caption=caption,
                parse_mode="HTML"
            )

        elif message.video_note:

            await message.bot.send_video_note(
                chat_id=user_id,
                video_note=message.video_note.file_id,
            )

            await message.bot.send_message(
                chat_id=user_id,
                text=caption,
                parse_mode="HTML"
            )

        elif message.sticker:

            await message.bot.send_sticker(
                chat_id=user_id,
                sticker=message.sticker.file_id,
            )

            await message.bot.send_message(
                chat_id=user_id,
                text=caption,
                parse_mode="HTML"
            )

        else:

            await message.bot.send_message(
                chat_id=user_id,
                text=caption,
                parse_mode="HTML"
            )

        await message.answer(
            "✅ Reply sent successfully."
        )

    except Exception:

        await message.answer(
            "❌ Failed to send reply."
        )

    await state.clear()