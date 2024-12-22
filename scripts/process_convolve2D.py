import sys
import time
import numpy as np
import scipy.signal as sig
from imports.kernel import Kernel
from imports.imports import QueryParamsConvolution, ConvolutionType, ImageType
from imports.utils import get_image_from_stdin, get_shape_output, set_stdout, get_image_type


query_params = QueryParamsConvolution(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
kernel_2d = Kernel.get_kernel(query_params.smoothing_type, ConvolutionType.TWO_D, query_params.kernel_size)
image_type = get_image_type(image.shape)
image_blur = get_shape_output(query_params.border_mode, query_params.kernel_size, image.shape, image_type)

match image_type:
    case ImageType.GRAYSCALE:
        image_blur[:,:] = np.uint8(sig.convolve2d(image[:,:], kernel_2d, mode=query_params.border_mode.value))
    case ImageType.RGB:
        for channel in range(ImageType.RGB.value):
            image_blur[:,:,channel] = np.uint8(sig.convolve2d(image[:,:,channel], kernel_2d, mode=query_params.border_mode.value))
    case _:
        raise ValueError(f"Unsupported image type: '{image_type}'")

end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for convolution with a Gaussian filter using sig.convolve2d is {time_taken:.4f} seconds")