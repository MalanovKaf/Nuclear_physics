import numpy as np
import random
import sys
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
            numpy.ndarray: массив векторов размером (n, 3) в декартовых координатах
        """
        v_all = np.zeros((self.n, 3))
        for i in range(self.n):
            r = 1  # радиус сферы
            phi = 2 * np.pi * random.uniform(0, 1)
            theta = np.arccos(2 * random.uniform(0, 1) - 1)

            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)

            v_all[i] = np.array([x, y, z])
        return v_all

    def plot_vectors(self):
        """Построение 3D графика векторов на сфере."""
        vectors = self.vectors()

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        x = vectors[:, 0]
        y = vectors[:, 1]
        z = vectors[:, 2]

        ax.scatter(x, y, z, c='blue', marker='o', alpha=0.6, s=30)

        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        sphere_x = np.outer(np.cos(u), np.sin(v))
        sphere_y = np.outer(np.sin(u), np.sin(v))
        sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='gray', alpha=0.2)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Изотропное распределение {self.n} векторов на сфере')

        ax.set_box_aspect([1, 1, 1])

        plt.show()