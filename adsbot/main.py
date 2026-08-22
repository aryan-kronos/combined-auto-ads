# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio

from loader import bot, dp

from database.session import init_db, close_db
import database.models
from aiogram.types import ErrorEvent

# USER
from handlers.user.start import router as start_router


# CALLBACKS
from handlers.callback import router as callback_router


# ACCOUNTS
from handlers.account.accounts import router as account_router
from handlers.account.my_accounts import router as my_accounts_router
from handlers.account.account_manage import router as account_manage_router


# CAMPAIGNS
from handlers.campaign.create_campaign import router as campaign_router
from handlers.campaign.my_campaigns import router as my_campaigns_router
from handlers.campaign.manage_campaign import router as manage_campaign_router
from handlers.campaign.campaign_control import router as campaign_control_router

from services.campaign.campaign_worker import run_campaigns

from handlers.wallet import router as wallet_router

from handlers.dashboard.dashboard import (
    router as dashboard_router
)

from handlers.subscription import router as subscription_router
from handlers.admin.status import router as status_router
from handlers.admin.admin_panel import router as admin_panel_router
from handlers.admin.running import router as running_router
from handlers.admin.maintenance import router as maintenance_router
from handlers.admin.broadcast import router as broadcast_router
from handlers.admin.support_reply import router as support_reply_router
from handlers.admin import content_manager

from handlers.campaign.loop_campaign import router as loop_campaign_router
from handlers.campaign.pause_campaign import router as pause_router

from handlers.buy_tg_acc import router as buy_tg_router

from handlers.campaign_loop import router as campaign_loop_router
from handlers.campaign_delay import router as campaign_delay_router
from handlers.campaign_confirm import router as campaign_confirm_router

from handlers.premium_buy import router as premium_buy_router

from handlers.set_commands import set_commands
from handlers.feedback import router as feedback_router
from handlers.guide import router as guide_router
from handlers.support.support import router as support_router

from services.bio.bio_worker import run_bio_worker
from services.bio.rotation_worker import rotation_worker
from services.bio.default_bio_worker import default_bio_worker

from handlers.bio.menu import router as bio_menu_router
from handlers.bio.add import router as bio_add_router
from handlers.bio.delete import router as bio_delete_router
from handlers.bio.enable import router as bio_enable_router
from handlers.bio.disable import router as bio_disable_router
from handlers.bio.select_account import router as bio_account_router
from handlers.bio.select_bios import router as bio_bios_router
from handlers.bio.select_interval import router as bio_interval_router
from handlers.bio.time import router as bio_time_router
from handlers.bio.change_interval import (
    router as bio_change_interval_router
)
from utils.error_handler import global_error_handler

async def startup():
    await init_db()

async def global_error_handler(event: ErrorEvent):
    try:
        print("\n" + "=" * 70)
        print("❌ UNHANDLED UPDATE ERROR")
        print("=" * 70)

        print(f"Exception: {event.exception}")

        if event.update:
            print(f"Update: {event.update}")

        print("=" * 70 + "\n")

    except Exception as e:
        print(f"[ERROR HANDLER FAILED] {e}")


from config import config

async def update_bot_profile():
    """
    Updates bot description and about bio ONLY IF explicitly provided in .env.
    Never overwrites what you or your client set on @BotFather.
    """
    try:
        if config.CUSTOM_BOT_DESCRIPTION:
            desc_text = config.CUSTOM_BOT_DESCRIPTION.replace("\\n", "\n").strip()
            await bot.set_my_description(description=desc_text)
        if config.CUSTOM_BOT_ABOUT:
            short_desc = config.CUSTOM_BOT_ABOUT.replace("\\n", "\n").strip()
            await bot.set_my_short_description(short_description=short_desc)
    except Exception as e:
        print(f"Could not update bot profile: {e}")

async def main():

    await startup()
    await set_commands(bot)
    await update_bot_profile()

    dp.errors.register(global_error_handler)

    # USER
    dp.include_router(start_router)
    # USER
  

    # CAMPAIGNS
    dp.include_router(campaign_router)
    dp.include_router(campaign_loop_router)
    dp.include_router(campaign_delay_router)
    dp.include_router(campaign_confirm_router)
    dp.include_router(my_campaigns_router)
    dp.include_router(manage_campaign_router)
    dp.include_router(campaign_control_router)

    # ACCOUNTS
    dp.include_router(account_router)
    dp.include_router(my_accounts_router)
    dp.include_router(account_manage_router)

    # SUPPORT
    dp.include_router(support_router)
    dp.include_router(support_reply_router)

    # USER PAGES
    dp.include_router(callback_router)
    dp.include_router(wallet_router)
    dp.include_router(dashboard_router)
    dp.include_router(guide_router)
    dp.include_router(subscription_router)
    dp.include_router(feedback_router)

    # ADMIN
    dp.include_router(admin_panel_router)
    dp.include_router(status_router)
    dp.include_router(running_router)
    dp.include_router(maintenance_router)
    dp.include_router(broadcast_router)
    dp.include_router(content_manager.router)

    # PREMIUM
    dp.include_router(premium_buy_router)

    # BUY TG
    dp.include_router(buy_tg_router)

    # LOOP / PAUSE
    dp.include_router(loop_campaign_router)
    dp.include_router(pause_router)

    # BIO
    dp.include_router(bio_menu_router)
    dp.include_router(bio_add_router)
    dp.include_router(bio_delete_router)
    dp.include_router(bio_enable_router)
    dp.include_router(bio_disable_router)
    dp.include_router(bio_account_router)
    dp.include_router(bio_bios_router)
    dp.include_router(bio_interval_router)
    dp.include_router(bio_time_router)
    dp.include_router(bio_change_interval_router)

    # Background Workers
    asyncio.create_task(run_campaigns())
    asyncio.create_task(run_bio_worker())
    asyncio.create_task(rotation_worker())
    asyncio.create_task(default_bio_worker())

    print("=" * 50)
    print("🚀 tGBITZ ADS BOT STARTED")
    print("=" * 50)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())