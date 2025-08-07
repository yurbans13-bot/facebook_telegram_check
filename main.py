import asyncio
import time
import traceback

from image_matcher import load_reference_images
from facebook_checker import load_cookies, check_groups_for_images
from telegram_notifier import send_telegram_message

CHECK_INTERVAL_MINUTES = 20  # Интервал проверки


async def run_check():
    try:
        reference_images = load_reference_images("samples")
        cookies = load_cookies("all_cookies.txt")
        matches = await check_groups_for_images(reference_images, cookies)

        if matches:
            for match in matches:
                await send_telegram_message(match)

    except Exception:
        await send_telegram_message("❌ Ошибка в боте:\n" + traceback.format_exc())


if __name__ == "__main__":
    while True:
        asyncio.run(run_check())
        time.sleep(CHECK_INTERVAL_MINUTES * 60)
