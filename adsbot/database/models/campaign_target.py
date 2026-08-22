# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CampaignTarget:
    id: int
    campaign_id: int
    chat_id: int
    chat_username: str | None = None
    chat_title: str | None = None
    created_at: datetime | None = None
