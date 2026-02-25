from labN2 import Figure
import math
import numpy as np

triangle = Figure([[2,4],[4,6],[6,4],[6,2],[2,2]])
A = B = 10
N = 10000
ITER = 10

squares=[triangle.square(A, B, N) for _ in range(ITER)]
print("Дисперсия через numpy:",np.var(squares, ddof=1))
print ("Мат ожидание через numpy:",np.mean(squares))
print("Площадь (Монте-Карло):", squares)
print("Мат. ожидание:", triangle.mathematical_expectation(ITER, A, B, N))
print("Дисперсия:", triangle.dispersion(ITER, A, B, N))