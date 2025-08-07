import asyncio
import os
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from image_matcher import image_matches
from telegram_notifier import send_telegram_message

import logging
logger = logging.getLogger(__name__)

GROUP_URLS = [
    "https://www.facebook.com/share/g/16tri6YkoY/",
    "https://www.facebook.com/share/g/16ktKMdwjL/"
]

EXECUTABLE_PATH = "/opt/render/project/src/.venv/lib/python3.13/site-packages/playwright/driver/package/.local-browsers/chromium_headless_shell-1181/chrome-linux/headless_shell"


async def check_groups_for_images(reference_images: list[Path], cookies: list[dict]) -> list[tuple[str, str]]:
    matches = []

    logger.info("Запуск браузера...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=EXECUTABLE_PATH
        )
        context = await browser.new_context()
        await context.add_cookies(cookies)

        for group_url in GROUP_URLS:
            page = await context.new_page()
            logger.info(f"Проверка группы: {group_url}")
            await page.goto(group_url, timeout=60000)

            await page.wait_for_timeout(3000)
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            img_tags = soup.find_all('img')

            for img in img_tags:
                src = img.get('src')
                if not src:
                    continue

                try:
                    if await image_matches(src, reference_images):
                        logger.info(f"✅ Найдено совпадение: {src}")
                        matches.append((group_url, src))
                        await send_telegram_message(f"🔍 Найдено совпадение в {group_url}\n{src}")
                except Exception as e:
                    logger.warning(f"Ошибка при сравнении изображений: {e}")

            await page.close()

        await context.close()
        await browser.close()

    return matches
