from LabN7 import *
cube = Cube_intersection(Xs=2, Ys=0, Zs=0, D=4, N=4000)
print(cube.run_simulation())
cube.plot_distance_dependence(num_positions=20, random_range=(0.5, 6))