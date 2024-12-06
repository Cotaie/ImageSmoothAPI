import numpy as np
import cv2
import os

BASE_FILE_NAME_PATH = "./render_image/"


def get_image_name_path(image_name: str):
    return f"{BASE_FILE_NAME_PATH}{image_name}"
    
def get_image(image_name_path: str):
    image = cv2.imread(image_name_path)
    if len(image.shape) == 2:
        return np.expand_dims(image, axis=-1)
    elif len(image.shape) == 3 and image.shape[2] == 3:
        return image
    else:
        print("The image format is unknown.")

def add_image_name_path_suffix(image_name_path: str, suffix: str):
    name, ext = os.path.splitext(image_name_path)
    return f"{name}_{suffix}{ext}"