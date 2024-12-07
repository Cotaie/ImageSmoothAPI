import cv2
import sys
import math
import time
from imports.types import SmoothingType, QueryParamsOpenCv
from imports.utils import get_image_from_stdin, set_stdout


def get_smoothing_result(image, smoothing_type: SmoothingType, kernel_size: int):
    match smoothing_type:
        case SmoothingType.BOX_BLUR:
            return cv2.blur(image, (kernel_size,kernel_size))
        case SmoothingType.GAUSSIAN_BLUR:
            return cv2.GaussianBlur(src=image, ksize=(kernel_size,kernel_size), sigmaX=kernel_size/(2*math.pi), sigmaY=kernel_size/(2*math.pi))
        case SmoothingType.MEDIAN_BLUR:
            return cv2.medianBlur(image, kernel_size)
        case _:
            raise ValueError(f"Unsupported kernel type: '{smoothing_type}'")

query_params = QueryParamsOpenCv(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
image_blur = get_smoothing_result(image, query_params.smoothing_type, query_params.kernel_size)
end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for {query_params.smoothing_type} using cv2.blur is {time_taken:.4f} seconds")