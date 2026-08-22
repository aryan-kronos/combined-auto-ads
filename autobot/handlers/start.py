from aiogram.types import LinkPreviewOptions
from custom_emojis import premiumize_text
# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InputMediaPhoto,
)
from utils import edit_or_send
import ui

from config import (
    REFERRAL_REWARD,
    BOT_NAME_STYLED,
    BOT_USERNAME,
    NETWORK_NAME,
    BRAND_FOOTER,
    OWNER_ID,
    ADMINS,
)
from database import (
    get_user,
    create_user,
    update_user,
    add_credits,
    add_history,
    get_bot_settings,
    get_balance,
)
from logger import log
from utils import joined

router = Router()


async def reward_referral(bot, user_id: int, user, event_date):
    if user.get("joined"):
        return

    await update_user(
        user_id,
        {
            "joined": True,
            "last_active": event_date,
        }
    )

    ref = user.get("referred_by")
    if not ref or ref == user_id or user.get("ref_rewarded"):
        return

    ref_user = await get_user(ref)
    if not ref_user:
        return

    await add_credits(ref, REFERRAL_REWARD)
    await add_history(
        ref,
        REFERRAL_REWARD,
        f"Referral Reward (User {user_id})",
        "referral",
    )
    await add_credits(user_id, REFERRAL_REWARD)
    await add_history(
        user_id,
        REFERRAL_REWARD,
        f"Joined via Referral ({ref})",
        "referral",
    )
    await log(
        bot,
        "💰 Referral Credits Added",
        f"""
-------------------------------------------------------
👤 Referrer: <code>{ref}</code>
👤 New User: <code>{user_id}</code>
🎁 Reward: {REFERRAL_REWARD} Credits Each
-------------------------------------------------------
"""
    )

    await update_user(user_id, {"ref_rewarded": True})

    try:
        await bot.send_message(
            ref,
            f"🎉 You earned <b>{REFERRAL_REWARD} Credits</b> from a successful referral!",
            parse_mode="HTML"
        )
    except:
        pass

    try:
        await bot.send_message(
            user_id,
            f"🎉 You received <b>{REFERRAL_REWARD} Credits</b> for joining through a referral!",
            parse_mode="HTML"
        )
    except:
        pass


@router.message(CommandStart())
async def start(message: Message):
    user = await get_user(message.from_user.id)

    if not user:
        ref = None
        args = message.text.split(maxsplit=1)
        if len(args) > 1:
            try:
                ref = int(args[1])
            except ValueError:
                pass

        if ref == message.from_user.id:
            ref = None

        await create_user(
            {
                "_id": message.from_user.id,
                "name": message.from_user.full_name,
                "username": message.from_user.username,
                "credits": 0,
                "channels": [],
                "referred_by": ref,
                "ref_rewarded": False,
                "joined": False,
                "created_at": message.date,
                "last_active": message.date,
            }
        )
        user = await get_user(message.from_user.id)

        await log(
            message.bot,
            "🆕 New User",
            f"""
👤 <b>{message.from_user.full_name}</b>
🆔 <code>{message.from_user.id}</code>
👤 @{message.from_user.username or 'None'}
🔗 Referrer: <code>{ref or 'None'}</code>
"""
        )

    # Force Join Check
    if not await joined(message.bot, message.from_user.id):
        return await message.answer(
            "🚫 <b>Access Denied: You must join our official channel to continue.</b>",
            reply_markup=ui.force_join_keyboard(),
            parse_mode="HTML",
        )

    # Referral Reward
    await reward_referral(
        message.bot,
        message.from_user.id,
        user,
        message.date,
    )

    # Rich Welcome Card
    credits = await get_balance(message.from_user.id)
    welcome_text = f"""
🎁 <a href='https://t.me/{BOT_USERNAME}'><b>{BOT_NAME_STYLED}</b></a> 🎉

<blockquote expandable>
✨ <b>ꜰᴜʟʟʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴄʜᴀɴɴᴇʟ ʙᴏᴏꜱᴛᴇʀ</b> ✔️
⚡ <b>ɪɴꜱᴛᴀɴᴛ ᴘᴏꜱᴛ ᴠɪᴇᴡꜱ &amp; ʀᴇᴀᴄᴛɪᴏɴꜱ</b> ✔️
💎 <b>ʀᴇᴀʟ-ᴛɪᴍᴇ ꜱᴍᴍ ᴀᴘɪ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ</b> ✔️
🛡 <b>ꜱᴇᴄᴜʀᴇ, ꜰᴀꜱᴛ &amp; ʀᴇʟɪᴀʙʟᴇ</b> ✔️
</blockquote>

<blockquote>
👤 <b>User:</b> {message.from_user.full_name}
🆔 <b>User ID:</b> <code>{message.from_user.id}</code>
💰 <b>Your Credits:</b> <code>{credits}</code>
</blockquote>

<blockquote>
📢 <b>ᴍʏ ᴄʜᴀɴɴᴇʟꜱ:</b> ᴀᴅᴅ &amp; ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ⭐
💳 <b>ᴡᴀʟʟᴇᴛ:</b> ʙᴜʏ ᴄʀᴇᴅɪᴛꜱ ᴠɪᴀ ɪɴꜱᴛᴀɴᴛ ᴜᴘɪ Qʀ 💰
👥 <b>ʀᴇꜰᴇʀ &amp; ᴇᴀʀɴ:</b> ɪɴᴠɪᴛᴇ ꜰʀɪᴇɴᴅꜱ &amp; ɢᴇᴛ ꜰʀᴇᴇ ᴄʀᴇᴅɪᴛꜱ 🎁
</blockquote>

{BRAND_FOOTER}
"""
    await message.answer(
        premiumize_text(welcome_text),
        reply_markup=ui.home_keyboard(message.from_user.id),
        parse_mode="HTML",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@router.callback_query(F.data == "home")
async def home(call: CallbackQuery):
    credits = await get_balance(call.from_user.id)
    welcome_text = f"""
🎁 <a href='https://t.me/{BOT_USERNAME}'><b>{BOT_NAME_STYLED}</b></a> 🎉

<blockquote expandable>
✨ <b>ꜰᴜʟʟʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴄʜᴀɴɴᴇʟ ʙᴏᴏꜱᴛᴇʀ</b> ✔️
⚡ <b>ɪɴꜱᴛᴀɴᴛ ᴘᴏꜱᴛ ᴠɪᴇᴡꜱ &amp; ʀᴇᴀᴄᴛɪᴏɴꜱ</b> ✔️
💎 <b>ʀᴇᴀʟ-ᴛɪᴍᴇ ꜱᴍᴍ ᴀᴘɪ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ</b> ✔️
🛡 <b>ꜱᴇᴄᴜʀᴇ, ꜰᴀꜱᴛ &amp; ʀᴇʟɪᴀʙʟᴇ</b> ✔️
</blockquote>

<blockquote>
👤 <b>User:</b> {call.from_user.full_name}
🆔 <b>User ID:</b> <code>{call.from_user.id}</code>
💰 <b>Your Credits:</b> <code>{credits}</code>
</blockquote>

<blockquote>
📢 <b>ᴍʏ ᴄʜᴀɴɴᴇʟꜱ:</b> ᴀᴅᴅ &amp; ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ⭐
💳 <b>ᴡᴀʟʟᴇᴛ:</b> ʙᴜʏ ᴄʀᴇᴅɪᴛꜱ ᴠɪᴀ ɪɴꜱᴛᴀɴᴛ ᴜᴘɪ Qʀ 💰
👥 <b>ʀᴇꜰᴇʀ &amp; ᴇᴀʀɴ:</b> ɪɴᴠɪᴛᴇ ꜰʀɪᴇɴᴅꜱ &amp; ɢᴇᴛ ꜰʀᴇᴇ ᴄʀᴇᴅɪᴛꜱ 🎁
</blockquote>

{BRAND_FOOTER}
"""
    await edit_or_send(
        call,
        welcome_text,
        ui.home_keyboard(call.from_user.id),
    )


@router.callback_query(F.data == "guide")
async def show_guide(call: CallbackQuery):
    guide_text = f"""
📖 <b>How to Use {BOT_NAME_STYLED}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
1️⃣ <b>Step 1: Add Your Channel</b> 📢
• Add <b>@{BOT_USERNAME}</b> as an <b>Admin</b> to your channel with <i>"Post Messages"</i> permission.
• Tap <b>My Channels</b> ➔ <b>Add New Channel</b> and send your channel link or forward any post.
</blockquote>

<blockquote>
2️⃣ <b>Step 2: Configure Views & Reactions</b> 👀
• Select your channel from <b>My Channels</b>.
• Set your desired <b>Auto Views</b> (e.g. 100 views) and <b>Auto Reactions</b> (e.g. 20 mix reactions).
• Make sure the channel is set to 🟢 <b>Active</b>.
</blockquote>

<blockquote>
3️⃣ <b>Step 3: Top-up Wallet Credits</b> 💳
• Go to <b>Wallet</b> ➔ <b>Add Credits</b>.
• Choose a deposit package (e.g. ₹100 = 5,000 Credits) or enter custom amount.
• Scan the dynamic UPI QR code with GPay, PhonePe, or Paytm and upload screenshot.
</blockquote>

<blockquote>
4️⃣ <b>Step 4: Automated 24/7 Boost Delivery</b> 🚀
• Whenever you publish a new post in your channel, our engine automatically boosts your post with Views and Reactions in seconds!
</blockquote>

<blockquote>
5️⃣ <b>Step 5: Refer & Earn Free Credits</b> 🎁
• Share your referral link from <b>Refer & Earn</b> with other creators.
• Receive <b>+{REFERRAL_REWARD} free credits</b> for every friend who joins!
</blockquote>

{BRAND_FOOTER}
"""
    await edit_or_send(
        call,
        guide_text,
        ui.guide_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "inbot_guide")
async def show_inbot_guide(call: CallbackQuery):
    await show_guide(call)

@router.callback_query(F.data == "support")
async def show_support(call: CallbackQuery):
    from config import SUPPORT_USERNAME, SUPPORT_URL, DEVELOPER_URL, DEVELOPER_NAME, NETWORK_URL
    support_text = f"""
🛟 <b>Customer Support & Assistance</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Need help adding your channel, purchasing credits, or configuring automated boosting?
Our team is available 24/7 to assist you!
</blockquote>

<blockquote>
👤 <b>Support Lead:</b> <a href='{SUPPORT_URL}'>@{SUPPORT_USERNAME}</a>
⚡ <b>Official Network:</b> <a href='{NETWORK_URL}'>{NETWORK_NAME}</a>
👨‍💻 <b>Lead Developer:</b> <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a>
</blockquote>

"""
    await edit_or_send(
        call,
        support_text,
        ui.support_keyboard(),
    )
    await call.answer()

@router.callback_query(F.data == "inbot_guide")
async def show_inbot_guide(call: CallbackQuery):
    from config import REFERRAL_REWARD
    guide_text = f"""
📖 <b>Comprehensive Bot User Guide & Instructions</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote expandable>
🔹 <b>Step 1: Adding Your Channel</b>
1️⃣ Add <b>@{BOT_USERNAME}</b> as an <b>Admin</b> to your Telegram channel with <i>"Post Messages"</i> permission.
2️⃣ Open <b>My Channels</b> ➔ tap <b>Add New Channel</b>.
3️⃣ Send your channel public <code>@username</code> or forward any message from your channel.

🔹 <b>Step 2: Configuring Views & Reactions</b>
1️⃣ In <b>My Channels</b>, tap on your added channel.
2️⃣ Tap <b>Set Auto Views</b> (e.g. 100 views).
3️⃣ Tap <b>Set Auto Reactions</b> (e.g. 20 mix positive reactions).
4️⃣ Make sure the channel toggle is set to 🟢 <b>Enabled</b>.

🔹 <b>Step 3: Purchasing Credits via UPI</b>
1️⃣ Tap <b>Wallet</b> ➔ <b>Add Credits</b>.
2️⃣ Pick a package (₹100 = 5,000 Credits) or enter a custom amount.
3️⃣ Scan the auto-generated dynamic UPI QR code with GPay, PhonePe, or Paytm.
4️⃣ Tap <b>Upload Payment Screenshot</b> and send your payment receipt.
5️⃣ Your wallet balance is credited immediately upon admin verification!

🔹 <b>Step 4: Automated 24/7 Boost Delivery</b>
• The moment you publish any new post in your linked channel, our server detects it in real-time and orders the views & reactions instantly from the SMM panel!

🔹 <b>Step 5: Refer & Earn Free Credits</b>
• Share your referral link from <b>Refer & Earn</b> with other channel owners.
• Both you and your friend receive <b>+{REFERRAL_REWARD} free credits</b> when they join!
</blockquote>

"""
    await edit_or_send(
        call,
        guide_text,
        ui.inbot_guide_keyboard(),
    )
    await call.answer()
