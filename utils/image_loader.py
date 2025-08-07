import os
import numpy as np
from PIL import Image

def load_image(path):
    img = Image.open(path).convert("L").resize((100, 100))
    return np.array(img)

def load_reference_images(directory="samples"):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(directory, filename)
            images.append((filename, load_image(path)))
    return images

