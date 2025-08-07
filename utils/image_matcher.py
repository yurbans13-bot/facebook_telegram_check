from skimage.metrics import structural_similarity as ssim
from .image_loader import load_image
from config import MAX_DISTANCE

def compare_images(img1, img2):
    return 1 - ssim(img1, img2)

def image_matches(image_url, reference_images):
    import requests
    from io import BytesIO

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = load_image(BytesIO(response.content))
    except Exception:
        return False

    for name, ref_img in reference_images:
        if compare_images(img, ref_img) <= (MAX_DISTANCE / 100):
            return True
    return False

