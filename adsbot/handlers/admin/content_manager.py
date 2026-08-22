# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import config
from database.repository.bot_setting_repo import BotSettingRepository
from utils.smart_edit import smart_edit
router = Router()


class CMSState(StatesGroup):
    waiting_content = State()


PAGES = {
    "home": "🏠 Home",
    "premium": "💎 Premium",
    "guide": "📖 Guide",
    "support": "🆘 Support",
    "wallet": "💰 Wallet",
    "statistics": "📊 Statistics",
    "maintenance": "🛠 Maintenance",
}


@router.message(Command("cms"))
async def cms(message: Message):

    if message.from_user.id not in config.ADMINS:
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Home", callback_data="cms_home")],
            [InlineKeyboardButton(text="💎 Premium", callback_data="cms_premium")],
            [InlineKeyboardButton(text="📖 Guide", callback_data="cms_guide")],
            [InlineKeyboardButton(text="🆘 Support", callback_data="cms_support")],
            [InlineKeyboardButton(text="💰 Wallet", callback_data="cms_wallet")],
            [InlineKeyboardButton(text="📊 Statistics", callback_data="cms_statistics")],
            [InlineKeyboardButton(text="🛠 Maintenance", callback_data="cms_maintenance")],
        ]
    )

    await message.answer(
        "<b>📝 Content Manager</b>\n\nSelect a page to edit.",
        reply_markup=kb
    )


@router.callback_query(
    F.data.in_(
        [
            "cms_home",
            "cms_premium",
            "cms_guide",
            "cms_support",
            "cms_wallet",
            "cms_statistics",
            "cms_maintenance",
        ]
    )
)
async def cms_page(
    callback: CallbackQuery,
    state: FSMContext
):

    page = callback.data.replace("cms_", "")

    await state.set_state(
        CMSState.waiting_content
    )

    await state.update_data(
        page=page
    )

    await smart_edit(
    callback,
        f"""
📝 <b>{PAGES[page]}</b>

Send the page text.

HTML is supported.

Only the Home page supports an image.
All other pages are text only.
"""
    )

    await callback.answer()


@router.message(CMSState.waiting_content)
async def preview_content(message: Message, state: FSMContext):

    data = await state.get_data()
    page = data["page"]

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Save",
                    callback_data="cms_save"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="cms_cancel"
                )
            ]
        ]
    )

    text = message.html_text or message.caption_html or ""

    media_type = None
    file_id = None

    if page == "home" and message.photo:
        media_type = "photo"
        file_id = message.photo[-1].file_id

        await message.answer_photo(
            file_id,
            caption=text,
            reply_markup=kb
        )
    else:
        await message.answer(
            text,
            reply_markup=kb
        )

    await state.update_data(
        text=text,
        media_type=media_type,
        file_id=file_id,
    )


@router.callback_query(F.data == "cms_cancel")
async def cms_cancel(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await smart_edit(
    callback,
        "❌ Cancelled."
    )

    await callback.answer()



@router.callback_query(F.data == "cms_save")
async def cms_save(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    await BotSettingRepository.save(
        page=data["page"],
        text=data["text"],
        media_type=data["media_type"],
        file_id=data["file_id"],
        admin_id=callback.from_user.id,
    )


    from services.cache.home_cache import set

    set(
        data["page"],
    {
        "text": data["text"],
        "media_type": data["media_type"],
        "file_id": data["file_id"],
    },
)



    await state.clear()

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.answer("✅ Saved Successfully!")

    await callback.message.answer(
        "🎉 <b>Content updated successfully.</b>\n\nThe changes are now live.",
        parse_mode="HTML"
    )