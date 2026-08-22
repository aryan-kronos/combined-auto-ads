# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import config
from custom_emojis import premiumize_text


class PremiumEmojiBot(Bot):
    """Preserves the existing Bot API behavior while adding configured custom emojis."""

    _TEXT_FIELDS = {
        "SendMessage": ("text",),
        "EditMessageText": ("text",),
        "SendPhoto": ("caption",),
        "EditMessageCaption": ("caption",),
        "SendVideo": ("caption",),
        "SendAnimation": ("caption",),
        "SendAudio": ("caption",),
        "SendDocument": ("caption",),
        "SendVoice": ("caption",),
        "CopyMessage": ("caption",),
    }

    async def __call__(self, method, request_timeout=None):
        fields = self._TEXT_FIELDS.get(method.__class__.__name__, ())
        # Keep explicit MessageEntity usage untouched.
        if fields and getattr(method, "entities", None) is None and getattr(method, "caption_entities", None) is None:
            for field in fields:
                value = getattr(method, field, None)
                if isinstance(value, str):
                    updated = premiumize_text(value)
                    if updated != value:
                        setattr(method, field, updated)
        return await super().__call__(method, request_timeout=request_timeout)


bot = PremiumEmojiBot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
