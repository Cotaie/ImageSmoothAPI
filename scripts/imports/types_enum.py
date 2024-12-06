from enum import Enum


class ConvolutionMode(Enum):
    VALID = 'valid'
    SAME = 'same'
    FULL = 'full'
    @classmethod
    def from_string(cls, convolution_mode: str) -> "ConvolutionMode":
        try:
            return cls(convolution_mode)
        except ValueError:
            raise ValueError(f"Invalid smoothing type: {convolution_mode}")

class SmoothingType(Enum):
    BOX_BLUR = 'box-blur'
    GAUSSIAN_BLUR = 'gaussian-blur'
    MEDIAN_BLUR = 'median-blur'
    @classmethod
    def from_string(cls, smoothing_type: str) -> "SmoothingType":
        try:
            return cls(smoothing_type)
        except ValueError:
            raise ValueError(f"Invalid smoothing type: {smoothing_type}")
        
