from LabN7 import *

def test_cube_probability_d4_l0():
    """
    D = 4, L = 0 (источник в центре куба) -> вероятность 100%
    """
    cube = Cube_intersection(Xs=0, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    expected = 1.0
    assert abs(prob - expected) == 0

def test_cube_probability_d4_l2():
    """
    D = 4, L = 2 (источник на грани куба по X) -> вероятность 50%
    """
    cube = Cube_intersection(Xs=2, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    expected = 0.5
    assert abs(prob - expected) < 0.02, f"Expected ~{expected}, got {prob}"

def test_cube_probability_d4_l2_000001():
    """
    D = 4, L = 2.000001 (источник чуть дальше грани) -> вероятность чуть меньше 50%
    Точное значение неизвестно, но должно быть около 0.5
    """
    cube = Cube_intersection(Xs=2.000001, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    expected = 0.5
    assert abs(prob-expected)<0.02

def test_cube_edge_mid_xy():
    """Тест 5: середина ребра (2,2,0) -> 25%"""
    cube = Cube_intersection(Xs=2, Ys=2, Zs=0, D=4, N=20000)
    prob = cube.run_simulation()
    assert abs(prob - 0.25) < 0.03

def test_cube_vertex():
    """Тест 8: вершина (2,2,2) -> 12.5%"""
    cube = Cube_intersection(Xs=2, Ys=2, Zs=2, D=4, N=30000)
    prob = cube.run_simulation()
    assert abs(prob - 0.125) < 0.02

if __name__ == "__main__":
    test_cube_probability_d4_l0()
    test_cube_probability_d4_l2()
    test_cube_probability_d4_l2_000001()
    test_cube_edge_mid_xy()
    test_cube_vertex()
    print("Все тесты прошли успешно!")
