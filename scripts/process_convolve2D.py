
import cv2
import time
import sys
import os
import numpy as np
import scipy.signal as sig
from imports.kernels import Kernel_2d
from imports.utils import get_image, get_image_name_path, get_shape_output_valid, add_filename_suffix
from imports.query_params import QueryParamsConvolution

start_time = time.time()
query_params = QueryParamsConvolution(sys.argv)
image_name_path = get_image_name_path(query_params.image_name)
image = get_image(image_name_path)


kernel_2d = Kernel_2d.get_kernel_2d(query_params.kernel_type, query_params.kernel_size)
image_blur = get_shape_output_valid(image, query_params.kernel_size, image.shape[2])
for channel in range(image.shape[2]):
    image_blur[:,:,channel] = np.uint8(sig.convolve2d(image[:,:,channel], kernel_2d, mode='valid'))
end_time = time.time()

# write processed file
cv2.imwrite(add_filename_suffix(image_name_path, query_params.kernel_type), image_blur)


print(f"Time taken for convolution with a Gaussian filter using sig.convolve2d is {end_time - start_time:.4f} seconds")