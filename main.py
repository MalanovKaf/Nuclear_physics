from labN2 import Figure
import math
import numpy as np

triangle = Figure([[2, 0], [2, 5]])
A = B = 10
N = 1000
ITER = 10

squares = [triangle.square(A, B, N) for i in range(ITER)]
print("Дисперсия через numpy:", np.var(squares, ddof=1))
print("Мат ожидание через numpy:", np.mean(squares))
print("Площадь (Монте-Карло):", squares)
print("Мат. ожидание:", triangle.mathematical_expectation(ITER, A, B, N))
print("Дисперсия:", triangle.dispersion(ITER, A, B, N))
