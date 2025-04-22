import random
from math import sqrt
from typing import List, Tuple, Dict

Punto = Tuple[float, float, str]

class OptimizadorRutas:
    def __init__(self, ubicaciones: List[Punto]):
        self.ubicaciones = ubicaciones  # Lista de puntos a visitar
        self.lista_tabu = []  # Lista de movimientos prohibidos
        self.tamano_tabu = 5  # Tamaño máximo de la lista tabú
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')

    def distancia(self, a: Punto, b: Punto) -> float:
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

        def distancia_total(self, ruta: List[Punto]) -> float:
        total = 0
for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        # Regresar al punto inicial
        total += self.distancia(ruta[-1], ruta[0])
        return total
