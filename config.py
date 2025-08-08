# config.py
import json
import os
import sys

# Telegram
TELEGRAM_TOKEN = "8146445783:AAE7XOUZB8Evil2pKIl1g0FczpBndbGbVek"
TELEGRAM_CHAT_ID = 243580570

# Facebook группы
FACEBOOK_GROUP_URLS = [
    "https://www.facebook.com/share/g/16tri6YkoY/",
    "https://www.facebook.com/share/g/16ktKMdwjL/"
]

# Порог сравнения изображений (чем меньше, тем строже)
MAX_DISTANCE = 8

COOKIES_FILE = "all_cookies.txt"

def load_cookies(path=COOKIES_FILE):
    if not os.path.exists(path):
        sys.exit(f"❌ Файл {path} не найден! Сначала создай его и вставь cookies из Opera.")

    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip()
        if not data:
            sys.exit(f"❌ Файл {path} пустой! Экспортируй cookies из Opera в JSON и вставь сюда.")

        try:
            cookies = json.loads(data)
        except json.JSONDecodeError:
            sys.exit(f"❌ Cookies в {path} не являются валидным JSON! Проверь формат.")

        if not isinstance(cookies, list) or not all("name" in c and "value" in c for c in cookies):
            sys.exit("❌ Cookies имеют неправильную структуру. Экспортируй их через расширение Cookie-Editor.")

        return cookies
