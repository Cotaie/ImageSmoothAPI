import sys
import time
import numpy as np
import scipy.signal as sig
from imports.kernels import Kernel2d
from imports.types import QueryParamsConvolution
from imports.utils import get_image_from_stdin, get_no_channels, get_shape_output, set_stdout


query_params = QueryParamsConvolution(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
kernel_2d = Kernel2d.get_kernel_2d(query_params.smoothing_type, query_params.kernel_size)
no_channels = get_no_channels(image.shape)
image_blur = get_shape_output(query_params.convolution_mode)(image.shape, query_params.kernel_size, no_channels)
for channel in range(no_channels):
    image_blur[:,:,channel] = np.uint8(sig.convolve2d(image[:,:,channel], kernel_2d, mode=query_params.convolution_mode.value))
end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for convolution with a Gaussian filter using sig.convolve2d is {time_taken:.4f} seconds")