# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Campaign:
    id: int
    account_id: int
    title: str = "New Campaign"
    post_data: str = ""
    send_delay: int = 3
    repeat_delay: int = 86400
    total_sent: int = 0
    failed_sent: int = 0
    current_target: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    running: bool = False
    completed: bool = False
    loop_count: int = 1
    completed_loops: int = 0
    infinite: bool = False
    paused: bool = False
    scheduled_at: datetime | None = None
    last_run: datetime | None = None
    next_run: datetime | None = None
    created_at: datetime | None = None
