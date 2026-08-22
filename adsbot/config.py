# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
# ==============================================================================
# 🤖 TGBITZ ADS BOT — CORE CONFIGURATION MODULE
# ==============================================================================
# 👨‍💻 Lead Architect & Primary Developer: Aryan (@thatonearyan)
# 🔗 Official Developer Profile: https://t.me/thatonearyan
# 🛡️ Anti-Tamper Developer Attribution & Dynamic Rebranding System
# ==============================================================================

from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()

# --- PERMANENT HARDCODED DEVELOPER CREDENTIALS ---
# [Protected Source: Author Aryan | https://t.me/thatonearyan]
DEVELOPER_NAME: str = "ᴀʀʏᴀɴ"
DEVELOPER_USERNAME: str = "thatonearyan"
DEVELOPER_URL: str = "https://t.me/thatonearyan"


def getenv_int(name: str, default: int = 0) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


@dataclass
class Config:
    # ---------------- DEVELOPER ATTRIBUTION ---------------- #
    DEVELOPER_NAME: str = DEVELOPER_NAME
    DEVELOPER_USERNAME: str = DEVELOPER_USERNAME
    DEVELOPER_URL: str = DEVELOPER_URL

    # ---------------- TELEGRAM BOT CREDENTIALS ---------------- #
    BOT_TOKEN: str = os.getenv("ADS_BOT_TOKEN") or os.getenv("BOT_TOKEN", "8823768877:AAFN01iR9652a9W9iW5hZlC48o4dF232w5E")
    BOT_NAME: str = os.getenv("BOT_NAME", "tGBITZ Ads Bot")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "tGBITZadsbot")

    # ---------------- DATABASE CONFIGURATION ---------------- #
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    DB_NAME: str = os.getenv("DB_NAME", "tGBITZ_ads_bot")

    # ---------------- PYROGRAM CREDENTIALS ---------------- #
    API_ID: int = getenv_int("API_ID", 32914069)
    API_HASH: str = os.getenv("API_HASH", "738c57e6e04f1668f473323293067a71")

    # ---------------- ADMIN & LOGGING ---------------- #
    ADMINS: list[int] = field(
        default_factory=lambda: [
            int(x)
            for x in os.getenv("ADMINS", "8021449673,233444460,8295433038").split(",")
            if x.strip().isdigit()
        ]
    )

    LOG_CHANNEL: int = getenv_int("LOG_CHANNEL", -1003803058714)

    # ---------------- FORCE JOIN CHANNELS ---------------- #
    FORCE_JOIN_1: str = os.getenv("FORCE_JOIN_1", "@tgbitznet")
    FORCE_JOIN_2: str = os.getenv("FORCE_JOIN_2", "")

    # ---------------- BRANDING & NETWORK ---------------- #
    BRAND_NAME: str = os.getenv("BRAND_NAME", "BITZ")
    BRAND_NAME_SMALLCAPS: str = os.getenv("BRAND_NAME_SMALLCAPS", "ʙɪᴛᴢ")
    NETWORK_NAME: str = os.getenv("NETWORK_NAME", "ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ")
    NETWORK_USERNAME: str = os.getenv("NETWORK_USERNAME", "tgbitznet")
    NETWORK_URL: str = os.getenv("NETWORK_URL", "https://t.me/tgbitznet")

    # ---------------- SUPPORT & CONTACT ---------------- #
    SUPPORT_NAME: str = os.getenv("SUPPORT_NAME", "ᴅᴇᴠᴀɴꜱʜ")
    SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "ogbitz")
    SUPPORT_URL: str = os.getenv("SUPPORT_URL", "https://t.me/ogbitz")
    HOW_TO_USE_URL: str = os.getenv("HOW_TO_USE_URL", "https://t.me/tgbitznet")

    # ---------------- PAYMENTS & UPI ---------------- #
    UPI_ID: str = os.getenv("UPI_ID", "devanshsingh2@fam")
    UPI_NAME: str = os.getenv("UPI_NAME", "ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ")

    # ---------------- BOT PROFILE & TAGLINE ---------------- #
    BOT_TAGLINE: str = os.getenv("BOT_TAGLINE", "Advanced Telegram Multi-Account Ads & Bio Rotation Bot\n!ᵎ! TRUST • POWER • INNOVATION ✦")
    CUSTOM_BOT_DESCRIPTION: str = os.getenv("CUSTOM_BOT_DESCRIPTION", "")
    CUSTOM_BOT_ABOUT: str = os.getenv("CUSTOM_BOT_ABOUT", "")

    # ---------------- DEBUG MODE ---------------- #
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # ---------------- BRAND FOOTERS ---------------- #
    @property
    def POWERED_BY_TEXT(self) -> str:
        return f"⚡ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <a href='{self.NETWORK_URL}'>{self.NETWORK_NAME}</a> | <a href='{self.DEVELOPER_URL}'>{self.DEVELOPER_NAME}</a> 👨‍💻"

    @property
    def BRAND_FOOTER(self) -> str:
        return (
            f"✈️———— <b>{self.BRAND_NAME_SMALLCAPS}</b> ————✈️\n"
            f"⚡ <b>ᴘᴏᴡᴇʀᴇᴅ</b> : <a href='{self.NETWORK_URL}'>{self.NETWORK_NAME}</a> ✨\n"
            f"❤️ <b>ꜱᴜᴘᴘᴏʀᴛ</b> :- <a href='{self.SUPPORT_URL}'>@{self.SUPPORT_USERNAME}</a> 💎\n"
            f"👨‍💻 <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b> :- <a href='{self.DEVELOPER_URL}'>{self.DEVELOPER_NAME}</a> 👑"
        )


config = Config()
