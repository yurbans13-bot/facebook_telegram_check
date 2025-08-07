def load_cookies(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
# Telegram
TELEGRAM_TOKEN = "8101121299:AAEUKSZjhkMi6k8ccHh3PQ7xKGalW3t2b_s"
TELEGRAM_CHAT_ID = 243580570

# Facebook
FACEBOOK_GROUP_URLS = [
    "https://www.facebook.com/share/g/16tri6YkoY/",
    "https://www.facebook.com/share/g/16ktKMdwjL/"
]

# Сравнение изображений
MAX_DISTANCE = 8
