from enum import Enum


class ImageType(Enum):
    GRAYSCALE = 1
    RGB = 3

class ConvolutionType(Enum):
    ONE_D = 0
    TWO_D = 1

class BorderMode(Enum):
    VALID = 'valid'
    SAME = 'same'
    FULL = 'full'
    @classmethod
    def from_string(cls, border_mode: str) -> "BorderMode":
        try:
            return cls(border_mode)
        except ValueError:
            raise ValueError(f"Invalid border mode: {border_mode}")

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

class MedianType(Enum):
    STANDARD = 'standard'
    HISTOGRAM = 'histogram'
    @classmethod
    def from_string(cls, median_mode: str) -> "MedianType":
        try:
            return cls(median_mode)
        except ValueError:
            raise ValueError(f"Invalid median type: {median_mode}")

class QueryParams:
    def __init__(self, args: list):
        self.location = args[0]
        self.image_name = args[1]
        self.smoothing_type = SmoothingType.from_string(args[2])
        self.kernel_size = int(args[3])

class QueryParamsOpenCv(QueryParams):
    def __init__(self, args):
        super().__init__(args)
        self.signal_color = args[4]
        self.sigma_space = args[5]

class QueryParamsConvolution(QueryParams):
    def __init__(self, args):
        super().__init__(args)
        self.border_mode = BorderMode.from_string(args[4])

class QueryParamsBilateral(QueryParams): 
    def __init__(self, args):
        super().__init__(args)
        self.signal_color = args[4]
        self.sigma_space = args[5]

class QueryParamsMedian(QueryParams):
    def __init__(self, args):
        super().__init__(args)
        self.border_mode = BorderMode.from_string(args[4])
        self.median_type = MedianType.from_string(args[5])
