# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BioRotation:
    id: int
    account_id: int
    enabled: bool = False
    interval: int = 3600
    current_index: int = 0
    last_changed: datetime | None = None
