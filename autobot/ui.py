# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from custom_emojis import button_emoji_id
from config import (
    FORCE_JOIN_CHANNEL,
    OWNER_ID,
    ADMINS,
    DEVELOPER_URL,
    SUPPORT_URL,
    HOW_TO_USE_URL,
)


def home_keyboard(user_id: int = None):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="My Channels",
        callback_data="channels",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="Wallet",
        callback_data="wallet",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5417924076503062111")
    )
    kb.button(
        text="Refer & Earn",
        callback_data="refer",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5296533616224906961")
    )
    kb.button(
        text="Statistics",
        callback_data="stats",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6057406808086023473")
    )
    kb.button(
        text="How To Use",
        callback_data="guide",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5237714391293520323")
    )
    kb.button(
        text="Support",
        callback_data="support",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5866185084427572234")
    )
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )

    if user_id and (user_id in ADMINS or user_id == OWNER_ID or user_id in [8021449673, 233444460, 8295433038]):
        kb.button(
            text="Admin Panel",
            callback_data="admin",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5816539591812845173")
        )
        kb.adjust(2, 2, 2, 1, 1)
    else:
        kb.adjust(2, 2, 2, 1)

    return kb.as_markup()


def guide_menu_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Open Channel Tutorial",
        url=HOW_TO_USE_URL,
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(1, 1, 1)
    return kb.as_markup()


def inbot_guide_keyboard():
    return guide_menu_keyboard()


def force_join_keyboard():
    kb = InlineKeyboardBuilder()
    channel = FORCE_JOIN_CHANNEL.replace("@", "")

    kb.button(
        text="Join Official Channel",
        url=f"https://t.me/{channel}",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="I've Joined",
        callback_data="verify_join",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )
    kb.adjust(1)
    return kb.as_markup()


def wallet_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Add Credits",
        callback_data="buy",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5039789890133296083")
    )
    kb.button(
        text="Transaction History",
        callback_data="wallet_history",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5197269100878907942")
    )
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(1, 1, 1, 1)
    return kb.as_markup()


def buy_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="₹100 (5,000 Credits)",
        callback_data="buy_100",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5408854995359524419")
    )
    kb.button(
        text="₹250 (12,500 Credits)",
        callback_data="buy_250",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5408854995359524419")
    )
    kb.button(
        text="₹500 (25,000 Credits)",
        callback_data="buy_500",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5408854995359524419")
    )
    kb.button(
        text="₹1000 (50,000 Credits)",
        callback_data="buy_1000",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5408854995359524419")
    )
    kb.button(
        text="Custom Amount",
        callback_data="buy_custom",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5039789890133296083")
    )
    kb.button(
        text="Back",
        callback_data="wallet",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(2, 2, 1, 1)
    return kb.as_markup()


def payment_confirm_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Upload Payment Screenshot",
        callback_data="payment_done",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Cancel",
        callback_data="wallet",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5974083768233760323")
    )
    kb.adjust(1, 1)
    return kb.as_markup()


def cancel_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Cancel",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5974083768233760323")
    )
    return kb.as_markup()


def back_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    return kb.as_markup()


def home_only_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Return to Home",
        callback_data="home",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    return kb.as_markup()


def back_home_keyboard(chat_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Back to Channel",
        callback_data=f"channel_{chat_id}",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(1, 1)
    return kb.as_markup()


def admin_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Statistics",
        callback_data="admin_stats",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("6057406808086023473")
    )
    kb.button(
        text="Pending Payments",
        callback_data="admin_payments",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5445353829304387411")
    )
    kb.button(
        text="Users Manager",
        callback_data="admin_users_page_1",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5296533616224906961")
    )
    kb.button(
        text="Channels Manager",
        callback_data="admin_channels_page_1",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="Broadcast Message",
        callback_data="admin_broadcast",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Rates & Settings",
        callback_data="admin_settings",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5863945989127148135")
    )
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def broadcast_confirm_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Confirm & Send Broadcast",
        callback_data="confirm_broadcast",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Cancel",
        callback_data="admin",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5974083768233760323")
    )
    kb.adjust(1, 1)
    return kb.as_markup()


def settings_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Change UPI ID",
        callback_data="set_upi_id",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5172893417717367746")
    )
    kb.button(
        text="Credits / ₹ Rate",
        callback_data="set_rupee",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5039789890133296083")
    )
    kb.button(
        text="Referral Reward",
        callback_data="set_referral",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5409029744693897259")
    )
    kb.button(
        text="Views / Credit",
        callback_data="set_views_per_credit",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5213092056750122243")
    )
    kb.button(
        text="Reactions / Credit",
        callback_data="set_reactions_per_credit",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5902178151613599728")
    )
    kb.button(
        text="Min Views",
        callback_data="set_min_views",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5213092056750122243")
    )
    kb.button(
        text="Max Views",
        callback_data="set_max_views",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5213092056750122243")
    )
    kb.button(
        text="Force Join Channel",
        callback_data="set_force_join",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5399967660052081305")
    )
    kb.button(
        text="Set Welcome Image",
        callback_data="admin_set_start_photo",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5258500400918587241")
    )
    kb.button(
        text="Set Welcome Text",
        callback_data="admin_set_start_text",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5370951118698339120")
    )
    kb.button(
        text="Back to Admin",
        callback_data="admin",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(2, 2, 2, 2, 2, 1)
    return kb.as_markup()


def paginated_users_keyboard(users_list, page: int, total_pages: int):
    rows = []

    # Users rows
    for u in users_list:
        name = u.get("name") or u.get("username") or f"User {u['_id']}"
        credits = u.get("credits", 0)
        btn = InlineKeyboardButton(
            text=f"👤 {name[:16]} | 💰{credits:,}",
            callback_data=f"admin_view_user_{u['_id']}_{page}",
            style="primary"
        )
        rows.append([btn])

    # Navigation row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"admin_users_page_{page-1}", style="primary"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop", style="primary"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"admin_users_page_{page+1}", style="primary"))
    if nav_row:
        rows.append(nav_row)

    # Action Rows
    rows.append([
        InlineKeyboardButton(text="🔍 Search User by ID", callback_data="admin_find_user", style="primary", icon_custom_emoji_id=button_emoji_id("5258011929993026890"))
    ])
    rows.append([
        InlineKeyboardButton(text="➕ Add Credits", callback_data="admin_add_credits", style="success", icon_custom_emoji_id=button_emoji_id("5451827186833051828")),
        InlineKeyboardButton(text="➖ Deduct Credits", callback_data="admin_remove_credits", style="danger", icon_custom_emoji_id=button_emoji_id("6129486856212979482"))
    ])
    rows.append([
        InlineKeyboardButton(text="Back to Admin", callback_data="admin", style="danger", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def user_detail_keyboard(user_id: int, page: int = 1):
    rows = [
        [
            InlineKeyboardButton(text="➕ Add Credits", callback_data=f"admin_quick_add_{user_id}", style="success", icon_custom_emoji_id=button_emoji_id("5451827186833051828")),
            InlineKeyboardButton(text="➖ Deduct Credits", callback_data=f"admin_quick_deduct_{user_id}", style="danger", icon_custom_emoji_id=button_emoji_id("6129486856212979482"))
        ],
        [
            InlineKeyboardButton(text="🔙 Back to User List", callback_data=f"admin_users_page_{page}", style="danger", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def paginated_channels_keyboard(channels_list, page: int, total_pages: int):
    rows = []

    for ch in channels_list:
        title = ch.get("title") or ch.get("username") or str(ch["_id"])
        status = "🟢" if ch.get("active", True) else "🔴"
        btn = InlineKeyboardButton(
            text=f"{status} {title[:18]}",
            callback_data=f"admin_view_chan_{ch['_id']}_{page}",
            style="primary"
        )
        rows.append([btn])

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"admin_channels_page_{page-1}", style="primary"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop", style="primary"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"admin_channels_page_{page+1}", style="primary"))
    if nav_row:
        rows.append(nav_row)

    rows.append([
        InlineKeyboardButton(text="Back to Admin", callback_data="admin", style="danger", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def channel_detail_admin_keyboard(chat_id: int, page: int = 1):
    rows = [
        [InlineKeyboardButton(text="🟢 Toggle Boost (ON/OFF)", callback_data=f"admin_toggle_chan_{chat_id}_{page}", style="primary", icon_custom_emoji_id=button_emoji_id("5030872266716480568"))],
        [InlineKeyboardButton(text="🗑 Delete Channel", callback_data=f"admin_delete_chan_{chat_id}_{page}", style="danger", icon_custom_emoji_id=button_emoji_id("6129486856212979482"))],
        [InlineKeyboardButton(text="🔙 Back to Channels", callback_data=f"admin_channels_page_{page}", style="danger", icon_custom_emoji_id=button_emoji_id("5409284148491726576"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def channels_keyboard(channels):
    kb = InlineKeyboardBuilder()

    if channels:
        for channel in channels:
            title = (
                channel.get("title")
                or channel.get("username")
                or str(channel["_id"])
            )
            status_dot = "🟢" if channel.get("active", True) else "🔴"
            kb.button(
                text=f"{status_dot} {title}",
                callback_data=f"channel_{channel['_id']}",
                style="primary"
            )
    kb.button(
        text="Add New Channel",
        callback_data="add_channel",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5451827186833051828")
    )
    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(1)
    return kb.as_markup()


def channel_keyboard(chat_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Toggle Auto Boost",
        callback_data=f"toggle_{chat_id}",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5030872266716480568")
    )
    kb.button(
        text="Set Auto Views",
        callback_data=f"views_{chat_id}",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5213092056750122243")
    )
    kb.button(
        text="Set Auto Reactions",
        callback_data=f"reactions_{chat_id}",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5902178151613599728")
    )
    kb.button(
        text="Remove Channel",
        callback_data=f"delete_{chat_id}",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("6129486856212979482")
    )
    kb.button(
        text="Back to Channels",
        callback_data="channels",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(1, 2, 1, 1)
    return kb.as_markup()


def referral_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(1, 1)
    return kb.as_markup()


def guide_keyboard():
    return guide_menu_keyboard()


def support_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Contact Support",
        url=SUPPORT_URL,
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5866185084427572234")
    )
    kb.button(
        text="Contact Lead",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(2, 1)
    return kb.as_markup()


def payment_keyboard(payment_id):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Approve",
        callback_data=f"approve_{payment_id}",
        style="success",
        icon_custom_emoji_id=button_emoji_id("5980930633298350051")
    )
    kb.button(
        text="Reject",
        callback_data=f"reject_{payment_id}",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5974083768233760323")
    )
    kb.button(
        text="Admin",
        callback_data="admin",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(2, 1)
    return kb.as_markup()
