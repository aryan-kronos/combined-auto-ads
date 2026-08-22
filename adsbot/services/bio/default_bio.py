# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from services.bio.set_bio import set_bio
from services.bio.get_bio import get_bio


DEFAULT_BIO = """
automated ads via • @bitzadsbot |
⚡ Telegram Advertising.
🌐 @TGBITZnet
""".strip()


async def apply_default_bio(
    session_string: str
):

    current_bio = await get_bio(
        session_string
    )

    if current_bio is None:
        return False

    if current_bio.strip() == DEFAULT_BIO:
        return True

    print("Updating default bio...")

    return await set_bio(
        session_string,
        DEFAULT_BIO
    ) 