import random
from math import *
class Figure(object):
    """Класс для представления геометрической фигуры (круга)"""

    def __init__(self,radius,x0,y0):
        """
        Инициализация круга.
        Args:
            radius (float): радиус круга
            x0 (float): x-координата центра
            y0 (float): y-координата центра
        """
        self.x0=float(x0)
        self.y0=float(y0)
        self.radius = float(radius)
        if self.radius<=0:
            raise ValueError("Радиус должен быть положительным числом")


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
            N0=0
            for i in range(N):
                x_i = random.uniform(0, A)
                y_i = random.uniform(0, B)
                L = sqrt((self.x0 - x_i) ** 2 + (self.y0 - y_i) ** 2)
                if L <= self.radius:
                    N0 += 1
            return A * B * N0 / N
        except (TypeError, ValueError):
            print("Ошибка при выполнении удара")


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
            print("Ошибка при выполнении удара")


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
            print("Ошибка при выполнении удара")

