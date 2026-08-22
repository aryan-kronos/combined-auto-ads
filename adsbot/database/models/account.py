# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Account:
    id: int
    user_id: int
    account_name: str
    phone: str | None = None
    session_string: str = ""
    active_campaign: bool = False
    active: bool = True
    created_at: datetime | None = None
    running_campaign: bool = False
