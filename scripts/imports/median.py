import numpy as np
import math
from collections import Counter


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
        for i in range(n - kernel_size + 1):
            for j in range(m - kernel_size + 1):
                submatrix = [row[j:j + kernel_size] for row in image[i:i + kernel_size]]
                histogram = Median.get_histogram(submatrix)
                image_blur[i,j] = Median.get_median_value(histogram)

        return image_blur
    @staticmethod
    def __is_odd(number: int) -> bool:
        return number%2 != 0
    @staticmethod
    def __get_mean(number1: int, number2: int) -> float:
        return (number1+number2) / 2
    @staticmethod
    def get_median(his: Counter):
        nr_elements = len(his)
        if Median.__is_odd(len(his)):
            mid = math.floor(nr_elements/2)
            return his.most_common()[mid][0]
        else:
            print(nr_elements/2.)
            mid1 = int(nr_elements/2) - 1
            print(f"mid1 {mid1}")
            mid2 = int(nr_elements/2)
            print(f"mid1 {mid2}")
            return Median.__get_mean(his.most_common()[mid1][0], his.most_common()[mid2][0])
        
        
