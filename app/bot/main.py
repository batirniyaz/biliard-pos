from telegram import Bot

from app.config import TG_TOKEN, TG_CHAT_ID

TELEGRAM_BOT_TOKEN = TG_TOKEN
CHAT_ID = TG_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_telegram_message(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)
