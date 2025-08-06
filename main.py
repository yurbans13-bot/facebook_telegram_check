
import asyncio
import logging
from utils.facebook_checker import check_groups_for_images
from utils.image_matcher import load_reference_images
from utils.telegram_notifier import send_telegram_message
from utils.helpers import load_cookies

CHECK_INTERVAL_MINUTES = 20

async def main_loop():
    logging.basicConfig(level=logging.INFO)
    reference_images = load_reference_images()
    cookies = load_cookies()

    while True:
        try:
            matched = await check_groups_for_images(reference_images, cookies)
            if matched:
                await send_telegram_message(f"🔔 Найдено {len(matched)} совпадений среди изображений!")
            else:
                logging.info("Нет совпадений.")
        except Exception as e:
            logging.exception("Ошибка во время выполнения:")
            await send_telegram_message(f"❌ Ошибка в боте: {e}")
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    asyncio.run(main_loop())
