import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class CubeIntersection:
    """
    Класс для моделирования изотропного источника и куба
    """

    def __init__(self, Xs, Ys, Zs, D, N):
        """
        Инициализация источника и куба

        Parameters:
        Xs, Ys, Zs: координаты источника
        D: длина ребра куба
        N: общее количество частиц
        """
        self.Xs = Xs
        self.Ys = Ys
        self.Zs = Zs
        self.L = sqrt(Xs ** 2 + Ys ** 2 + Zs ** 2)
        self.N = abs(N)
        self.D = D
        self.half_d = D / 2

        # Вершины куба
        d = self.half_d
        self.vertices = np.array([
            [d, d, d],
            [d, d, -d],
            [d, -d, d],
            [d, -d, -d],
            [-d, d, d],
            [-d, d, -d],
            [-d, -d, d],
            [-d, -d, -d]
        ])

        # Грани куба (индексы вершин)
        self.face_indices = [
            [0, 1, 3, 2, 0],
            [4, 5, 7, 6, 4],
            [0, 2, 6, 4, 0],
            [1, 3, 7, 5, 1],
            [0, 4, 5, 1, 0],
            [2, 6, 7, 3, 2]
        ]

        # Вершины каждой грани
        self.faces = []
        for face_idx in self.face_indices:
            face_vertices = [self.vertices[idx] for idx in face_idx[:-1]]
            self.faces.append(face_vertices)

        # Параметры плоскостей для каждой грани
        self.face_planes = []
        for face in self.faces:
            plane = self.get_plane_params(face[0], face[1], face[2])
            self.face_planes.append(plane)

    def get_plane_params(self, P1, P2, P3):
        """
        Определение параметров плоскости по трём точкам
        Возвращает нормированные коэффициенты (A, B, C, D)
        """
        x1, y1, z1 = P1
        x2, y2, z2 = P2
        x3, y3, z3 = P3

        # Векторы в плоскости
        v1 = [x2 - x1, y2 - y1, z2 - z1]
        v2 = [x3 - x1, y3 - y1, z3 - z1]

        # Нормаль (векторное произведение)
        A = v1[1] * v2[2] - v1[2] * v2[1]
        B = v1[2] * v2[0] - v1[0] * v2[2]
        C = v1[0] * v2[1] - v1[1] * v2[0]
        D = -(A * x1 + B * y1 + C * z1)

        # Нормировка
        norm = sqrt(A ** 2 + B ** 2 + C ** 2)
        if norm > 0:
            A, B, C, D = A / norm, B / norm, C / norm, D / norm

        return (A, B, C, D)

    def generate_ray(self):
        """
        Генерация случайного направления луча (изотропный источник)
        Возвращает единичный направляющий вектор (l, m, n)
        """
        while True:
            l = random.uniform(-1, 1)
            m = random.uniform(-1, 1)
            n = random.uniform(-1, 1)
            length_sq = l ** 2 + m ** 2 + n ** 2
            if length_sq <= 1:
                break
        length = sqrt(length_sq)
        return (l / length, m / length, n / length)

    def generate_rays(self):
        """
        Генерация всех направлений лучей
        Возвращает массив направлений размером (N, 3)
        """
        rays = np.zeros((self.N, 3))
        for i in range(self.N):
            rays[i] = self.generate_ray()
        return rays

    def set_source_position(self, Xs, Ys, Zs):
        """Установка нового положения источника"""
        self.Xs = Xs
        self.Ys = Ys
        self.Zs = Zs
        self.L = sqrt(Xs ** 2 + Ys ** 2 + Zs ** 2)

    def find_intersection(self, ray, plane):
        """
        Нахождение точки пересечения луча с плоскостью
        ray: направляющий вектор луча (l, m, n)
        plane: коэффициенты плоскости (A, B, C, D)
        Возвращает точку пересечения и параметр t, или (None, None)
        """
        l, m, n = ray
        A, B, C, D = plane

        denominator = A * l + B * m + C * n

        if abs(denominator) < 1e-10:
            return None, None

        t = -(A * self.Xs + B * self.Ys + C * self.Zs + D) / denominator

        if t < -1e-10:
            return None, None

        point = (self.Xs + l * t, self.Ys + m * t, self.Zs + n * t)
        return point, t

    @staticmethod
    def point_in_polygon(point, polygon):
        """
        Проверка, лежит ли точка внутри многоугольника (2D)
        polygon: список точек [(x1,y1), (x2,y2), ...]
        """
        x, y = point
        inside = False
        n = len(polygon)

        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]

            if ((y1 > y) != (y2 > y)) and \
                    (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside

        return inside

    def is_point_inside_face(self, point, face_vertices):
        """
        Проверка, лежит ли точка внутри грани (3D -> 2D проекция)
        """
        # Нормаль грани
        v1 = np.array(face_vertices[1]) - np.array(face_vertices[0])
        v2 = np.array(face_vertices[2]) - np.array(face_vertices[0])
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)

        # Выбор плоскости проекции
        abs_normal = np.abs(normal)
        if abs_normal[0] > abs_normal[1] and abs_normal[0] > abs_normal[2]:
            # Проекция на YZ
            proj_vertices = [(v[1], v[2]) for v in face_vertices]
            proj_point = (point[1], point[2])
        elif abs_normal[1] > abs_normal[2]:
            # Проекция на XZ
            proj_vertices = [(v[0], v[2]) for v in face_vertices]
            proj_point = (point[0], point[2])
        else:
            # Проекция на XY
            proj_vertices = [(v[0], v[1]) for v in face_vertices]
            proj_point = (point[0], point[1])

        return self.point_in_polygon(proj_point, proj_vertices)

    def is_source_on_face(self):
        """Проверка, находится ли источник на грани куба"""
        for i, face in enumerate(self.faces):
            A, B, C, D = self.face_planes[i]
            if abs(A * self.Xs + B * self.Ys + C * self.Zs + D) < 1e-10:
                if self.is_point_inside_face((self.Xs, self.Ys, self.Zs), face):
                    return True
        return False

    def run_simulation(self):
        """
        Запуск моделирования
        Возвращает вероятность попадания
        """
        # Специальный случай: источник внутри куба
        if (abs(self.Xs) < self.half_d and
                abs(self.Ys) < self.half_d and
                abs(self.Zs) < self.half_d):
            return 1.0

        # Специальный случай: источник на грани
        if self.is_source_on_face():
            return 0.5

        hit_count = 0
        rays = self.generate_rays()

        for i in range(self.N):
            ray = rays[i]

            for j, face in enumerate(self.faces):
                point, t = self.find_intersection(ray, self.face_planes[j])

                if point is not None and self.is_point_inside_face(point, face):
                    hit_count += 1
                    break

        return hit_count / self.N

    def plot_distance_dependence(self, distances=None, num_points=200, N_mc=None):
        """
        Построение графика зависимости вероятности от расстояния

        Parameters:
        distances: список расстояний (если None, генерируется автоматически)
        num_points: количество точек для автоматической генерации
        N_mc: количество частиц для Монте-Карло (если None, используется self.N)
        """
        if N_mc is None:
            N_mc = self.N

        original_N = self.N
        self.N = N_mc

        # Генерация расстояний
        if distances is None:
            distances = np.linspace(0.5, 10, num_points)

        # Сохраняем исходное положение источника
        original_Xs, original_Ys, original_Zs = self.Xs, self.Ys, self.Zs

        probabilities = []


        for i, L in enumerate(distances):
            self.set_source_position(L, 0, 0)
            prob = self.run_simulation()
            probabilities.append(prob)

        # Восстанавливаем исходное положение
        self.set_source_position(original_Xs, original_Ys, original_Zs)
        self.N = original_N

        # Теоретическая кривая
        L_theory = np.linspace(0.1, 10, 2000)
        P_theory = np.zeros_like(L_theory)
        d = self.half_d

        for i, L in enumerate(L_theory):
            if L < d - 1e-10:
                P_theory[i] = 1.0
            elif abs(L - d) < 1e-6:
                P_theory[i] = 0.5
            else:
                P_theory[i] = 0.5 * (d ** 2) / (L ** 2)

        # Построение графика
        plt.figure(figsize=(12, 7))

        # Точки Монте-Карло
        plt.plot(distances, probabilities, 'b.', alpha=0.5, markersize=8,
                 label=f'Монте-Карло (N={N_mc})')

        # Теоретическая кривая
        plt.plot(L_theory, P_theory, 'r-', linewidth=2.5,
                 label=r'Теория: $P=1$ при $L<d$, $P=0.5$ при $L=d$, $P=0.5(d/L)^2$ при $L>d$')

        # Вертикальная линия на грани
        plt.axvline(x=d, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Грань куба (L = {d:.2f})')

        # Точка на грани
        plt.plot(d, 0.5, 'ro', markersize=8, label='Теоретическое значение на грани')

        plt.xlabel('Расстояние L от источника до центра куба', fontsize=12)
        plt.ylabel('Вероятность попадания P', fontsize=12)
        plt.title(f'Зависимость вероятности попадания от расстояния (D = {self.D})', fontsize=14)
        plt.legend(fontsize=10)
        plt.xlim(0, 10)
        plt.ylim(0, 1.05)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.show()

        return distances, probabilities
