import cv2
import numpy as np
import time
import sys
from imports.kernels import Kernel_1d
from imports.utils import get_image, get_shape_output_valid, add_filename_suffix, get_image_name_path
from imports.query_params import QueryParamsConvolution

def do_conv(kern):
    return lambda dimension: np.convolve(dimension, kern, mode='valid')

start_time = time.time()
query_params = QueryParamsConvolution(sys.argv)
image_name_path = get_image_name_path(query_params.image_name)
image = get_image(image_name_path)
kernel_1d = Kernel_1d.get_kernel_1d(query_params.kernel_type, query_params.kernel_size)
image_blur = get_shape_output_valid(image, query_params.kernel_size, image.shape[2])
for channel in range(image.shape[2]):
    first_convolution = np.apply_along_axis(do_conv(kernel_1d[0]), axis=0, arr=image[:,:,channel])
    image_blur[:,:,channel] = np.apply_along_axis(do_conv(kernel_1d[1]), axis=1, arr=first_convolution)
end_time = time.time()

# write processed file
cv2.imwrite(add_filename_suffix(image_name_path, query_params.kernel_type), image_blur)

print(f"Time taken for convolution with a box filter using np.convolve is {end_time - start_time:.4f} seconds")
print(f"Received arguments: {sys.argv}")