# Custom / Premium Emojis

Edit **only `custom_emojis.py`** to change custom emoji IDs.

### Message emojis
Fill the value for each fallback emoji in `MESSAGE_EMOJI_IDS`:

```python
"💎": "5909174430000484676",
```

Leave a value blank until you have the correct Telegram custom emoji ID; the
bot will then keep showing the normal emoji instead of breaking.

### Button emojis
`BUTTON_EMOJI_IDS` contains every custom emoji ID that was already hard-coded
in the bot's keyboards. The left side is the original ID and the right side is
the editable ID. Callback data and button behavior are unchanged.

This bot uses **aiogram 3.25.0**. It already uses HTML as the global parse mode.
The custom emoji layer only touches outgoing Aiogram message text/captions;
callback-query alerts, Pyrogram campaign messages, database logic, and other
Bot API methods are not modified.
