from typing import Callable, TypeVar, List, Iterator

import random

try:
    from .vectors import Vector, dot, sum_of_squares
except:
    from vectors import Vector, dot, sum_of_squares

T = TypeVar('T')

def difference_quotient(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x)) / h


def square(x: float) -> float:
    return x * x


def derivative(x: float) -> float:
    return 2 * x

def partial_difference_quotient(f: Callable[[Vector], float], v: Vector, i: int, h: float) -> float:
    """Returns the i-th partial difference quotient of f at v"""
    
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    print(w)
    
    return (f(w) - f(v)) / h


def estimates_gradient(f: Callable[[Vector], float], v: Vector, h: float = 0.0001):
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))]


def linear_gradient(x: float, y: float, theta: Vector) -> Vector:
    assert len(theta) == 2, "Theta must be two values"
    
    slope, intercept = theta
    predicted = slope * x + intercept
    error = (predicted - y)
    grad = [2 * error * x, 2 * error]
    return grad


def minibatch(dataset: List[T], batch_size: int, shuffle: bool = True) -> Iterator[List[T]]:

    batch_starts = [start for start in range(0, len(dataset), batch_size)]
    
    if shuffle: random.shuffle(batch_starts)

    for start in batch_starts:
        end = start + batch_size
        yield dataset[start:end]
        

def is_between(value: float, target: float, epsilon = 0) -> bool:
    """True if value is within epsilon of target, inclusive"""
       
    setLow = target - epsilon
    setHigh = target + epsilon
        
    if setLow <= value <= setHigh:
        return True
    else:
        return False
    