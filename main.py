from LabN7 import *

cube = CubeIntersection(Xs=1.0, Ys=1, Zs=1, D=2.0, N=5000)

# Запуск моделирования
probability = cube.run_simulation()
print(f"Вероятность попадания: {probability:.4f} ({probability * 100:.2f}%)")

# Построение зависимости от расстояния
print("\nПостроение зависимости от расстояния...")
cube.plot_distance_dependence(num_points=70, N_mc=5000)
