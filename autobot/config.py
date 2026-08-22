# ==============================================================================
# 🤖 BITZ AUTO BOOST BOT — CORE CONFIGURATION MODULE
# ==============================================================================
# 👨‍💻 Lead Architect & Primary Developer: Aryan (@thatonearyan)
# 🔗 Official Developer Profile: https://t.me/thatonearyan
# 🛡️ Permanent Developer Hardcoding & Dynamic Rebranding System
# ==============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- PERMANENT HARDCODED DEVELOPER CREDENTIALS ---
DEVELOPER_NAME: str = "ᴀʀʏᴀɴ"
DEVELOPER_USERNAME: str = "thatonearyan"
DEVELOPER_URL: str = "https://t.me/thatonearyan"

# ==========================================
# Telegram Credentials
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8993564937:AAFBohah5AWHfF2XzOZS5hl5Ts8GJFwqXwA")
BOT_USERNAME = os.getenv("BOT_USERNAME", "BITZAutoBot")
BOT_NAME = os.getenv("BOT_NAME", "BITZ Auto Boost Bot")
BOT_NAME_STYLED = os.getenv("BOT_NAME_STYLED", "𝐁𝐈𝐓𝐙 𝐀𝐔𝐓𝐎 𝐁𝐎𝐎𝐒𝐓 𝐁𝐎𝐓")

OWNER_ID = int(os.getenv("OWNER_ID", "8021449673"))
ADMINS = [
    int(x.strip()) for x in os.getenv("ADMINS", "8021449673,233444460,8295433038").split(",")
    if x.strip().isdigit()
]
if 8295433038 not in ADMINS:
    ADMINS.append(8295433038)
if 233444460 not in ADMINS:
    ADMINS.append(233444460)
if 8021449673 not in ADMINS:
    ADMINS.append(8021449673)

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "@tgbitznet")

# ==========================================
# Database
# ==========================================
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv("AUTO_DB_NAME") or os.getenv("DATABASE_NAME", "bitz_autoboost_bot")

# ==========================================
# CheapestSMM Panel
# ==========================================
PANEL_URL = os.getenv("PANEL_URL", "https://cheapestsmmpanels.com/api/v2")
PANEL_KEY = os.getenv("PANEL_KEY", "e5ec7c175a3589da986b7aed0f4a9b8b")

VIEW_SERVICE = int(os.getenv("VIEW_SERVICE", "344"))
REACTION_SERVICE = int(os.getenv("REACTION_SERVICE", "3960"))

# ==========================================
# Credits & Rates
# ==========================================
REFERRAL_REWARD = int(os.getenv("REFERRAL_REWARD", "50"))
CREDITS_PER_RUPEE = int(os.getenv("CREDITS_PER_RUPEE", "50"))

VIEW_COST = int(os.getenv("VIEW_COST", "1"))
REACTION_COST = int(os.getenv("REACTION_COST", "5"))

# ==========================================
# Payments & Dynamic UPI QR
# ==========================================
DEFAULT_UPI_ID = os.getenv("DEFAULT_UPI_ID", "devanshsingh2@fam")
DEFAULT_UPI_NAME = os.getenv("DEFAULT_UPI_NAME", "ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ")

# ==========================================
# Branding & Identity
# ==========================================
BRAND_NAME = os.getenv("BRAND_NAME", "BITZ")
BRAND_NAME_SMALLCAPS = os.getenv("BRAND_NAME_SMALLCAPS", "ʙɪᴛᴢ")
NETWORK_NAME = os.getenv("NETWORK_NAME", "ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ")
NETWORK_USERNAME = os.getenv("NETWORK_USERNAME", "tgbitznet")
NETWORK_URL = os.getenv("NETWORK_URL", "https://t.me/tgbitznet")

SUPPORT_NAME = os.getenv("SUPPORT_NAME", "ᴅᴇᴠᴀɴꜱʜ")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "ogbitz")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/ogbitz")
HOW_TO_USE_URL = os.getenv("HOW_TO_USE_URL", "https://t.me/tgbitznet")

CUSTOM_BOT_DESCRIPTION = os.getenv("CUSTOM_BOT_DESCRIPTION", "")
CUSTOM_BOT_ABOUT = os.getenv("CUSTOM_BOT_ABOUT", "")

# ==========================================
# Channel Limits
# ==========================================
MIN_VIEWS = 20
MAX_VIEWS = 9000

MIN_REACTIONS = 20
MAX_REACTIONS = 5000

# ==========================================
# Brand Footers
# ==========================================
POWERED_BY_TEXT = f"⚡ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <a href='{NETWORK_URL}'>{NETWORK_NAME}</a> | <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a> 👨‍💻"
BRAND_FOOTER = (
    f"✈️———— <b>{BRAND_NAME_SMALLCAPS}</b> ————✈️\n"
    f"⚡ <b>ᴘᴏᴡᴇʀᴇᴅ</b> : <a href='{NETWORK_URL}'>{NETWORK_NAME}</a> ✨\n"
    f"❤️ <b>ꜱᴜᴘᴘᴏʀᴛ</b> :- <a href='{SUPPORT_URL}'>@{SUPPORT_USERNAME}</a> 💎\n"
    f"👨‍💻 <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b> :- <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a> 👑"
)
