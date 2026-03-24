from LabN7 import *

cube = CubeIntersection(Xs=3.0, Ys=0, Zs=0, D=4, N=5000)

# Запуск моделирования
probability = cube.run_simulation()
print(f"Вероятность попадания: {probability:.4f} ({probability * 100:.2f}%)")

# Построение зависимости от расстояния
print("\nПостроение зависимости от расстояния...")
cube.plot_distance_dependence(num_points=40, N_mc=4000)
