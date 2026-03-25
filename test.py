from LabN7 import *

def test_cube_probability_d4_l0():
    """
    D = 4, L = 0 (источник в центре куба) -> вероятность 100%
    """
    cube = CubeIntersection(Xs=0, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    print(f"Вероятность попадания внутри: {prob:.4f} ({prob * 100:.2f}%)")
    expected = 1.0
    assert abs(prob - expected) == 0

def test_cube_probability_d4_l2():
    """
    D = 4, L = 2 (источник на грани куба по X) -> вероятность 50%
    """
    cube = CubeIntersection(Xs=2, Ys=0, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    print(f"Вероятность попадания на грани: {prob:.4f} ({prob * 100:.2f}%)")
    expected = 0.5
    assert abs(prob - expected) == 0

def test_cube_edge_mid_xy():
    """Тест 5: середина ребра (2,2,0) -> 25%"""
    cube = CubeIntersection(Xs=2, Ys=2, Zs=0, D=4, N=10000)
    prob = cube.run_simulation()
    print(f"Вероятность попадания на середине ребра: {prob:.4f} ({prob * 100:.2f}%)")
    assert abs(prob - 0.25) < 0.03

def test_cube_vertex():
    """Тест 8: вершина (2,2,2) -> 12.5%"""
    cube = CubeIntersection(Xs=2, Ys=2, Zs=2, D=4, N=10000)
    prob = cube.run_simulation()
    print(f"Вероятность попадания в вершине: {prob:.4f} ({prob * 100:.2f}%)")
    assert abs(prob - 0.125) < 0.02

if __name__ == "__main__":
    test_cube_probability_d4_l0()
    print("Тест 1 прошел успешно")
    test_cube_probability_d4_l2()
    print("Тест 2 прошел успешно")
    test_cube_edge_mid_xy()
    print("Тест 3 прошел успешно")
    test_cube_vertex()
    print("Тест 4 прошел успешно")
    print("Все тесты прошли успешно!")
