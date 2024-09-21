from telegram import Bot

from app.config import TG_TOKEN

TELEGRAM_BOT_TOKEN = TG_TOKEN
CHAT_ID = '685366044'

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_telegram_message(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)
