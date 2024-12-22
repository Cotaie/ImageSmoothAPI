import os
import cv2
import sys
import numpy as np
from imports.kernel import STD_RATIO_KERNEL
from imports.imports import BorderMode, ImageType


TIME_TAKEN_STRING = "Time-Taken"

def get_border_mode_value(border_mode: BorderMode, kernel_size: int):
    match border_mode:
        case BorderMode.VALID:
            return -kernel_size + 1
        case BorderMode.SAME:
            return 0
        case BorderMode.FULL:
            return kernel_size - 1
        case _:
            raise ValueError(f"Unsupported mode type: '{border_mode}'")

def get_shape_output(border_mode: BorderMode, kernel_size: int, shape: tuple[int,int] | tuple[int,int,int], image_type: ImageType):
    border_mode_value = get_border_mode_value(border_mode, kernel_size)
    def _inner(image_type: ImageType):
        match image_type:
            case ImageType.GRAYSCALE:
                return (shape[0] + border_mode_value, shape[1] + border_mode_value)
            case ImageType.RGB:
                return (shape[0] + border_mode_value, shape[1] + border_mode_value, ImageType.RGB.value)
            case _:
                raise ValueError(f"Unsupported image type: '{image_type}'")
    return np.zeros(_inner(image_type))

        
def get_default_kernel_value(shape: tuple):
    return round(min(shape[0], shape[1]) * STD_RATIO_KERNEL)

def get_image_from_stdin() -> np.ndarray:
    image_data = sys.stdin.buffer.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if image is None:
        print("Failed to decode image")
        sys.exit(1)
    return image

def get_extension_from_filename(filename: str):
    return os.path.splitext(filename)[1]

def set_stdout(image: np.ndarray, image_name: str):
    image_extension = get_extension_from_filename(image_name)
    _, encoded_image = cv2.imencode(image_extension, image)
    #sys.stdout.write(f"{TIME_TAKEN_STRING}: {time_taken:.6f}\n")
    sys.stdout.buffer.write(encoded_image)

def get_image_type(shape: tuple[int, int, int] | tuple[int,int]):
    return ImageType.GRAYSCALE if shape[2] is None else ImageType.RGB