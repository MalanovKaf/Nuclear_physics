import random
from math import *
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Source_izotrop(object):

    def __init__(self,N):
        self.N=N
        if N<=0:
            sys.exit("Количество векторов не может быть 0 или меньше 0")

    def vectors(self):
        v_all = np.zeros((self.N, 3))
        for i in range(self.N):
            while True:
                l = random.uniform(-1, 1)
                m = random.uniform(-1, 1)
                n = random.uniform(-1, 1)
                s_squared = l ** 2 + m ** 2 + n ** 2
                if s_squared <= 1 and s_squared > 0:
                    break
            length = sqrt(s_squared)
            v_1 = np.array([l, m, n]) / length
            v_all[i] = v_1
        return v_all

    def plot_vectors(self):
        """Метод для построения 3D графика векторов"""
        vectors = self.vectors()

        # Создаю 3D график
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Координаты для построения точек
        x = vectors[:, 0]
        y = vectors[:, 1]
        z = vectors[:, 2]

        # Строю точки на сфере
        ax.scatter(x, y, z, c='blue', marker='o', alpha=0.6, s=30)

        # Настройка графика
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Изотропное распределение {self.N} векторов на сфере')

        plt.show()