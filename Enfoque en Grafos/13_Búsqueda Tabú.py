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

