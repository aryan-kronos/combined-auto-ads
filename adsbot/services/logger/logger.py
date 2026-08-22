# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram.exceptions import TelegramBadRequest

from loader import bot
from config import config


async def send_log(text: str):

    if config.LOG_CHANNEL == 0:
        return

    try:

        await bot.send_message(
            chat_id=config.LOG_CHANNEL,
            text=text,
        )

    except TelegramBadRequest:
        pass