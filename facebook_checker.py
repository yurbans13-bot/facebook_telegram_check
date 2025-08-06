
import os
import time
import hashlib
import tempfile
from playwright.async_api import async_playwright
from PIL import Image
from utils.image_matcher import load_image, is_similar
from config import FACEBOOK_GROUP_URLS

async def check_groups_for_images(reference_images, cookies):
    matches = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies(cookies)

        for url in FACEBOOK_GROUP_URLS:
            page = await context.new_page()
            await page.goto(url, timeout=60000)

            # Прокрутка и сбор изображений
            for _ in range(3):
                await page.mouse.wheel(0, 2000)
                await page.wait_for_timeout(2000)

            images = await page.locator("img").element_handles()
            for img_el in images:
                try:
                    src = await img_el.get_attribute("src")
                    if not src:
                        continue
                    img_bytes = await download_image(page, src)
                    if not img_bytes:
                        continue

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(img_bytes)
                        tmp_path = tmp.name

                    candidate = load_image(tmp_path)

                    for ref_name, ref_img in reference_images:
                        if is_similar(candidate, ref_img):
                            matches.append(src)
                            break

                    os.unlink(tmp_path)

                except Exception:
                    continue

            await page.close()

        await context.close()
        await browser.close()
    return matches

async def download_image(page, url):
    try:
        response = await page.request.get(url)
        if response.ok:
            return await response.body()
    except:
        return None
