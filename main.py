from facebook_checker import check_groups_for_images
from telegram_notifier import send_telegram_message
import time
import traceback

CHECK_INTERVAL_MINUTES = 20  # Интервал проверки

if __name__ == "__main__":
    while True:
        try:
            matches = check_groups_for_images()
            if matches:
                for match in matches:
                    send_telegram_message(match)
        except Exception as e:
            send_telegram_message("❌ Ошибка в боте:\n" + traceback.format_exc())

        time.sleep(CHECK_INTERVAL_MINUTES * 60)
