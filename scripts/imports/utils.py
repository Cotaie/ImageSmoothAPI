import numpy as np
import cv2
import math
import sys
import os

from imports.types_enum import ConvolutionMode, SmoothingType
from imports.kernels import STD_RATIO_KERNEL

TIME_TAKEN_STRING = "Time-Taken"

def get_shape_output(mode: ConvolutionMode):
    def _inner(shape: tuple, kernel_size: int, nr_channels: int):
        match mode:
            case ConvolutionMode.VALID:
                return np.zeros((shape[0] - kernel_size + 1,shape[1] - kernel_size + 1,nr_channels))
            case ConvolutionMode.SAME:
                return np.zeros((shape[0],shape[1],nr_channels))
            case ConvolutionMode.FULL:
                return np.zeros((shape[0] + kernel_size - 1,shape[1] + kernel_size - 1,nr_channels))
            case _:
                raise ValueError(f"Unsupported mode type: '{mode}'")
    return _inner

def get_cv_function(image, smoothing_type: SmoothingType, kernel_size: int):
    match smoothing_type:
        case SmoothingType.BOX_BLUR:
            return cv2.blur(image, (kernel_size,kernel_size))
        case SmoothingType.GAUSSIAN_BLUR:
            return cv2.GaussianBlur(src=image, ksize=(kernel_size,kernel_size), sigmaX=kernel_size/(2*math.pi), sigmaY=kernel_size/(2*math.pi))
        case SmoothingType.MEDIAN_BLUR:
            return cv2.medianBlur(image, kernel_size)
        case _:
            raise ValueError(f"Unsupported kernel type: '{smoothing_type}'")
        
def get_default_kernel_value(shape):
    return round(min(shape[0], shape[1]) * STD_RATIO_KERNEL)

def get_image_from_stdin():
    image_data = sys.stdin.buffer.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if image is None:
        print("Failed to decode image")
        sys.exit(1)
    return image

def get_extension_from_filename(filename: str):
    return os.path.splitext(filename)[1]

def set_stdout(image, image_name):
    image_extension = get_extension_from_filename(image_name)
    _, encoded_image = cv2.imencode(image_extension, image)
    #sys.stdout.write(f"{TIME_TAKEN_STRING}: {time_taken:.6f}\n")
    sys.stdout.buffer.write(encoded_image)

def get_no_channels(shape: tuple):
    return 1 if shape[2] is None else shape[2]