# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated
)

from config import config


async def get_bio(
    session_string: str
):

    try:

        app = Client(
            "bio_check",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=session_string,
            in_memory=True
        )

        await app.start()

        chat = await app.get_chat("me")

        await app.stop()

        return chat.bio or ""

    except (
        AuthKeyUnregistered,
        UserDeactivated
    ):

        return None

    except Exception as e:

        print("GET BIO ERROR:", e)

        return None