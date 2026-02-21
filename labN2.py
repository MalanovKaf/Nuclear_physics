import random
from math import *
import sys
from tabnanny import check

import numpy as np


class Figure(object):
    """Класс для представления геометрической фигуры"""

    def __init__(self,vertices):
        """
        Инициализация n-угольника.
        Args:
            vertices (array): заданынй массив вершин n-угольника
        """
        self.vertices = np.array(vertices)
        if self.check_orientation()>0:
            sys.exit('Ошибка:точки должны задаваться по часовой стрелке ')

    def check_orientation(self):
        """
        Определение ориентации многоугольника
        Возвращает:
            > 0: против часовой стрелки
            < 0: по часовой стрелке
            = 0: точки коллинеарны
        """
        n = len(self.vertices)
        if n < 3:
            return 0  # Для линии или точки
        area2 = 0
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            area2 += (x1 * y2 - x2 * y1)
        return area2  # Знак показывает ориентацию


    def square(self,A,B,N):
        """
        Вычисление площади n-угольника методом Монте-Карло.
        Args:
            A (float): ширина прямоугольной области
            B (float): высота прямоугольной области
            N (int): количество случайных точек
        Return:
            float: приблизительная площадь n-угольника
        """
        try:
            x_coords = [v[0] for v in self.vertices]
            y_coords = [v[1] for v in self.vertices]

            if (max(x_coords) > A or max(y_coords) > B or min(x_coords) < 0 or min(y_coords) < 0):
                sys.exit('Ошибка:n-угольник не в прямоугольнике')
            N0=0
            for i in range(N):
                x_i = random.uniform(0, A)
                y_i = random.uniform(0, B)

        except (TypeError, ValueError):
            print("Ошибка при выполнении")


    def mathematical_expectation(self,iteration, A, B, N):
        """
        Вычисление математического ожидания площади.
        Args:
            iteration (int): количество итераций
            A (float): ширина прямоугольной области
            B (float): высота прямоугольной области
            N (int): количество случайных точек на итерацию
        Return:
            float: математическое ожидание площади
        """
        try:
            squares=[self.square(A,B,N) for i in range (iteration)]
            return sum(squares)/iteration
        except (TypeError, ValueError):
            print("Ошибка при выполнении")


    def dispersion(self,iteration, A, B, N):
        """
        Вычисление дисперсии площади.
        Args:
            iteration (int): количество итераций
            A (float): ширина прямоугольной области
            B (float): высота прямоугольной области
            N (int): количество случайных точек на итерацию
        Return:
            float: дисперсия площади
        """
        try:
            squares = [self.square(A, B, N) for i in range(iteration)]
            mean=sum(squares)/iteration
            squared_mean = sum(s ** 2 for s in squares)/iteration
            return squared_mean - mean ** 2
        except (TypeError, ValueError):
            print("Ошибка при выполнении")