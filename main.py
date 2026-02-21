from labN1 import Figure
import math
import numpy as np

circle = Figure(1, 5, 5)
A = B = 10
N = 10000
ITER = 10

squares=[circle.square(A, B, N) for _ in range(ITER)]
print("Дисперсия через numpy:",np.var(squares, ddof=1))
print ("Мат ожидание через numpy:",np.mean(squares))
print("Площадь круга (теор):", math.pi)
print("Площадь (Монте-Карло):", squares)
print("Мат. ожидание:", circle.mathematical_expectation(ITER, A, B, N))
print("Дисперсия:", circle.dispersion(ITER, A, B, N))