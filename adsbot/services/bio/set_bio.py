# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated
)

from config import config


async def set_bio(
    session_string: str,
    bio: str
):

    try:

        app = Client(
            "bio_change",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=session_string,
            in_memory=True
        )

        await app.start()

        await app.update_profile(
            bio=bio
        )

        await app.stop()

        return True

    except (
        AuthKeyUnregistered,
        UserDeactivated
    ):

        return False

    except Exception as e:

     print("SET BIO ERROR:", e)

     return False