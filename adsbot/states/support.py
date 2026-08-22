# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.fsm.state import StatesGroup, State


class SupportState(StatesGroup):
    waiting_issue = State()
    waiting_contact = State()