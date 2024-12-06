import sys
import time
from imports.query_params import QueryParamsOpenCv
from imports.utils import get_image_from_stdin, set_stdout, get_cv_function


query_params = QueryParamsOpenCv(sys.argv)
image = get_image_from_stdin()

start_time = time.time()
image_blur = get_cv_function(image, query_params.smoothing_type, query_params.kernel_size)
end_time = time.time()

time_taken = end_time - start_time
set_stdout(image_blur, query_params.image_name)
print(f"Time taken for {query_params.smoothing_type} using cv2.blur is {time_taken:.4f} seconds")