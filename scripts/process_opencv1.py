import cv2
import time
import sys
import numpy as np
from imports.query_params import QueryParamsOpenCv
from imports.utils import get_cv_function
from imports.image import get_image, get_image_name_path, add_image_name_path_suffix


query_params = QueryParamsOpenCv(sys.argv)
print("TESTT: ")
image_name_path = get_image_name_path(query_params.image_name)
# image = get_image(image_name_path)

# get image from stdin
image_data = sys.stdin.buffer.read()
nparr = np.frombuffer(image_data, np.uint8)
image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

if image is None:
    print("Failed to decode image")
    sys.exit(1)

start_time = time.time()
image_blur = get_cv_function(image, query_params.smoothing_type, query_params.kernel_size)
end_time = time.time()

# write processed file
cv2.imwrite(add_image_name_path_suffix(image_name_path, query_params.smoothing_type), image_blur)

print(f"Time taken for {query_params.smoothing_type} using cv2.blur is {end_time - start_time:.4f} seconds")