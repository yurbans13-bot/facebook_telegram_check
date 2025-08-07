import asyncio
import json
import logging

from utils.image_loader import load_reference_images
from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
from config import COOKIES_FILE

logging.basicConfig(level=logging.INFO)

async def run_check():
    try:
        # Загружаем cookies
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)

        # Загружаем эталонные изображения
        reference_images = load_reference_images()

        # Проверяем группы
        matches = await check_groups_for_images(reference_images, cookies)

        if not matches:
            logging.info("✅ Нет совпадений.")
        else:
            logging.info(f"🔍 Найдено {len(matches)} совпадений.")
            for group_url, image_url in matches:
                await send_telegram_message(f"🔔 Совпадение найдено:\nГруппа: {group_url}\nИзображение: {image_url}")

    except Exception as e:
        logging.error(f"❌ Ошибка в run_check: {e}")
        await send_telegram_message(f"❌ Ошибка в боте:\n{e}")

if __name__ == "__main__":
    asyncio.run(run_check())
