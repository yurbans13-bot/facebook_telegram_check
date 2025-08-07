import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from config import MAX_DISTANCE

def load_reference_images(directory="samples"):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(directory, filename)
            image = load_image(path)
            if image is not None:
                images.append((filename, image))
    return images

def load_image(path):
    try:
        img = Image.open(path).convert("L").resize((100, 100))  # grayscale
        return np.array(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения {path}: {e}")
        return None

def compare_images(img1, img2):
    try:
        score = ssim(img1, img2)
        return 1 - score  # чем меньше разница, тем ближе к 0
    except Exception as e:
        print(f"Ошибка сравнения изображений: {e}")
        return 1  # максимально непохожи

async def image_matches(image_url, reference_images):
    try:
        from io import BytesIO
        import requests

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("L").resize((100, 100))
        test_img = np.array(image)

        for name, ref_img in reference_images:
            distance = compare_images(test_img, ref_img)
            if distance <= (MAX_DISTANCE / 100):
                return True
        return False
    except Exception as e:
        print(f"Ошибка загрузки или сравнения изображения {image_url}: {e}")
        return False
