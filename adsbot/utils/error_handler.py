# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import ErrorEvent


async def global_error_handler(event: ErrorEvent):

    try:

        print("\n" + "=" * 70)
        print("❌ UNHANDLED UPDATE ERROR")
        print("=" * 70)

        print(
            f"Exception: "
            f"{type(event.exception).__name__}: "
            f"{event.exception}"
        )

        if event.update:
            print(
                f"Update: {event.update}"
            )

        print("=" * 70 + "\n")

    except Exception as e:

        print(
            f"[Error Handler] Failed: {e}"
        )