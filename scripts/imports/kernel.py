import numpy as np
import math
from imports.imports import SmoothingType, ConvolutionType


STD_RATIO_KERNEL = 0.01

class Kernel:
    @staticmethod
    def get_kernel(smoothing_type: SmoothingType, convolution_type: str, size: int):
        match smoothing_type:
            case SmoothingType.BOX_BLUR:
                match convolution_type:
                    case ConvolutionType.ONE_D:
                        return np.ones((size,), dtype=np.float64) / size
                    case ConvolutionType.TWO_D:
                        return np.ones((size,size), dtype=np.float64) / (size*size)
                    case _:
                        raise ValueError(f"Unsupported convolution type: '{convolution_type}'")
            case SmoothingType.GAUSSIAN_BLUR:
                match convolution_type:
                    case ConvolutionType.ONE_D:
                        sigma = size/(2*math.pi)
                        ax = np.linspace(-(size // 2), size // 2, size)
                        kernel = np.exp(-0.5 * (ax / sigma) ** 2)
                        return kernel / np.sum(kernel)
                    case ConvolutionType.TWO_D:
                        sigma = size/(2*math.pi)
                        ax = np.linspace(-(size // 2), size // 2, size)
                        xx, yy = np.meshgrid(ax, ax)
                        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
                        return kernel / np.sum(kernel)
                    case _:
                        raise ValueError(f"Unsupported convolution type: '{convolution_type}'")
            case _:
                raise ValueError(f"Unsupported kernel type: '{smoothing_type}'")
