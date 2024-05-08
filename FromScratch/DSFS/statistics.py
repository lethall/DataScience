from collections import Counter
from typing import List
from vectors import sum_of_squares
import math

def mean(xs: List[float]) -> float:
    """Return mean of list"""
    return sum(xs) / len(xs)

# 
# def _median_odd(xs: List[float]) -> float:
#     """If len(xs) is odd, the median is the middle element"""
#     return sorted(xs)[len(xs) // 2]

# def _median_even(xs: list[float]) -> float:
#     """If len(xs) is even, it's the average of the middle two elements"""
#     sorted_xs = sorted(xs)
#     hi_midpoint = len(xs) // 2
#     return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2

# def median(v: List[float]) -> float:
#     """Find the 'middle-most' value of v"""
#     return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)

def median(v: List[float]) -> float:
    """Find the 'middle-most value of v"""
    if len(v) % 2 == 0:
        sorted_v = sorted(v)
        hi_midpoint = len(v) // 2
        return (sorted_v[hi_midpoint - 1] + sorted_v[hi_midpoint]) / 2
    
    else:
        return sorted(v)[len(v) // 2]
 

def mode(x: List[float]) -> List[float]:
    """Returns a list of the modes"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

def quantile(xs: List[float], p: float) -> float:
    """Returns a p-th-percentile value in x"""
    p = p / 100
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]

def data_range(xs: List[float]) -> float:
    return max(xs) - min(xs)

def de_mean(xs: List[float]) -> List[float]:
    """Translate xs by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(xs)
    return [x - x_bar for x in xs]
    
    
def variance(xs: List[float]) -> float:
    """Almost the average squared deviation from the mean"""
    assert len(xs) >= 2, "Variance requires at least two elements"

    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n - 1)

def standard_deviation(xs: List[float]) -> float:
    """The standard deviation is the square root of the variance"""
    return math.sqrt(variance(xs))

def interquantile_range(xs: List[float]) -> float:
    """Returns the difference between the 75%-ile and the 25%-ile"""
    return quantile(xs, 75) - quantile(xs, 25)



if __name__ == "__main__":
    num_friends = [100,49,41,40,25,21,21,19,
               19,18,18,16,15,15,15,15,
               14,14,13,13,13,13,12,12,
               11,10,10,10,10,10,10,10,
               10,10,10,10,10,10,10,10,
               9,9,9,9,9,9,9,9,9,9,9,9,
               9,9,9,9,9,9,8,8,8,8,8,8,
               8,8,8,8,8,8,8,7,7,7,7,7,
               7,7,7,7,7,7,7,7,7,7,6,6,
               6,6,6,6,6,6,6,6,6,6,6,6,
               6,6,6,6,6,6,6,6,5,5,5,5,
               5,5,5,5,5,5,5,5,5,5,5,5,
               5,4,4,4,4,4,4,4,4,4,4,4,
               4,4,4,4,4,4,4,4,4,3,3,3,
               3,3,3,3,3,3,3,3,3,3,3,3,
               3,3,3,3,3,2,2,2,2,2,2,2,
               2,2,2,2,2,2,2,2,2,2,1,1,
               1,1,1,1,1,1,1,1,1,1,1,1,
               1,1,1,1,1,1,1,1]
    
    assert median([1, 10, 2, 9, 5]) == 5
    assert median([1, 9, 2, 10]) == (2 + 9) / 2
      
    assert quantile(num_friends, 10) == 1
    assert quantile(num_friends, 25) == 3
    assert quantile(num_friends, 75) == 9
    assert quantile(num_friends, 90) == 13
    
    assert data_range(num_friends) == 99
    
    assert 81.54 < variance(num_friends) < 81.55
    
    assert 9.03 < standard_deviation(num_friends) < 9.04
    
    assert interquantile_range(num_friends) == 6