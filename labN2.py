import random
from math import *
import sys
import numpy as np


class Figure(object):
    """Класс для представления геометрической фигуры"""

    def __init__(self,x,y):
        """
        Инициализация n-угольника.
        Args:
            x (array): x-координаты заданного n-угольника
            y (array): y-координаты заданного n-угольника
        """
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        if len(x) != len(y):
            raise ValueError("Массивы x и y должны быть одинаковой длины")


    def square(self,A,B,N):
        """
        Вычисление площади круга методом Монте-Карло.
        Args:
            A (float): ширина прямоугольной области
            B (float): высота прямоугольной области
            N (int): количество случайных точек
        Return:
            float: приблизительная площадь круга
        """
        try:
            if max(self.x) > A or max(self.y) > B or min(self.x)<0 or min(self.y)<0:
                sys.exit('Ошибка:n-угольник не в прямоугольнике')
            N0=0
            for i in range(N):
                x_i = random.uniform(0, A)
                y_i = random.uniform(0, B)
                L = sqrt((self.x0 - x_i) ** 2 + (self.y0 - y_i) ** 2)
                if L <= self.radius:
                    N0 += 1
            return A * B * N0 / N
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