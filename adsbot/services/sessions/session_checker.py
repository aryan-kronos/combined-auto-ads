# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated
)

from config import config


async def check_session(session_string):

    try:

        app = Client(
            "check",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=session_string,
            in_memory=True
        )

        await app.start()
        await app.get_me()
        await app.stop()

        return True

    except (
        AuthKeyUnregistered,
        UserDeactivated
    ):
        return False

    except Exception:
        return False