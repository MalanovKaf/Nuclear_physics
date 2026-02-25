import random
from math import sqrt
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SourceIzotrop:
    """
    Класс для генерации изотропно распределенных векторов на сфере.
    """

    def __init__(self, n):
        """
        Инициализация генератора векторов.

        Args:
            n: количество векторов для генерации
        """
        self.n = n
        if n <= 0:
            sys.exit("Количество векторов не может быть 0 или меньше 0")

    def vectors(self):
        """
        Генерация изотропно распределенных векторов на сфере.

        Returns:
            numpy.ndarray: массив векторов размером (n, 3)
        """
        v_all = np.zeros((self.n, 3))
        for i in range(self.n):
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
        """Построение 3D графика векторов на сфере."""
        vectors = self.vectors()

        # Создание 3D графика
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Координаты для построения точек
        x = vectors[:, 0]
        y = vectors[:, 1]
        z = vectors[:, 2]

        # Построение точек на сфере
        ax.scatter(x, y, z, c='blue', marker='o', alpha=0.6, s=30)

        # Добавление сферы для наглядности
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        sphere_x = np.outer(np.cos(u), np.sin(v))
        sphere_y = np.outer(np.sin(u), np.sin(v))
        sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='gray', alpha=0.2)

        # Настройка графика
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Изотропное распределение {self.n} векторов на сфере')

        plt.show()