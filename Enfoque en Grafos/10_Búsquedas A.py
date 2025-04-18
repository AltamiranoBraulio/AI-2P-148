import heapq
import math
from typing import List, Tuple, Dict, Optional

class Laberinto:
    SIMBOLOS = {
        ' ': ' ',     # Espacio vacío
        '#': '▓',     # Pared
        'R': '🐭',    # Ratón
        'Q': '🧀',    # Queso
        'G': '🐱',    # Gato
        '*': '·',     # Camino
        'V': 'V'      # Visitado (para depuración)
    }

    def __init__(self, laberinto: List[List[str]], raton: Tuple[int, int], queso: Tuple[int, int], gato: Tuple[int, int]):
        self.laberinto = laberinto
        self.raton = raton
        self.queso = queso
        self.gato = gato
        self.filas = len(laberinto)
        self.columnas = len(laberinto[0]) if self.filas > 0 else 0