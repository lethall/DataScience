from typing import Callable

try:
    from .vectors import Vector, dot, sum_of_squares
except:
    from vectors import Vector, dot, sum_of_squares



def difference_quotient(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x)) / h

def square(x: float) -> float:
    return x * x

def derivative(x: float) -> float:
    return 2 * x

def partial_difference_quotient(f: Callable[[Vector], float], v: Vector, i: int, h: float) -> float:
    """Returns the i-th partial difference quotient of f at v"""
    
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    
    return (f(w) - f(v)) / h

def estimates_gradient(f: Callable[[Vector], float], v: Vector, h: float = 0.0001):
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))]