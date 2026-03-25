import math
import random
import numpy as np
import matplotlib.pyplot as plt


class GammaInteraction:
    def __init__(self):
        """
        Инициализация параметров детектора, источника и физических констант
        """
        # Физические константы
        self.NA = 6.022e23  # Число Авогадро
        self.mc2 = 0.511  # Энергия покоя электрона в МэВ
        self.Z_Na = 11
        self.Z_I = 53
        self.A_Na = 22.99  # г/моль
        self.A_I = 126.9  # г/моль
        self.rho_NaI = 3.67  # г/см³
        self.M_NaI = 149.89  # г/моль

        n_molecules = (self.rho_NaI / self.M_NaI) * self.NA  # молекул/см³
        self.N_Na = n_molecules  # атомов Na/см³
        self.N_I = n_molecules  # атомов I/см³

        # Ввод параметров детектора и источника
        print("Введите параметры детектора :")
        self.R = float(input("Радиус цилиндра R (см): "))
        self.D = float(input("Высота цилиндра D (см): "))
        self.d = self.D / 2

        print("\nВведите координаты источника:")
        self.XO = float(input("XO (см): "))
        self.YO = float(input("YO (см): "))
        self.ZO = float(input("ZO (см): "))

        self.N_events = int(input("\nКоличество событий: "))

        # Параметры спектра
        self.E_min = 0.05
        self.E_max = 1.0
        self.num_channels = 1024
        self.Cch = (self.E_max - self.E_min) / self.num_channels  # цена канала
        self.spectrum = [0] * self.num_channels
        self._init_planes()
    @staticmethod
    def ray():
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
        length = math.sqrt(length_sq)
        return (l / length, m / length, n / length)

    def _init_planes(self):
        """
        Инициализация плоскостей верхнего и нижнего торцов цилиндра
        """
        # Верхняя плоскость (z = d)
        P1_top = (0, 0, self.d)
        P2_top = (self.R, 0, self.d)
        P3_top = (0, self.R, self.d)
        self.F_top = self.flateABCD(P1_top, P2_top, P3_top)

        # Нижняя плоскость (z = -d)
        P1_bottom = (0, 0, -self.d)
        P2_bottom = (self.R, 0, -self.d)
        P3_bottom = (0, self.R, -self.d)
        self.F_bottom = self.flateABCD(P1_bottom, P2_bottom, P3_bottom)

        # Координаты источника
        self.Ps = (self.XO, self.YO, self.ZO)

    def flateABCD(self, P1, P2, P3):
        """
        коэффициенты плоскости по трем точкам
        """
        x1, y1, z1 = P1
        x2, y2, z2 = P2
        x3, y3, z3 = P3

        A = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        B = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
        C = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        D = - (A * x1 + B * y1 + C * z1)
        return A, B, C, D

    def crossFlat(self, RAY, Ps, F):
        """
        Определяет точку пересечения луча и плоскости
        Возвращает t и точку пересечения (x, y, z) или None, если t < 0
        """
        l, m, n = RAY
        x0, y0, z0 = Ps
        A, B, C, D = F

        denominator = A * l + B * m + C * n
        if abs(denominator) < 1e-12:  # Луч параллелен плоскости
            return None, None

        t = - (A * x0 + B * y0 + C * z0 + D) / denominator

        if t < 0:  # позади источника
            return None, None

        x = x0 + l * t
        y = y0 + m * t
        z = z0 + n * t
        return t, (x, y, z)

    def insideFlat(self, R_cyl, P_cross):
        """
        Проверяет, что точка пересечения лежит в пределах торца цилиндра
        """
        x, y, z = P_cross
        # Расстояние от оси цилиндра (оси Z)
        r = math.sqrt(x ** 2 + y ** 2)
        return r <= R_cyl

    def crossCil(self, RAY):
        """
        Определяет пересечение луча с бесконечным цилиндром x^2 + y^2 = R^2
        Возвращает минимальное положительное t и точку пересечения (x, y, z)
        """
        l, m, n = RAY
        x0, y0, z0 = self.XO, self.YO, self.ZO  # координаты источника

        a = l ** 2 + m ** 2
        if a < 1e-12:  # Луч // оси Z
            return None, None

        b = 2 * (x0 * l + y0 * m)
        c = x0 ** 2 + y0 ** 2 - self.R ** 2

        D = b ** 2 - 4 * a * c

        if D < 0:
            return None, None

        t1 = (-b - math.sqrt(D)) / (2 * a)
        t2 = (-b + math.sqrt(D)) / (2 * a)

        t_min = None
        for t in [t1, t2]:
            if t > 1e-12:
                if t_min is None or t < t_min:
                    t_min = t

        if t_min is None:
            return None, None

        x = x0 + l * t_min
        y = y0 + m * t_min
        z = z0 + n * t_min
        return t_min, (x, y, z)

    def insideCil(self, P):
        """
        Проверяет, что точка P находится внутри цилиндра
        """
        x, y, z = P

        if abs(z) > self.d:
            return False

        if math.sqrt(x ** 2 + y ** 2) > self.R:
            return False
        return True

    def sigmaPh(self, E, Z):
        """
        Микроскопическое сечение фотоэффекта на K-оболочке
        """
        if E <= 0:
            return 0
        # 6.651e-25 - классический радиус электрона
        return 6.651e-25 * 4 * math.sqrt(2) * (Z ** 5) / (137 ** 4) * (self.mc2 / E) ** (7 / 2)

    def sigmaK(self, E, Z):
        """
        Микроскопическое сечение комптон-эффекта
        """
        if E <= 0:
            return 0
        gamma = E / self.mc2
        if gamma <= 0:
            return 0

        term1 = 1 - (2 * (gamma + 1) / gamma ** 2) * math.log(2 * gamma + 1)
        term2 = 1 / 2 + 4 / gamma - 1 / (2 * (2 * gamma + 1) ** 2)

        return 6.651e-25 * (3 * Z) / (8 * gamma) * (term1 + term2)

    def Sigma(self, sigmaPh_values, sigmaK_values):
        """
        Вычисляет макроскопические сечения для всех атомов
        sigmaPh_values, sigmaK_values - списки для Na и I
        Возвращает (Sigma_ph_total, Sigma_k_total, Sigma_total)
        """
        # Фотоэффект: Σ = (5/4) * N * σ
        Sigma_ph_Na = (5 / 4) * self.N_Na * sigmaPh_values[0]  # sigmaPh для Na
        Sigma_ph_I = (5 / 4) * self.N_I * sigmaPh_values[1]  # sigmaPh для I
        Sigma_ph_total = Sigma_ph_Na + Sigma_ph_I

        # Комптон: Σ = N_A * (Z/A) * σ_K
        # для каждого атома
        Sigma_k_Na = self.NA * (self.Z_Na / self.A_Na) * sigmaK_values[0] * 1e-24
        Sigma_k_I = self.NA * (self.Z_I / self.A_I) * sigmaK_values[1]
        Sigma_k_total = Sigma_k_Na + Sigma_k_I

        Sigma_total = Sigma_ph_total + Sigma_k_total

        return Sigma_ph_total, Sigma_k_total, Sigma_total

    def Length(self, Sigma_total):
        """
        Разыгрывает среднюю длину свободного пробега
        """
        if Sigma_total <= 0:
            return float('inf')
        return - (1.0 / Sigma_total) * math.log(random.random())

    def Interaction(self, P_cross, l, m, n, L):
        """
        Вычисляет координату взаимодействия
        """
        x, y, z = P_cross
        x_int = x + l * L
        y_int = y + m * L
        z_int = z + n * L
        return (x_int, y_int, z_int)

    def cost(self, l, m, n, ll, mm, nn):
        """
        Вычисляет косинус угла между двумя единичными векторами
        """
        return l * ll + m * mm + n * nn

    def Eloss(self, cos_theta, E):
        """
        Определяет потерянную энергию при комптоновском рассеянии
        Формула комптон-эффекта: E' = E / (1 + γ(1-cosθ))
        Потерянная энергия: ΔE = E - E'
        """
        gamma = E / self.mc2
        # Энергия после рассеяния
        E_prime = E / (1 + gamma * (1 - cos_theta))
        return E - E_prime

    def Lottery(self, Sigma_ph, Sigma_k, Sigma_total):
        """
        Разыгрывает тип взаимодействия на основе сечений
        Возвращает 'ph' для фотоэффекта, 'k' для комптона
        """
        if Sigma_total <= 0:
            return None

        rand = random.random()
        p_ph = Sigma_ph / Sigma_total

        if rand < p_ph:
            return 'ph'
        else:
            return 'k'

    def find_entry_point(self, ray_direction):
        """
        Находит точку входа фотона в детектор
        Возвращает точку входа (x, y, z) или None, если луч не пересекает детектор
        """
        l, m, n = ray_direction
        # Пересечение с верхним торцом
        t_top, P_top = self.crossFlat(ray_direction, self.Ps, self.F_top)
        hit_top = False
        t_entry = None
        P_entry = None

        if t_top is not None and self.insideFlat(self.R, P_top):
            hit_top = True
            t_entry = t_top
            P_entry = P_top
        # Пересечение с нижним торцом
        t_bottom, P_bottom = self.crossFlat(ray_direction, self.Ps, self.F_bottom)
        hit_bottom = False
        if t_bottom is not None and self.insideFlat(self.R, P_bottom):
            hit_bottom = True
            if not hit_top or t_bottom < t_entry:
                t_entry = t_bottom
                P_entry = P_bottom
        # Пересечение с цилиндром
        t_cyl, P_cyl = self.crossCil(ray_direction)
        hit_cyl = False
        if t_cyl is not None and self.insideCil(P_cyl):
            hit_cyl = True
            # Проверяем, что это ближайшее пересечение
            if (not hit_top and not hit_bottom) or \
                    (hit_top and t_cyl < t_entry) or \
                    (hit_bottom and t_cyl < t_entry):
                t_entry = t_cyl
                P_entry = P_cyl
        # Если нет пересечения с детектором
        if not (hit_top or hit_bottom or hit_cyl):
            return None
        return P_entry

    def simulate(self):
        """
        Основной метод моделирования взаимодействия гамма-квантов с детектором
        """
        for event in range(self.N_events):
            # Начальная энергия для Cs-137
            E = 0.662  # МэВ
            # Начальное направление
            l, m, n = self.ray()
            # Находим точку входа в детектор
            P_entry = self.find_entry_point((l, m, n))
            if P_entry is None:
                # Фотон не попал в детектор
                continue
            # Фотон внутри детектора
            current_point = P_entry
            while E > 0:
                # Сечения для текущей энергии
                sigma_ph_Na = self.sigmaPh(E, self.Z_Na)
                sigma_ph_I = self.sigmaPh(E, self.Z_I)
                sigma_k_Na = self.sigmaK(E, self.Z_Na)
                sigma_k_I = self.sigmaK(E, self.Z_I)
                Sigma_ph, Sigma_k, Sigma_total = self.Sigma(
                    [sigma_ph_Na, sigma_ph_I],
                    [sigma_k_Na, sigma_k_I]
                )
                if Sigma_total <= 0:
                    break
                # Длина свободного пробега
                L = self.Length(Sigma_total)
                # Точка взаимодействия
                P_int = self.Interaction(current_point, l, m, n, L)
                # Проверяем, что взаимодействие внутри детектора
                if not self.insideCil(P_int):
                    # Фотон покинул детектор без взаимодействия
                    break
                # Разыгрываем тип взаимодействия
                interaction_type = self.Lottery(Sigma_ph, Sigma_k, Sigma_total)
                if interaction_type == 'ph':
                    # Фотоэффект - вся энергия поглощена
                    channel = int(round(E / self.Cch))
                    if 0 <= channel < self.num_channels:
                        self.spectrum[channel] += 1
                    break
                elif interaction_type == 'k':
                    # Комптон-эффект
                    # Новое направление
                    l_new, m_new, n_new = self.ray()
                    # Косинус угла между старым и новым направлением
                    cos_theta = self.cost(l, m, n, l_new, m_new, n_new)
                    # Потерянная энергия
                    dE = self.Eloss(cos_theta, E)
                    # Регистрируем потерянную энергию
                    if dE > 0:
                        channel = int(round(dE / self.Cch))
                        if 0 <= channel < self.num_channels:
                            self.spectrum[channel] += 1
                    # Обновляем энергию фотона
                    E = E - dE
                    # Обновляем направление
                    l, m, n = l_new, m_new, n_new
                    # Обновляем текущую точку
                    current_point = P_int

    def plot_spectrum(self):
        """
        Построение энергетического спектра
        """
        plt.figure(figsize=(10, 6))
        energies = [self.E_min + i * self.Cch for i in range(self.num_channels)]
        plt.plot(energies, self.spectrum, 'b-', linewidth=1)
        plt.xlabel('Энергия (МэВ)')
        plt.ylabel('Количество отсчетов')
        plt.title('Энергетический спектр гамма-излучения Cs-137 в детекторе NaI')
        plt.grid(True, alpha=0.3)
        plt.show()