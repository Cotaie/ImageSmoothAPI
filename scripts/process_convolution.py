import cv2
import numpy as np
import time
import sys
import scipy.signal as sig
from imports.kernels import Kernel1d
from imports.kernels import Kernel2d
from imports.query_params import QueryParamsConvolution
from imports.utils import get_shape_output
from imports.image import get_image, add_image_name_path_suffix, get_image_name_path


query_params = QueryParamsConvolution(sys.argv)
image_name_path = get_image_name_path(query_params.image_name)
image = get_image(image_name_path)
image_blur = get_shape_output(query_params.convolution_mode)(image.shape, query_params.kernel_size)
match query_params.convolution_type:
    case "convolution_1d":
        start_time = time.time()
        def do_conv(kern):
            return lambda dimension: np.convolve(dimension, kern, mode=query_params.convolution_mode)
        kernel_1d = Kernel1d.get_kernel_1d(query_params.smoothing_type, query_params.kernel_size)
        for channel in range(image.shape[2]):
            first_convolution = np.apply_along_axis(do_conv(kernel_1d[0]), axis=0, arr=image[:,:,channel])
            image_blur[:,:,channel] = np.apply_along_axis(do_conv(kernel_1d[1]), axis=1, arr=first_convolution)
        end_time = time.time()
    case "convolution2d":
        start_time = time.time()
        kernel_2d = Kernel2d.get_kernel_2d(query_params.smoothing_type, query_params.kernel_size)
        for channel in range(image.shape[2]):
            image_blur[:,:,channel] = np.uint8(sig.convolve2d(image[:,:,channel], kernel_2d, mode='valid'))
        end_time = time.time()

# write processed file
cv2.imwrite(add_image_name_path_suffix(image_name_path, query_params.smoothing_type), image_blur)

print(f"Time taken for {query_params.convolution_type} is {end_time - start_time:.4f} seconds")
print(f"Received arguments: {sys.argv}")