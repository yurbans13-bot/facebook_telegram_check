
import aiohttp
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    async with aiohttp.ClientSession() as session:
        await session.post(url, data=data)
