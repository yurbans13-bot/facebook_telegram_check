from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
import asyncio
import traceback

CHECK_INTERVAL_MINUTES = 20  # Интервал проверки

async def main_loop():
    while True:
        try:
            matches = check_groups_for_images()
            if matches:
                for match in matches:
                    await send_telegram_message(match)
        except Exception:
            await send_telegram_message("❌ Ошибка в боте:\n" + traceback.format_exc())

        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    asyncio.run(main_loop())
