import sys
import time
import numpy as np
from imports.median import Median
from imports.imports import MedianType, QueryParamsMedian, ImageType
from imports.utils import get_image_from_stdin, set_stdout, get_image_type, get_shape_output, get_border_mode_value


def get_median_type_result(subimage: np.ndarray, median_type: MedianType):
    match median_type:
        case MedianType.STANDARD:
            histogram = Median.get_histogram(subimage)
            return Median.get_median_value(histogram)
        case _:
            raise ValueError(f"Unsupported kernel type: '{median_type}'")

query_params = QueryParamsMedian(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
image_type = get_image_type(image.shape)
image_blur = get_shape_output(query_params.border_mode, query_params.kernel_size, image.shape, image_type)
border_mode_value = get_border_mode_value(query_params.border_mode, query_params.kernel_size)

match image_type:
    case ImageType.GRAYSCALE:
        for i in range(image.shape[0] + border_mode_value):
            for j in range(image.shape[1] + border_mode_value):
                submatrix = np.array([row[j:j + query_params.kernel_size] for row in image[i:i + query_params.kernel_size]])
                match query_params.median_type:
                    case MedianType.STANDARD:
                        histogram = Median.get_histogram(submatrix)
                        image_blur[i,j] = Median.get_median_value(histogram)



# for channel in range(no_channels):
#     n = image.shape[0]
#     m = image.shape[1]
#     for i in range(n - query_params.kernel_size + 1):        # Row indices
#         for j in range(m - query_params.kernel_size + 1):    # Column indices
#             # Extract the k x k submatrix using slicing
#             submatrix = np.array([row[j:j + query_params.kernel_size] for row in image[i:i + query_params.kernel_size]])
#             image_blur[i,j,channel] = get_median_type_result(submatrix, query_params.median_type)

end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for {query_params.smoothing_type} using cv2.blur is {time_taken:.4f} seconds")