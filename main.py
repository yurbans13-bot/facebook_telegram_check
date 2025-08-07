from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
import time
import traceback
import asyncio

CHECK_INTERVAL_MINUTES = 20  # Интервал проверки

async def run_check():
    try:
        matches = check_groups_for_images()
        if matches:
            for match in matches:
                await send_telegram_message(match)
    except Exception:
        await send_telegram_message("❌ Ошибка в боте:\n" + traceback.format_exc())

if __name__ == "__main__":
    while True:
        asyncio.run(run_check())
        time.sleep(CHECK_INTERVAL_MINUTES * 60)
