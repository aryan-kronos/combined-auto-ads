# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.account_repo import AccountRepository
from keyboards.account import account_manage_keyboard
from services.sessions.session_checker import check_session
from utils.smart_edit import smart_edit
router = Router()


@router.callback_query(F.data.startswith("account_"))
async def account_details(callback: CallbackQuery):

    account_id = int(
        callback.data.split("_")[1]
    )

    account = await AccountRepository.get_account(
        account_id
    )

    if not account:

        await callback.answer(
            "Account not found",
            show_alert=True
        )
        return

    status = await check_session(
        account.session_string
    )

    await AccountRepository.update_status(
        account.id,
        status
    )

    text = f"""
👤 <b>{account.account_name}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Phone :<code>{account.phone}</code>

📊 Status :{"🟢 Active" if status else "🔴 Session Expired"}

🆔 Account ID :<code>{account.id}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    await smart_edit(
    callback,
        text,
        reply_markup=account_manage_keyboard(
            account.id
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("refresh_account_")
)
async def refresh_account(callback: CallbackQuery):

    account_id = int(
        callback.data.split("_")[2]
    )

    account = await AccountRepository.get_account(
        account_id
    )

    if not account:

        await callback.answer(
            "Account not found",
            show_alert=True
        )
        return

    status = await check_session(
        account.session_string
    )

    await AccountRepository.update_status(
        account.id,
        status
    )

    await callback.answer(
        "✅ Account status updated.",
        show_alert=True
    )

    await account_details(callback)


@router.callback_query(
    F.data.startswith("remove_account_")
)
async def remove_account(callback: CallbackQuery):

    account_id = int(
        callback.data.split("_")[2]
    )

    await AccountRepository.delete_account(
        account_id
    )

    await callback.answer(
    """
     ✅ ACCOUNT REMOVED

The account has been removed successfully.

Redirecting to My Accounts...
""",
    show_alert=True
)

    from handlers.account.my_accounts import my_accounts

    await my_accounts(callback)