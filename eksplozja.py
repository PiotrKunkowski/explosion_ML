import numpy as np
import matplotlib.pyplot as plt
from klasy import *
from funkcje import *


N = 10  #liczba punktow pomiarowych
sensors = set_sensors(N)
e = random_explosion()
print('Miejsce wybuchu: (%.4f, %.4f)' %(e[0], e[1]))

sigma2 = 0.1 #odchylenie standardowe
measure = interference(sensors, e, N, sigma2) 

print('\n\nDane do interferencji:\n')
for i in range(N):
    print('punkt %d: (%.4f, %.4f)' %(i+1, sensors[i][0], sensors[i][1]),
          '\tpomiar: %.4f'%(measure[i]))

e_x = 0
e_y = 1
delta = 0.1
states = np.arange(-1, 1.001, delta)
ile_stanow = len(states)
print('\n\nStanow dla wspolrzednej wybuchu jest', ile_stanow, ':\n', states)

var = [variable(None, None) for i in range(2)]
var[e_x].name = "e_x"
var[e_x].domain = states
var[e_y].name = "e_y"
var[e_y].domain = states

#obliczanie potencjalow
pot = potential()
pot.variables = np.array([e_x, e_y])
table = np.zeros((ile_stanow, ile_stanow))
x1 = 1 / (2 * sigma2)
x2 = np.sqrt(np.pi*x1)
srodek = [0, 0]
for j in range(ile_stanow):
    for k in range(ile_stanow):
        p = 1
        rob_e = [-1 + delta * j, -1 + delta * k]
        odl_e = dist_squared(rob_e, srodek)
        if odl_e < 1.0:
            rob_d2 = np.zeros(N)
            d2 = np.zeros(N)
            rob_p = np.zeros(N)
            for i in range(N):
                rob_d2[i] = dist_squared(sensors[i], rob_e)
                d2[i] = 1 / (rob_d2[i] + 0.1)
                rob_p[i] = np.exp((-1 / x1) * (measure[i] - d2[i]) ** 2)/x2
                p = p*rob_p[i]
        else:
            p = 0
        table[j, k] = p

pot.table = table
suma = np.sum(pot.table)
pot.table = pot.table/suma  #wykonanie normalizacji rozkladu do 1

maxi = np.amax(pot.table)
argument_maxi = np.argmax(pot.table)
indexes = np.unravel_index(np.argmax(pot.table), pot.table.shape)
esty_ex = -1+delta*indexes[0]
esty_ey = -1+delta*indexes[1]
print("\nEstymacja punktu: (%.4f" %esty_ex + ", %.4f) " %esty_ey)

#rysowanie wykresu
x = np.arange(-1,1.001, delta)
y = np.arange(-1,1.001, delta)
X,Y = np.meshgrid(x,y)
plt.figure(figsize=(7,6))
tytul = "wybuch w: " + str(round(e[0],2)) + ", " + str(round(e[1],2)) + (" rozpoznany w: %.2f " % esty_ex) + (", %.2f" % esty_ey)

plt.scatter(e[0], e[1], color='red', marker='x', 
            label='faktyczne epicentrum ')
plt.scatter(esty_ex, esty_ey, color='green', marker='x', 
            label='zarejestrowane epicentrum')
plt.scatter([sensor[0] for sensor in sensors],
            [sensor[1] for sensor in sensors], 
            color='magenta', label='sensory')
plt.legend(loc='lower left')

plt.title(tytul)
plt.show()