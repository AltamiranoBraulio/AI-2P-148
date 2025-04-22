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

