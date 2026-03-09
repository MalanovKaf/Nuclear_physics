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

    def cross (self,Ray,F):
        t=-(F[0]*self.Xs+F[1]*self.Ys+F[2]*self.Zs+F[3])/(F[0]*Ray[0]+F[1]*Ray[1]+F[2]*Ray[2])
        if t>=0:
            P_cross=[self.Xs+t*Ray[0],self.Ys+t*Ray[1],self.Zs+t*Ray[2]]
            return P_cross
        else:
            return None

    def inside (self,G,Pc):
