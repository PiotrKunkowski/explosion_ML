import numpy as np
import matplotlib.pyplot as plt

'''przygotowanie danych do eksplozji'''

def dist_squared(a, b, dim=2):
    #oblicza kwadrat odległości między punktami a i b w dwóch wymiarach
    dist = [(a[i] - b[i]) ** 2 for i in range(dim)]
    return sum(dist)

def set_sensors(n, r=1.0):
    #ustawia n równoodległych punktów na okręgu o promieniu r=1
    sensors = []
    for r, n in {(r, n)}:
        t = np.linspace(0, np.pi*2, n)
        x = r * np.cos(t)
        y = r * np.sin(t)
        sensors.append(np.c_[x, y])
    #w tej chwili zmienna sensors jest listą, która zawiera np.ndarray
    #konwersja do zwykłej listy:
    sensors = sensors[0]
    sensors.tolist()
    return sensors


def random_explosion():
    ex = 2
    ey = 2
    dist_e = dist_squared([ex, ey], [0, 0])
    while (dist_e > 1):
        ex = np.random.rand()
        ey = np.random.rand()
        if (np.random.rand() < 0.5):
            ex = -ex
        if (np.random.rand() < 0.5):
            ey = -ey
        dist_e = dist_squared([ex, ey], [0, 0])
    return [ex, ey]


def interference(sensors, e, N, sigma2):
    '''zaburzenie danych z obserwacji
    sensors - lista współrzędnych sensorów, e - parametr wygenerowanej eksplozji, 
    N - liczba sensorów, sigma2 - odchylenie standardowe'''
    d2 = [dist_squared(sensors[i], e) for i in range(N)]
    signal_received = [1 / (d2[i] + 0.1) for i in range(N)]
    interfer = [signal_received[i] + np.random.normal(0, sigma2) for i in range(N)]
    return interfer

