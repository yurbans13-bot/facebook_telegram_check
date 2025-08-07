# main.py
import asyncio
from image_utils import load_reference_images
from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
from config import COOKIES_FILE, MAX_DISTANCE
import json
import logging

logging.basicConfig(level=logging.INFO)

async def run_check():
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)

    reference_images = load_reference_images()
    matches = await check_groups_for_images(reference_images, cookies)

    if not matches:
        logging.info("Нет совпадений.")
    else:
        logging.info(f"Найдено {len(matches)} совпадений.")

if __name__ == "__main__":
    asyncio.run(run_check())
