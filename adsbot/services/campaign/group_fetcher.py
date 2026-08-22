# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from pyrogram import Client
from pyrogram.enums import ChatType

from config import config


async def get_joined_groups(session_string: str):

    groups = []

    seen_ids = set()
    supergroup_titles = set()

    app = Client(
        "group_fetch",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=session_string,
        in_memory=True
    )

    try:

        await app.start()

        me = await app.get_me()

        print(f"✅ Logged in as: {me.first_name} ({me.id})")

        dialogs = []

        async for dialog in app.get_dialogs():

            chat = dialog.chat

            # Ignore channels
            if chat.type == ChatType.CHANNEL:
                continue

            # Ignore everything except groups
            if chat.type not in (
                ChatType.GROUP,
                ChatType.SUPERGROUP
            ):
                continue

            dialogs.append(chat)

            if chat.type == ChatType.SUPERGROUP:
                supergroup_titles.add(
                    (chat.title or "").strip().lower()
                )

        for chat in dialogs:

            title = (chat.title or "").strip()

            # Skip basic group if upgraded supergroup exists
            if (
                chat.type == ChatType.GROUP
                and title.lower() in supergroup_titles
            ):
                continue

            if chat.id in seen_ids:
                continue

            seen_ids.add(chat.id)

            print(
                f"✅ Added: {title} | {chat.id} | {chat.type}"
            )

            groups.append(
                {
                    "id": chat.id,
                    "title": title or "Untitled",
                    "username": chat.username
                }
            )

        groups.sort(
            key=lambda g: g["title"].lower()
        )

        print(f"📂 Total Groups: {len(groups)}")

    except Exception as e:

        print("❌ Group fetch error:", e)

    finally:

        try:
            await app.stop()
        except Exception:
            pass

    return groups