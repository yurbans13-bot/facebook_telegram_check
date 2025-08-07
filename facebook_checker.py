import os
from pathlib import Path
from playwright.async_api import async_playwright
from config import FACEBOOK_GROUP_URLS
from image_matcher import load_image, is_similar
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import io
import base64

async def check_groups_for_images(reference_images, cookies):
    matches = []

    async with async_playwright() as p:
        # Указываем путь вручную к headless Chromium
        chromium_path = Path.home() / ".playwright" / "chromium-1181" / "chrome-linux" / "chrome"

        browser = await p.chromium.launch(
            headless=True,
            executable_path=str(chromium_path)
        )

        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()

        for url in FACEBOOK_GROUP_URLS:
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(5000)  # дожидаемся полной загрузки

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")

                for img_tag in soup.find_all("img"):
                    src = img_tag.get("src")
                    if src and src.startswith("data:image"):
                        header, encoded = src.split(",", 1)
                        image_data = base64.b64decode(encoded)
                        image = Image.open(io.BytesIO(image_data)).convert("L").resize((100, 100))
                        np_image = np.array(image)

                        for name, ref_image in reference_images:
                            if is_similar(np_image, ref_image):
                                matches.append(f"👁 Найдено совпадение с образцом '{name}' в группе:\n{url}")
                                break

            except Exception as e:
                matches.append(f"⚠️ Ошибка при проверке группы {url}:\n{e}")

        await browser.close()

    return matches
