from LabN7 import *

cube = CubeIntersection(Xs=3.0, Ys=0, Zs=0, D=4, N=5000)

probability = cube.run_simulation()
print(f"Вероятность попадания: {probability:.4f} ({probability * 100:.2f}%)")

print("\nПостроение зависимости от расстояния...")
cube.plot_distance_dependence(num_points=50, N_mc=1000)
