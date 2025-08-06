
from flask import Flask
import threading
from main import run_bot  # Предполагается, что основной цикл вынесен в функцию run_bot()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Facebook Image Monitor Bot is running."

# Запуск фонового потока для бота
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
