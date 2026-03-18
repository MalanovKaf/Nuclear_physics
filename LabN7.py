import random
from math import sqrt
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Cube_intersection:
    """
    Класс для моделирования изотропного источника и куба
    """
    def __init__(self, Xs,Ys,Zs, D, N):
        """
        Инициализация источника и куба

        Parameters:
        L: расстояние от источника до центра куба
        D: длина ребра
        N: общее количество частиц
        """
        self.Xs = Xs
        self.Ys = Ys
        self.Zs = Zs
        self.L=sqrt(Xs**2+Ys**2+Zs**2)
        self.N = abs(N)
        d=D/2
        P = np.array([
            [d, d, d, d, -d, -d, -d, -d],
            [d, d, -d, -d, d, d, -d, -d],
            [d, -d, d, -d, d, -d, d, -d]
        ])

        vertices=P.T
        self.G=[
    [vertices[0], vertices[1], vertices[2], vertices[3], vertices[0]],  # G1: P1,P2,P4,P3,P1
    [vertices[4], vertices[5], vertices[7], vertices[6], vertices[4]],  # G2: P5,P6,P8,P7,P5
    [vertices[0], vertices[3], vertices[7], vertices[4], vertices[0]],  # G3: P1,P4,P8,P5,P1
    [vertices[1], vertices[2], vertices[6], vertices[5], vertices[1]],  # G4: P2,P3,P7,P6,P2
    [vertices[0], vertices[4], vertices[5], vertices[1], vertices[0]],  # G5: P1,P5,P6,P2,P1
    [vertices[3], vertices[7], vertices[6], vertices[2], vertices[3]]   # G6: P4,P8,P7,P3,P4
                ]
        self.P=vertices

    def ray(self):
        """
        Изотропный источник и направляющий вектор для луча с помощью l, m, n
        """
        v_all = np.zeros((self.N, 3))
        for i in range(self.N):
            while True:
                l = random.uniform(-1, 1)
                m = random.uniform(-1, 1)
                n = random.uniform(-1, 1)
                s_squared = l ** 2 + m ** 2 + n ** 2
                if s_squared <= 1:
                    break
            length = sqrt(s_squared)
            v_1 = np.array([l, m, n]) / length
            v_all[i] = v_1
        return v_all

    def flateABCD (self,P1,P2,P3):
        A=np.linalg.det([[P1[1],P1[2],1], [P2[1],P2[2],1], [P3[1],P3[2],1]])
        B = np.linalg.det([[P1[2], P1[0], 1], [P2[2], P2[0], 1], [P3[2], P3[0], 1]])
        C = np.linalg.det([[P1[0], P1[1], 1], [P2[0], P2[1], 1], [P3[0], P3[1], 1]])
        D = np.linalg.det([[P1[2], P1[0], P1[1]], [P2[2], P2[0], P2[1]], [P3[2], P3[0], P3[1]]])
        return [A,B,C,D]

    def cross(self, Ray, F):
        """
        Нахождение точки пересечения луча с плоскостью
        Ray: направляющий вектор луча
        F: коэффициенты плоскости [A, B, C, D]
        """
        denominator = F[0] * Ray[0] + F[1] * Ray[1] + F[2] * Ray[2]
        # Проверка на параллельность (знаменатель близок к нулю)
        if abs(denominator) < 1e-10:
            return None
        t = -(F[0] * self.Xs + F[1] * self.Ys + F[2] * self.Zs + F[3]) / denominator
        if t >= 0:
            P_cross = [self.Xs + t * Ray[0],
                       self.Ys + t * Ray[1],
                       self.Zs + t * Ray[2]]
            return P_cross
        else:
            return None

    @staticmethod
    def point_in_polygon(point, polygon):
        """
        Проверка, лежит ли точка внутри многоугольника
        polygon: список точек [(x1,y1), (x2,y2), ...]
        """
        x, y = point
        inside = False
        n = len(polygon)
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside

    def inside(self, P_cross, face_vertices):
        """
        Лежит ли точка пересечения внутри указанной грани куба
        P_cross: точка пересечения (x, y, z)
        face_vertices: вершины конкретной грани
        Returns:
        True если точка внутри грани, иначе False
        """
        # Получаем нормаль грани для определения проекции
        v1 = np.array(face_vertices[1]) - np.array(face_vertices[0])
        v2 = np.array(face_vertices[2]) - np.array(face_vertices[0])
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)

        # Определяем, по какой оси проецировать (выбираем ось с максимальной компонентой нормали)
        abs_normal = np.abs(normal)

        if abs_normal[0] > abs_normal[1] and abs_normal[0] > abs_normal[2]:
            # Проецируем на YZ плоскость (нормаль близка к оси X)
            proj_vertices = [(v[1], v[2]) for v in face_vertices]
            proj_point = (P_cross[1], P_cross[2])
        elif abs_normal[1] > abs_normal[2]:
            # Проецируем на XZ плоскость (нормаль близка к оси Y)
            proj_vertices = [(v[0], v[2]) for v in face_vertices]
            proj_point = (P_cross[0], P_cross[2])
        else:
            # Проецируем на XY плоскость (нормаль близка к оси Z)
            proj_vertices = [(v[0], v[1]) for v in face_vertices]
            proj_point = (P_cross[0], P_cross[1])

        # Проверяем, находится ли проекция точки внутри проекции грани
        return self.point_in_polygon(proj_point, proj_vertices)

    def run_simulation(self):
        """
        Запуск моделирования в соответствии с блок-схемой
        """
        rays = self.ray()
        hit_count = 0 # Счетчик попаданий
        for i in range (self.N):
            current_ray = rays[i]
            for j in range (6):
                face = self.G[j]
                F = self.flateABCD(face[0], face[1], face[2]) # Коэффициенты плоскости для грани
                P_cross = self.cross(current_ray, F) # Точка пересечения луча с плоскостью грани
                # Если есть пересечение
                if P_cross is not None:
                    if self.inside(P_cross, face):
                        hit_count += 1
                        break
        print(f"Результат моделирования:")
        print(f"Всего частиц: {self.N}")
        print(f"Попаданий в куб: {hit_count}")
        print(f"Вероятность попадания: {hit_count / self.N:.4f}")

        return hit_count