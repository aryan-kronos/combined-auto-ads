# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.fsm.state import (
    State,
    StatesGroup
)


class BioState(StatesGroup):

    waiting_bio = State()

    selecting_account = State()

    selecting_bios = State()

    waiting_custom_interval = State()