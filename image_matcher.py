import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from config import MAX_DISTANCE

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
