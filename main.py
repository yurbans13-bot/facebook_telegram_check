import asyncio
import json
import logging

from image_tools import load_reference_images  # 🔁 было image_utils
from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
from config import COOKIES_FILE

logging.basicConfig(level=logging.INFO)

async def run_check():
    # Загрузка cookies
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)

    # Загрузка эталонных изображений
    reference_images = load_reference_images()

    # Поиск совпадений
    matches = await check_groups_for_images(reference_images, cookies)

    if not matches:
        logging.info("Нет совпадений.")
    else:
        logging.info(f"Найдено {len(matches)} совпадений.")
        for group_url, image_url in matches:
            await send_telegram_message(f"✅ Совпадение в {group_url}\n{image_url}")

if __name__ == "__main__":
    asyncio.run(run_check())
