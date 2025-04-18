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

    def __init__(self, filas: int, columnas: int):
        self.filas = filas
        self.columnas = columnas
        self.grid = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.raton_pos = None
        self.queso_pos = None
        self.gatos_pos = []

    def agregar_elemento(self, fila: int, col: int, elemento: str):
        """Agrega un elemento al laberinto."""
        if elemento == 'R':
            self.raton_pos = (fila, col)
        elif elemento == 'Q':
            self.queso_pos = (fila, col)
        elif elemento == 'G':
            self.gatos_pos.append((fila, col))
        self.grid[fila][col] = elemento

    def es_valido(self, fila: int, col: int) -> bool:
        """Verifica si una posición es válida y transitable."""
        return (0 <= fila < self.filas and 
                0 <= col < self.columnas and 
                self.grid[fila][col] not in ('#', 'G'))
    
    def mostrar(self, camino: List[Tuple[int, int]] = None):
        """Muestra el laberinto, opcionalmente con un camino marcado."""
        for i in range(self.filas):
            for j in range(self.columnas):
                if camino and (i, j) in camino:
                    print('*', end=' ')
                else:
                    print(self.SIMBOLOS.get(self.grid[i][j], end=' ')
            print()

    