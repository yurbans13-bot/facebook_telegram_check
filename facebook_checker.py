import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from image_tools import image_matches
from telegram_notifier import send_telegram_message
from config import FACEBOOK_GROUP_URLS
import logging

logger = logging.getLogger(__name__)

# Путь к headless_shell — должен быть актуальным
EXECUTABLE_PATH = "/opt/render/.cache/ms-playwright/chromium_headless_shell-1181/chrome-linux/headless_shell"

async def check_groups_for_images(reference_images: list[Path], cookies: list[dict]) -> list[tuple[str, str]]:
    matches = []

    logger.info("Запуск браузера...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                executable_path=EXECUTABLE_PATH
            )
            context = await browser.new_context()
            await context.add_cookies(cookies)

            for group_url in FACEBOOK_GROUP_URLS:
                page = await context.new_page()
                logger.info(f"Проверка группы: {group_url}")
                try:
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

                except Exception as e:
                    logger.warning(f"Не удалось загрузить {group_url}: {e}")
                finally:
                    await page.close()

            await context.close()
            await browser.close()

    except Exception as e:
        logger.error(f"Ошибка при запуске браузера: {e}")
        await send_telegram_message(f"❌ Ошибка при запуске браузера:\n{e}")

    return matches
