from labN1 import Figure
import math

circle = Figure(1, 5, 5)
A = B = 10
N = 10000
ITER = 10

print("Площадь круга (теор):", math.pi)
print("Площадь (Монте-Карло):", [circle.square(A, B, N) for _ in range(ITER)])
print("Мат. ожидание:", circle.mathematical_expectation(ITER, A, B, N))
print("Дисперсия:", circle.dispersion(ITER, A, B, N))