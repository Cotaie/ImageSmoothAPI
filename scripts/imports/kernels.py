import numpy as np
import math
from imports.types_enum import SmoothingType

STD_RATIO_KERNEL = 0.01


class Kernel1d:
    @staticmethod
    def get_box_filter_1d(size: int):
        return np.ones((size,), dtype=np.float64) / size
    @staticmethod
    def get_gaussian_filter_1d(size: int):
        sigma = size/(2*math.pi)
        ax = np.linspace(-(size // 2), size // 2, size)
        kernel = np.exp(-0.5 * (ax / sigma) ** 2)
        return kernel / np.sum(kernel)
    @staticmethod
    def get_kernel_1d(smoothing_type: SmoothingType, size: int):
        match smoothing_type:
            case SmoothingType.BOX_BLUR:
                return (Kernel1d.get_box_filter_1d(size), Kernel1d.get_box_filter_1d(size))
            case SmoothingType.GAUSSIAN_BLUR:
                return (Kernel1d.get_gaussian_filter_1d(size), Kernel1d.get_gaussian_filter_1d(size))
            case _:
                raise ValueError(f"Unsupported kernel type: '{smoothing_type}'")

class Kernel2d:
    @staticmethod
    def get_box_filter_2d(size: int):
        return np.ones((size,size), dtype=np.float64) / (size*size)
    @staticmethod
    def get_gaussian_filter_2d(size: int):
        sigma = size/(2*math.pi)
        ax = np.linspace(-(size // 2), size // 2, size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
        return kernel / np.sum(kernel)
    @staticmethod
    def get_kernel_2d(smoothing_type: SmoothingType, size: int):
        match smoothing_type:
            case SmoothingType.BOX_BLUR:
                return Kernel2d.get_box_filter_2d(size)
            case SmoothingType.GAUSSIAN_BLUR:
                return Kernel2d.get_gaussian_filter_2d(size)
            case _:
                raise ValueError(f"Unsupported kernel type: '{smoothing_type}'")