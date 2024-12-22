import sys
import time
import numpy as np
from imports.kernel import Kernel
from imports.imports import QueryParamsConvolution, ConvolutionType, ImageType, BorderMode
from imports.utils import get_image_from_stdin, set_stdout, get_shape_output, get_image_type


def get_convolution_function(kern, border_mode: BorderMode):
    return lambda dimension: np.convolve(dimension, kern, mode=border_mode.value)

query_params = QueryParamsConvolution(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
kernel_1d = Kernel.get_kernel(query_params.smoothing_type, ConvolutionType.ONE_D, query_params.kernel_size)
image_type = get_image_type(image.shape)
image_blur = get_shape_output(query_params.border_mode, query_params.kernel_size, image.shape, image_type)
convolution_function = get_convolution_function(kernel_1d, query_params.border_mode)

match image_type:
    case ImageType.GRAYSCALE:
        first_convolution = np.apply_along_axis(convolution_function, axis=0, arr=image[:,:])
        image_blur[:,:] = np.apply_along_axis(convolution_function, axis=1, arr=first_convolution)
    case ImageType.RGB:
        for channel in range(image_type.value):
            first_convolution = np.apply_along_axis(convolution_function, axis=0, arr=image[:,:,channel])
            image_blur[:,:,channel] = np.apply_along_axis(convolution_function, axis=1, arr=first_convolution)
    case _:
        raise ValueError(f"Unsupported image type: '{image_type}'")
end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for convolution with a box filter using np.convolve is {time_taken:.4f} seconds")