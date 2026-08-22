# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bio:
    id: int
    user_id: int
    text: str
    created_at: datetime | None = None
