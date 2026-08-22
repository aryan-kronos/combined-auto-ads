# [Engineered & Developed by Aryan | https://t.me/thatonearyan]

from config import CUSTOM_BOT_DESCRIPTION, CUSTOM_BOT_ABOUT

async def update_bot_profile():
    """
    Updates bot description and about bio ONLY IF explicitly configured in .env.
    Never overwrites what you or your client set on @BotFather.
    """
    try:
        if CUSTOM_BOT_DESCRIPTION:
            desc_text = CUSTOM_BOT_DESCRIPTION.replace("\\n", "\n").strip()
            await bot.set_my_description(description=desc_text)
        if CUSTOM_BOT_ABOUT:
            short_desc = CUSTOM_BOT_ABOUT.replace("\\n", "\n").strip()
            await bot.set_my_short_description(short_description=short_desc)
    except Exception as e:
        print(f"Could not update bot profile: {e}")

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import (
    client,
    get_settings,
)
from handlers import routers
from panel import services
from worker import worker

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))
dp = Dispatcher()


async def startup():

    # MongoDB
    await client.admin.command("ping")
    print("✅ MongoDB Connected")

    # Load/Create Settings
    settings = await get_settings()
    print("✅ Settings Loaded")

    # Telegram
    me = await bot.get_me()
    print(f"✅ @{me.username} started successfully")

    # CheapestSMM API
    try:

        data = await services()

        print("✅ CheapestSMM Connected")
        print(f"📦 Total Services: {len(data)}")

        view = next(
            (
                x for x in data
                if int(x["service"])
                == settings["view_service"]
            ),
            None,
        )

        reaction = next(
            (
                x for x in data
                if int(x["service"])
                == settings["reaction_service"]
            ),
            None,
        )

        if view:
            print(f"✅ View Service: {view['name']}")
        else:
            print(
                f"❌ View Service ({settings['view_service']}) Not Found"
            )

        if reaction:
            print(f"✅ Reaction Service: {reaction['name']}")
        else:
            print(
                f"❌ Reaction Service ({settings['reaction_service']}) Not Found"
            )

    except Exception as e:

        print("❌ CheapestSMM Connection Failed")
        print(e)


async def worker_loop():

    while True:

        try:
            # Pass bot to worker
            await worker(bot)

        except Exception as e:

            print(f"❌ Worker crashed: {e}")

            await asyncio.sleep(5)


async def main():

    await startup()
    await update_bot_profile()

    for router in routers:
        dp.include_router(router)

    # Start worker in background
    asyncio.create_task(worker_loop())

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    asyncio.run(main())