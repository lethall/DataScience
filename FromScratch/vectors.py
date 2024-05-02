from typing import List, Tuple, Callable
import math

Vector = List[float]
Matrix = List[List[float]]

def add(v: Vector, w: Vector) -> Vector:
    """Adds corresponding elements"""
    assert len(v) == len(w), "Vectors must be the same length"
    
    return [v_i + w_i for v_i, w_i in zip(v, w)]

assert add([1, 10], [4, 10]) == [5, 20]

def subtract(v: Vector, w: Vector) -> Vector:
    """Subtracts corresponding elements"""
    assert len(v) == len(w), "Vectors must be the same length"
    
    return [v_i - w_i for v_i, w_i in zip(v, w)]

assert subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]

def vector_sum(vectors: List[Vector]) -> Vector:
    """Sums all corresponding elements"""
    assert vectors, "No vectors provided"
    
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors),  "Diffrent sized vectors"
    
    return [sum(vector[i] for vector in vectors) for i in range(num_elements)]

numbers = [[1, 2], [4, 3], [7, 8], [6, 5]]
assert vector_sum(numbers) == [18, 18]

def scalar_multiply(c: float, v: Vector) -> Vector:
    """Multiplies every element by c"""
    return [c * v_i for v_i in v]

assert scalar_multiply(3, numbers[1]) == [12, 9]

def vector_mean(vectors: List[Vector]) -> Vector:
    """Computes the element-wise average"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

assert vector_mean([[1, 2], [3, 4], [5, 6]]) == [3, 4]

def dot(v: Vector, w: Vector) -> float:
    """Computes each dimension of v times the dimension of w and sums them all"""
    assert len(v) == len(w), "vectors must be the same length"
    
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

assert dot([1, 2, 3], [4, 5, 6]) == 32

def sum_of_squares(v: Vector) -> float:
    """Returns sum of each dimension multiplied by itself"""
    return dot(v, v)

assert sum_of_squares([1, 2, 3]) == 14

def magnitude(v: Vector) -> float:
    """Return the magnitude (or length) of v"""
    return math.sqrt(sum_of_squares(v))

assert magnitude([3, 4]) == 5

def squared_distance(v:Vector, w: Vector) -> float:
    """Computes (v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(subtract(v, w))

assert squared_distance([2, 5], [5, 8]) == 18

def distance(v: Vector, w: Vector) -> float:
    """Computes the distance between v and w"""
    return magnitude(subtract(v, w))

assert distance([5, 6], [8, 10]) == 5

def shape(A: Matrix) -> Tuple[int, int]:
    """Returns (number of rows, number of columns of A)"""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)
assert shape([[],[],[]]) == (3, 0)

def get_column(A: Matrix, j: int) -> Vector:
    return [row[j] for row in A]

assert get_column([[1, 3, 5], [4, 6, 3], [11, 9, 2]], 2) == [5, 3, 2]

def make_matrix(num_rows: int, num_cols: int, entry_fn: Callable[[int, int], float]) -> Matrix:
    """Returns a num_rows x num_cols matrix whose (i, j)-th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_rows)]

def identity_matrix(n: int) -> Matrix:
    def set0(i, j) -> float:
        if i == j: return 1
        else: return 0
            
    return make_matrix(n, n, set0)

assert identity_matrix(5) == [[1, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 1]]