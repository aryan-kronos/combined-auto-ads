# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.fsm.state import State, StatesGroup


class AddAccount(StatesGroup):
    waiting_phone = State()
    waiting_code = State()
    waiting_password = State()