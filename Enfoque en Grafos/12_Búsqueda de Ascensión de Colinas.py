import random
from math import sqrt
from typing import List, Tuple, Dict

Punto = Tuple[float, float, str]

class RepartidorPizzas:
    def __init__(self, ubicaciones: List[Punto]):
        self.ubicaciones = ubicaciones
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')

    def distancia(self, a: Punto, b: Punto) -> float:
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def distancia_total(self, ruta: List[Punto]) -> float:
        total = 0
        for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        total += self.distancia(ruta[-1], ruta[0])
        return total
    
        def generar_vecino(self, ruta: List[Punto]) -> List[Punto]:
        vecino = ruta.copy()
        i, j = random.sample(range(len(vecino)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino