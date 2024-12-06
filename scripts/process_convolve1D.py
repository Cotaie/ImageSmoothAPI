import sys
import time
import numpy as np
from imports.kernels import Kernel1d
from imports.query_params import QueryParamsConvolution
from imports.utils import get_image_from_stdin, set_stdout, get_shape_output, get_no_channels


def do_conv(kern, mode: str):
    return lambda dimension: np.convolve(dimension, kern, mode=mode)

query_params = QueryParamsConvolution(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
kernel_1d = Kernel1d.get_kernel_1d(query_params.smoothing_type, query_params.kernel_size)
no_channels = get_no_channels(image.shape)
image_blur = get_shape_output(query_params.convolution_mode)(image.shape, query_params.kernel_size, no_channels)
for channel in range(no_channels):
    first_convolution = np.apply_along_axis(do_conv(kernel_1d[0], query_params.convolution_mode.value), axis=0, arr=image[:,:,channel])
    image_blur[:,:,channel] = np.apply_along_axis(do_conv(kernel_1d[1], query_params.convolution_mode.value), axis=1, arr=first_convolution)
end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for convolution with a box filter using np.convolve is {time_taken:.4f} seconds")