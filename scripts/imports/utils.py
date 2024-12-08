import os
import cv2
import sys
import numpy as np
from imports.kernels import STD_RATIO_KERNEL
from imports.imports import ConvolutionMode


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

def get_no_channels(shape: tuple) -> int:
    return 1 if shape[2] is None else shape[2]