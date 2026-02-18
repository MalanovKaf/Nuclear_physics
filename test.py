from labN1 import Figure
import math
import random


def test_figure_creation():
    """Тест создания фигуры с корректными параметрами"""
    circle = Figure(5, 2, 3)
    assert circle.radius == 5
    assert circle.x0 == 2
    assert circle.y0 == 3


def test_figure_creation_string_parameters():
    """Тест создания фигуры со строковыми параметрами"""
    circle = Figure("5", "2", "3")
    assert circle.radius == 5
    assert circle.x0 == 2
    assert circle.y0 == 3


def test_square_calculation_basic():
    """Тест базового вычисления площади методом Монте-Карло"""
    circle = Figure(2, 5, 5)
    area = circle.square(10, 10, 1000)
    assert 10 < area < 15


def test_full_coverage():
    """Тест когда круг покрывает весь прямоугольник"""
    circle = Figure(10, 5, 5)
    area = circle.square(10, 10, 1000)
    assert abs(area - 100) < 10


def test_no_coverage():
    """Тест когда круг не попадает в прямоугольник"""
    circle = Figure(1, -10, -10)
    area = circle.square(10, 10, 1000)
    assert area == 0


def test_mathematical_expectation_convergence():
    """Тест сходимости математического ожидания"""
    circle = Figure(2, 5, 5)
    exp1 = circle.mathematical_expectation(10, 10, 10, 100)
    exp2 = circle.mathematical_expectation(50, 10, 10, 500)
    assert abs(exp1 - exp2) < 5


def test_dispersion_calculation():
    """Тест вычисления дисперсии"""
    circle = Figure(2, 5, 5)
    disp = circle.dispersion(50, 10, 10, 500)
    assert disp >= 0
    assert isinstance(disp, float)


if __name__ == "__main__":
    test_figure_creation()
    test_figure_creation_string_parameters()
    test_square_calculation_basic()
    test_full_coverage()
    test_no_coverage()
    test_mathematical_expectation_convergence()
    test_dispersion_calculation()
    print("Все тесты прошли успешно!")