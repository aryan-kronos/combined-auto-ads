# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BotSetting:
    id: int
    page: str
    text: str | None = None
    media_type: str | None = None
    file_id: str | None = None
    updated_by: int | None = None
    updated_at: datetime | None = None
