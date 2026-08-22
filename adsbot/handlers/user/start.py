# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from config import config
from html import escape
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from keyboards.inline import home_keyboard
import time
from database.repository.user_repo import UserRepository
from services.logger.logger import send_log

from handlers.user.force_join import (
    check_force_join,
    force_join_message,
    force_join_callback,
)

from handlers.admin.maintenance import maintenance_enabled
from aiogram.fsm.context import FSMContext
from utils.smart_edit import smart_edit
from custom_emojis import premiumize_text
from database.repository.bot_setting_repo import BotSettingRepository
from database.repository.account_repo import AccountRepository

router = Router()


async def send_home(
    target,
    user,
    edit: bool = False,
):
    keyboard = await home_keyboard(user.telegram_id)
    try:
        accounts = await AccountRepository.get_accounts(user.id)
        active_accs = sum(1 for a in accounts if a.active)
    except Exception:
        active_accs = 0

    status_tag = "👑 <b>PREMIUM VIP</b> 💎" if user.is_premium else "🆓 <b>STANDARD MEMBER</b>"

    text = premiumize_text(f"""
🚀 <a href='https://t.me/{config.BOT_USERNAME}'><b>{config.BOT_NAME}</b></a> ✨

<blockquote expandable>
⚡ <b>ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜʟᴛɪ-ᴀᴄᴄᴏᴜɴᴛ ᴀᴅꜱ &amp; ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴇɴɢɪɴᴇ</b>
👑 <b>ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ʙɪᴏ ʀᴏᴛᴀᴛɪᴏɴ (ᴜᴘ ᴛᴏ 5 ʙɪᴏꜱ)</b>
💎 <b>ʜɪɢʜ-ꜱᴘᴇᴇᴅ ɢʀᴏᴜᴘ ᴍᴇꜱꜱᴀɢɪɴɢ &amp; ᴄᴀᴍᴘᴀɪɢɴꜱ</b>
🛡 <b>ꜱᴇᴄᴜʀᴇ, ꜰᴀꜱᴛ &amp; 100% ʀᴇʟɪᴀʙʟᴇ</b>
</blockquote>

<blockquote>
👤 <b>User:</b> {escape(user.first_name or 'User')}
🆔 <b>User ID:</b> <code>{user.telegram_id}</code>
👑 <b>Status:</b> {status_tag}
📱 <b>Active Sessions:</b> <code>{active_accs}</code> Accounts Linked
</blockquote>

<blockquote>
🎯 <b>ᴄᴀᴍᴘᴀɪɢɴꜱ:</b> ᴄʀᴇᴀᴛᴇ &amp; ᴍᴀɴᴀɢᴇ ᴀᴅ ʙʀᴏᴀᴅᴄᴀꜱᴛꜱ 📢
📱 <b>ᴀᴄᴄᴏᴜɴᴛꜱ:</b> ʟɪɴᴋ ᴍᴜʟᴛɪᴘʟᴇ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴇꜱꜱɪᴏɴꜱ 🔐
🔄 <b>ᴀᴜᴛᴏ ʙɪᴏ:</b> ʀᴏᴛᴀᴛᴇ ᴘʀᴏꜰɪʟᴇ ʙɪᴏꜱ ᴏɴ ꜱᴄʜᴇᴅᴜʟᴇ ✍️
</blockquote>

{config.BRAND_FOOTER}
""")

    if edit:
        try:
            await target.message.edit_text(
                text=text,
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        except Exception:
            await target.message.answer(
                text=text,
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    else:
        await target.answer(
            text=text,
            reply_markup=keyboard,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    user = await UserRepository.get_user(message.from_user.id)
    if not user:
        user = await UserRepository.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

    if not await check_force_join(message.bot, message.from_user.id):
        return await force_join_message(message)

    await send_home(message, user, edit=False)


@router.callback_query(F.data == "home")
async def home_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await UserRepository.get_user(callback.from_user.id)
    if not user:
        user = await UserRepository.create_user(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name,
        )

    await send_home(callback, user, edit=True)
    await callback.answer()
