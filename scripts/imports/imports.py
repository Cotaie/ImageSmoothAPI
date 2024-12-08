from enum import Enum


class ConvolutionType(Enum):
    ONE_D = 0
    TWO_D = 1

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
        self.convolution_mode = ConvolutionMode.from_string(args[4])

class QueryParamsBilateral(QueryParams): 
    def __init__(self, args):
        super().__init__(args)
        self.signal_color = args[4]
        self.sigma_space = args[5]

class QueryParamsMedian(QueryParams):
    def __init__(self, args):
        super().__init__(args)
