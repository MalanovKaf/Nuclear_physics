from labN2 import Figure
import math
import random


def test_square_rectangle():
    """Тест для прямоугольника"""
    rectangle = Figure([[2, 2], [6, 2], [6, 4], [2, 4]])
    A = B = 10
    N = 10000
    # Площадь прямоугольника = 4 * 4 = 8
    assert abs(rectangle.square(A, B, N) - 8) < 1


def test_square_triangle():
    """Тест для треугольника"""
    triangle = Figure([[2, 2], [6, 2], [4, 6]])
    A = B = 10
    N = 10000
    # Площадь треугольника = (4 * 4) / 2 = 8
    area = triangle.square(A, B, N)
    assert abs(area - 8) < 1


def test_square_pentagon():
    """Тест для пятиугольника"""
    pentagon = Figure([[3, 2], [7, 2], [8, 5], [5, 7], [2, 5]])
    A = B = 10
    N = 10000
    # Для данного пятиугольника примерная площадь 20
    area = pentagon.square(A, B, N)
    assert abs(area - 20) < 2, f"Площадь пятиугольника {area} отличается от ожидаемой 20"


def test_dispersion():
    """Тест дисперсии"""
    rectangle = Figure([[2, 2], [6, 2], [6, 4], [2, 4]])
    A = B = 10
    N = 1000
    iteration = 50

    dispersion = rectangle.dispersion(iteration, A, B, N)
    # Дисперсия должна быть положительной
    assert dispersion > 0
    # При увеличении N дисперсия должна уменьшаться
    dispersion_small_N = rectangle.dispersion(iteration, A, B, 100)
    dispersion_large_N = rectangle.dispersion(iteration, A, B, 10000)
    assert dispersion_large_N < dispersion_small_N


if __name__ == "__main__":
    test_square_rectangle()
    test_square_triangle()
    test_square_pentagon()
    test_dispersion()
    print("Все тесты прошли успешно!")
