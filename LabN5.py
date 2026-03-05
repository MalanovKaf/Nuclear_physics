import random
from math import sqrt
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Source_photon:
    """
    Класс для моделирования источника фотонов с тремя возможными энергиями
    """

    def __init__(self, P1, P2, P3, E1, E2, E3, N):
        """
        Инициализация источника фотонов

        Parameters:
        P1, P2, P3: вероятности выхода фотонов с энергиями E1, E2, E3
        E1, E2, E3: значения энергий фотонов
        N: общее количество фотонов
        """
        self.P1 = abs(P1)
        self.P2 = abs(P2)
        self.P3 = abs(P3)
        self.E1 = abs(E1)
        self.E2 = abs(E2)
        self.E3 = abs(E3)
        self.N = abs(N)
        if self.P1 + self.P2 + self.P3 != 1:
            sys.exit("Сумма выходов источника должна быть 1")

    def Energy_diagramma(self):
        """
        Генерация распределения фотонов по энергиям и построение гистограммы
        """
        N1 = 0
        N2 = 0
        N3 = 0
        for i in range(self.N):
            G = random.uniform(0, 1)
            if G < self.P1:
                N1 += 1
            elif G < self.P1 + self.P2:
                N2 += 1
            else:
                N3 += 1
        error1, error2, error3 = sqrt(N1) / self.N, sqrt(N2) / self.N, sqrt(N3) / self.N
        N1, N2, N3 = N1 / self.N, N2 / self.N, N3 / self.N
        self.plot_histogram(N1, N2, N3, error1, error2, error3)

    def plot_histogram(self, N1, N2, N3, error1, error2, error3):
        """
        Построение гистограммы распределения фотонов по энергиям
        Parameters:
        n1, n2, n3: количество фотонов с каждой энергией
        """
        energies = [self.E1, self.E2, self.E3]
        counts = [N1, N2, N3]
        errors = [error1, error2, error3]

        # Создание фигуры
        plt.figure(figsize=(10, 6))

        # Столбчатая диаграмма (количество фотонов)
        bars = plt.bar(range(len(energies)), counts, yerr=errors, capsize=5, color=['blue', 'green', 'red'], alpha=0.7,
                       error_kw={'elinewidth': 1, 'ecolor': 'black'})

        # Настройка графика
        plt.xlabel('Энергия фотонов')
        plt.ylabel('Количество фотонов')
        plt.title('Распределение фотонов по энергиям')
        plt.xticks(range(len(energies)), [f'E1={self.E1}', f'E2={self.E2}', f'E3={self.E3}'])

        # Добавление значений над столбцами
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + 0.01 * max(counts), f'{count}', ha='center',
                     va='bottom', fontsize=11, fontweight='bold')

        # Добавление сетки для лучшей читаемости
        plt.tight_layout()
        plt.show()
