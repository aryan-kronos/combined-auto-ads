# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):

    commands = [
        BotCommand(
            command="start",
            description="🏠 Start"
        ),
        BotCommand(
            command="status",
            description="📊 Bot Status"
        ),
        BotCommand(
            command="running",
            description="🚀 Running Campaigns"
        ),
        BotCommand(
            command="maintenance",
            description="🛠 Maintenance Mode"
        ),
        BotCommand(
            command="feedback",
            description="⭐ Send Feedback"
        ),
    ]

    await bot.set_my_commands(commands)