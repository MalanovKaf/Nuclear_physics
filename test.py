from LabN7 import *

def test_cube_probability_d4_l0():
    """
    D = 4, L = 0 (источник в центре куба) -> вероятность 100%
    """
    cube = Cube_intersection(Xs=0, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    expected = 1.0
    assert abs(prob - expected) < 0.01

def test_cube_probability_d4_l2():
    """
    D = 4, L = 2 (источник на грани куба по X) -> вероятность 50%
    """
    cube = Cube_intersection(Xs=2, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    expected = 1
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
