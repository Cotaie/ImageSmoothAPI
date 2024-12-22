import numpy as np
import math


class Median:
    @staticmethod
    def get_histogram(submatrix: np.ndarray):
        histogram: dict[int, int] = {}
        for row in submatrix:
            for el in row:
                if el in histogram:
                    histogram[el] += 1
                else:
                    histogram[el] = 1

        return histogram

    @staticmethod
    def get_median_value(histogram: dict[int,int]):
        return histogram[np.median(histogram.values())]

    @staticmethod
    def standard(image: np.ndarray, image_blur: np.ndarray, kernel_size: int):
        n = image.shape[0]
        m = image.shape[1]
        for i in range(n - kernel_size + 1):        # Row indices
            for j in range(m - kernel_size + 1):    # Column indices
                # Extract the k x k submatrix using slicing
                submatrix = [row[j:j + kernel_size] for row in image[i:i + kernel_size]]
                histogram = Median.get_histogram(submatrix)
                image_blur[i,j] = Median.get_median_value(histogram)

        return image_blur
        
        
