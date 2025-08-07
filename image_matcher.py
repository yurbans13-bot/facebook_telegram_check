import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from config import MAX_DISTANCE
from io import BytesIO
import requests
from pathlib import Path

def load_reference_images(directory="samples"):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(directory, filename)
            images.append((filename, load_image(path)))
    return images

def load_image(path):
    img = Image.open(path).convert("L").resize((100, 100))
    return np.array(img)

def compare_images(img1, img2):
    return 1 - ssim(img1, img2)

def is_similar(img1, img2):
    return compare_images(img1, img2) <= (MAX_DISTANCE / 100)

def image_matches(image_url: str, reference_images: list[tuple[str, np.ndarray]]) -> bool:
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("L").resize((100, 100))
        img_array = np.array(img)

        for _, ref_img in reference_images:
            if is_similar(img_array, ref_img):
                return True

    except Exception as e:
        print(f"Ошибка при сравнении: {e}")

    return False
