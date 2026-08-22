# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class PremiumState(StatesGroup):
    waiting_details = State()
    waiting_screenshot = State()