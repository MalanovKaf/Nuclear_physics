import random
from math import sqrt
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Sphere_intersection:
    """
    Класс для моделирования изотропного источника и сферы
    """
    def __init__(self, X0, Y0, Z0, R, N):
        """
        Инициализация источника и сферы

        Parameters:
        X0, Y0: координаты центра сферы
        R: радиус сферы
        N: общее количество частиц
        """
        self.X0 = X0
        self.Y0 = Y0
        self.Z0 = Z0
        self.R = abs(R)
        self.N = abs(N)
        self.L = sqrt(self.X0**2 + self.Y0**2 + self.Z0**2)

    def SourceIzotrop(self):
        """
        Изотропный источник и направляющий вектор для луча с помощью l, m, n
        """
        v_all = np.zeros((self.N, 3))
        for i in range(self.N):
            while True:
                l = random.uniform(-1, 1)
                m = random.uniform(-1, 1)
                n = random.uniform(-1, 1)
                s_squared = l ** 2 + m ** 2 + n ** 2
                if s_squared <= 1:
                    break
            length = sqrt(s_squared)
            v_1 = np.array([l, m, n]) / length
            v_all[i] = v_1
        return v_all

    def intersection(self):
        """
        Вычисление вероятности пересечения сферы с частицей
        """
        NS=0
        V=self.SourceIzotrop()
        for component in V:
            b=2*(self.X0*component[0]+self.Y0*component[1]+self.Z0*component[2])
            c=self.X0**2+self.Y0**2+self.Z0**2-self.R**2
            D=(b**2)/4 -c
            if D>=0:
                t1,t2=b/2 +sqrt(D),b/2-sqrt(D)
                if t1>=0 and t2>=0:
                    NS+=1
        return NS/len(V)

    def distance_dependence(self, num_distances, max_distance):
        """
        Исследование зависимости вероятности от расстояния
        Parameters:
            num_distances (int): Количество точек для измерения
            max_distance (float): Максимальное расстояние от источника
        Returns:
           tuple: (массив расстояний, массив вероятностей)
        """
        distances = []
        probabilities = []
        orig_X, orig_Y, orig_Z = self.X0, self.Y0, self.Z0
        distances.append(self.R)
        probabilities.append(self.intersection())
        for i in range(num_distances):
            if i==0:
                L=self.R
            else:
                L = random.uniform(self.R, max_distance)
            self.X0 = L
            self.Y0 = 0
            self.Z0 = 0
            prob = self.intersection()
            distances.append(L)
            probabilities.append(prob)

            # Восстанавливаем исходные координаты
        self.X0, self.Y0, self.Z0 = orig_X, orig_Y, orig_Z
        return np.array(distances), np.array(probabilities)

    def plot_distance_dependence(self, num_distances, max_distance=None):
        """
        Построение графика зависимости вероятности от расстояния
        Parameters:
            num_distances (int): Количество точек для измерения
            max_distance (float, optional): Максимальное расстояние от источника.
        """
        if max_distance is None:
            max_distance = 5 * self.R
        distances, probabilities = self.distance_dependence(num_distances, max_distance)
        sort_idx = np.argsort(distances)
        distances = distances[sort_idx]
        probabilities = probabilities[sort_idx]
        plt.figure(figsize=(10, 6))
        plt.plot(distances, probabilities, 'bo-', markersize=4, linewidth=1)
        plt.xlabel('Расстояние от источника до центра сферы')
        plt.ylabel('Вероятность попадания')
        plt.title(f'Зависимость вероятности попадания от расстояния\nR={self.R}, N={self.N}')
        plt.grid(True)
        plt.show()

