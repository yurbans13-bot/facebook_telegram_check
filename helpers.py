
import json

def load_cookies(path="all_cookies.txt"):
    with open(path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    return cookies
