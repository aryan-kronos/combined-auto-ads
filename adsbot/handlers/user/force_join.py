# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from loader import bot
from config import config
from keyboards.inline import force_join_keyboard

from database.repository.user_repo import UserRepository


async def check_force_join(bot_or_user, user_id: int = None) -> bool:
    if user_id is None:
        target_user = bot_or_user
    else:
        target_user = user_id

    if target_user in config.ADMINS or target_user in [8021449673, 233444460, 8295433038]:
        return True

    channels = [
        config.FORCE_JOIN_1,
        config.FORCE_JOIN_2,
    ]

    for channel in channels:

        if not channel:
            continue

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id,
            )

            if member.status in (
                "left",
                "kicked",
            ):
                return False

        except TelegramBadRequest as e:

            print(
                f"[Force Join] TelegramBadRequest "
                f"channel={channel} "
                f"user={user_id}: {e}"
            )

            return False

        except Exception as e:

            print(
                f"[Force Join] Unexpected error "
                f"channel={channel} "
                f"user={user_id}: {e}"
            )

            return False

    return True

async def force_join_message(message: Message):

    keyboard = force_join_keyboard()

    print("\n========== FORCE JOIN KEYBOARD ==========")
    print(keyboard.model_dump())
    print("=========================================\n")

    await message.answer(
        "<b>🚫 Join both channels first.</b>\n\n"
        "After joining press ✅ Verify .",
        reply_markup=keyboard,
    )

async def force_join_callback(callback: CallbackQuery):

    joined = await check_force_join(
        callback.from_user.id
    )

    if not joined:

        await callback.answer(
            "⚠️ Please join both required channels first, then tap '✅ Verify' again.",
            show_alert=True,
        )

        try:
            await callback.message.edit_reply_markup(
                reply_markup=force_join_keyboard()
            )
        except TelegramBadRequest:
            pass

        return

    from handlers.user.start import send_home

    user = await UserRepository.get_user(
    callback.from_user.id
)

    if user is None:
     user = await UserRepository.create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
    )

    await send_home(
        callback,
        user,
        edit=True,
    )