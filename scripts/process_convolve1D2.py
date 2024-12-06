import cv2
import numpy as np
import time
import sys
from imports.query_params import QueryParamsConvolution
from imports.kernels import Kernel1d
from imports.utils import get_image_from_stdin, set_stdout, get_shape_output, get_no_channels
from imports.types_enum import ConvolutionMode, SmoothingType

def do_conv(kern):
    return lambda dimension: np.convolve(dimension, kern, mode='valid')

query_params = QueryParamsConvolution(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
kernel_1d = Kernel1d.get_kernel_1d(query_params.smoothing_type, query_params.kernel_size)
no_channels = get_no_channels(image.shape)
image_blur = get_shape_output(ConvolutionMode.VALID)(image.shape, query_params.kernel_size, no_channels)
for channel in range(no_channels):
    first_convolution = np.apply_along_axis(do_conv(kernel_1d[0]), axis=0, arr=image[:,:,channel])
    image_blur[:,:,channel] = np.apply_along_axis(do_conv(kernel_1d[1]), axis=1, arr=first_convolution)
end_time = time.time()

# write processed file
set_stdout(image_blur, query_params.image_name)

print(f"Time taken for convolution with a box filter using np.convolve is {end_time - start_time:.4f} seconds")
print(f"Received arguments: {sys.argv}")