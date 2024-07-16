from typing import Callable

try:
    from .vectors import Vector, dot, sum_of_squares
except:
    from vectors import Vector, dot, sum_of_squares



def difference_quotient(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x)) / h