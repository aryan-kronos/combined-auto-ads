# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import config
from utils.smart_edit import smart_edit

router = Router()


class FeedbackState(StatesGroup):
    waiting_feedback = State()


ratings = {
    "rate_1": "⭐",
    "rate_2": "⭐⭐",
    "rate_3": "⭐⭐⭐",
    "rate_4": "⭐⭐⭐⭐",
    "rate_5": "⭐⭐⭐⭐⭐",
}


async def show_feedback(message_or_callback):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐",
                    callback_data="rate_1",
                    style="success",
                
                ),
                ],
               [ InlineKeyboardButton(
                    text="⭐⭐",
                    callback_data="rate_2",
                    style="success",
                    
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐",
                    callback_data="rate_3",
                    style="success",
                   
                ),
                ],
               [ InlineKeyboardButton(
                    text="⭐⭐⭐⭐",
                    callback_data="rate_4",
                    style="success",
                   
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐⭐",
                    callback_data="rate_5",
                    style="success",
                   
                ),
            ]
        ]
    )

    text = """
⭐ <b>Rate TGBITZ Ads Bot</b>S
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please select your rating.
"""

    if isinstance(message_or_callback, Message):

        await message_or_callback.answer(
            text,
            reply_markup=kb
        )

    else:

        await smart_edit(
            message_or_callback,
            text,
            kb
        )


@router.message(Command("feedback"))
async def feedback_command(message: Message):

    await show_feedback(message)


@router.callback_query(F.data == "feedback")
async def feedback_callback(callback: CallbackQuery):

    await show_feedback(callback)


@router.callback_query(F.data.startswith("rate_"))
async def rating_selected(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        rating=ratings[callback.data]
    )

    await state.set_state(
        FeedbackState.waiting_feedback
    )

    await smart_edit(
        callback,
        """
✍ <b>Write your Feedback</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
You can send text, screenshots, photos,
videos, documents, or any other message.
"""
    )


@router.message(FeedbackState.waiting_feedback)
async def receive_feedback(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    rating = data["rating"]

    await message.bot.send_message(
        config.ADMINS[0],
        f"""
💡 <b>New Feedback</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ Rating : {rating}

👤 User : {message.from_user.first_name}
🆔 User ID : <code>{message.from_user.id}</code>
📎 Username : @{message.from_user.username or "None"}

⬇️ Feedback attached below.
"""
    )

    await message.bot.copy_message(
        chat_id=config.ADMINS[0],
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await message.answer(
        """
✅ <b>Thank You!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Your feedback has been received successfully.

❤️ We appreciate your support and will use your feedback to improve TGBITZ Ads Bot.
"""
    )

    await state.clear()