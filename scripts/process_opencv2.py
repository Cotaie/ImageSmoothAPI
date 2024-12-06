
import time
import sys
from imports.query_params import QueryParamsOpenCv
from imports.image import get_image, get_image_name_path, add_image_name_path_suffix
from imports.utils import TIME_TAKEN_STRING, get_image_from_stdin, set_stdout, get_cv_function


print("DIN PYTHON")

query_params = QueryParamsOpenCv(sys.argv)

print(query_params)

image = get_image_from_stdin()
print("DIN PYTHONN")
start_time = time.time()
image_blur = get_cv_function(image, query_params.smoothing_type, query_params.kernel_size)
end_time = time.time()

time_taken = end_time - start_time

set_stdout(image_blur, query_params.image_name)

print(f"Time taken for {query_params.smoothing_type} using cv2.blur is {end_time - start_time:.4f} seconds")