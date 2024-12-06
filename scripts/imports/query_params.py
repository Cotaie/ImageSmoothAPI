from imports.types_enum import SmoothingType, ConvolutionMode

class QueryParams:
    def __init__(self, args):
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
