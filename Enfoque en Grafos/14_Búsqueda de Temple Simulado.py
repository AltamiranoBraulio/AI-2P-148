import random
import math
import matplotlib.pyplot as plt

def espectacularidad(x):
    return x**2 + 5 * math.sin(3*x) + 3 * math.cos(5*x)
def mover_robot(x):
    return x + random.uniform(-0.5, 0.5)
def buscar_mejor_paso():
    temperatura = 100
    enfriamiento = 0.95
    minimo_temp = 0.1
x = random.uniform(-10, 10)
    mejor_x = x
    mejor_espectaculo = espectacularidad(x)

    historial = [x]