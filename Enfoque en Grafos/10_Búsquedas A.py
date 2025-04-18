import heapq
import math
from typing import List, Tuple, Dict, Optional

class Laberinto:
    """Clase para representar el laberinto del ratón."""
    
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
                    print(self.SIMBOLOS.get(self.grid[i][j]), end=' ')  # Error corregido aquí
            print()

def distancia_chebyshev(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Distancia de Chebyshev (para movimientos en 8 direcciones)."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def a_estrella(laberinto: Laberinto) -> Optional[List[Tuple[int, int]]]:
    """
    Implementación creativa de A* para que el ratón encuentre el queso.
    
    Args:
        laberinto: Objeto Laberinto con la configuración del problema.
    
    Returns:
        Lista de posiciones del camino óptimo o None si no hay solución.
    """
    if not laberinto.raton_pos or not laberinto.queso_pos:
        return None
    
    # Movimientos posibles (8 direcciones)
    movimientos = [(-1,-1), (-1,0), (-1,1),
                   (0,-1),          (0,1),
                   (1,-1),  (1,0),  (1,1)]
    
    # Nodos abiertos (por explorar) y cerrados (explorados)
    abiertos = []
    cerrados = set()
    
    # Diccionario para reconstruir caminos y registrar costos
    registro = {laberinto.raton_pos: {'g': 0, 'h': distancia_chebyshev(laberinto.raton_pos, laberinto.queso_pos), 'padre': None}}
    
    # Agregar posición inicial a la lista abierta
    heapq.heappush(abiertos, (registro[laberinto.raton_pos]['g'] + registro[laberinto.raton_pos]['h'], laberinto.raton_pos))
    
    while abiertos:
        # Obtener el nodo con menor f = g + h
        _, pos_actual = heapq.heappop(abiertos)
        
        # Si llegamos al queso, reconstruir el camino
        if pos_actual == laberinto.queso_pos:
            camino = []
            while pos_actual:
                camino.append(pos_actual)
                pos_actual = registro[pos_actual]['padre']
            return camino[::-1]
        
        cerrados.add(pos_actual)
        
        # Explorar vecinos
        for movimiento in movimientos:
            nueva_pos = (pos_actual[0] + movimiento[0], pos_actual[1] + movimiento[1])
            
            # Saltar si no es válido o ya explorado
            if not laberinto.es_valido(*nueva_pos) or nueva_pos in cerrados:
                continue
            
            # Calcular nuevo costo g
            # Movimiento diagonal cuesta más (sqrt(2) ≈ 1.4)
            costo_movimiento = 1.4 if movimiento[0] != 0 and movimiento[1] != 0 else 1
            nuevo_g = registro[pos_actual]['g'] + costo_movimiento
            
            # Si es nuevo nodo o encontramos un camino mejor
            if nueva_pos not in registro or nuevo_g < registro[nueva_pos]['g']:
                registro[nueva_pos] = {
                    'g': nuevo_g,
                    'h': distancia_chebyshev(nueva_pos, laberinto.queso_pos),
                    'padre': pos_actual
                }
                heapq.heappush(abiertos, (registro[nueva_pos]['g'] + registro[nueva_pos]['h'], nueva_pos))
    
    return None

# Ejemplo de uso creativo
def crear_laberinto_ejemplo() -> Laberinto:
    """Crea un laberinto de ejemplo para el ratón."""
    lab = Laberinto(10, 15)
    
    # Paredes
    paredes = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14),
        (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14),
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
        (1, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14),
        (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (4, 8), (4, 9), (4, 10), (4, 11),
        (6, 2), (6, 3), (6, 4), (6, 5),
        (8, 7), (8, 8), (8, 9), (8, 10)
    ]
    for fila, col in paredes:
        lab.agregar_elemento(fila, col, '#')
    
    # Gatos
    lab.agregar_elemento(3, 7, 'G')
    lab.agregar_elemento(7, 6, 'G')
    lab.agregar_elemento(5, 12, 'G')
    
    # Ratón y queso
    lab.agregar_elemento(1, 1, 'R')
    lab.agregar_elemento(8, 13, 'Q')
    
    return lab

if __name__ == "__main__":
    print("🐭 LABERINTO DEL RATÓN - ALGORITMO A* 🧀")
    print("▓ = Pared | 🐭 = Ratón | 🧀 = Queso | 🐱 = Gato")
    
    laberinto = crear_laberinto_ejemplo()
    print("\nLaberinto inicial:")
    laberinto.mostrar()
    
    print("\nBuscando camino óptimo con A*...")
    camino = a_estrella(laberinto)  # Error de nombre corregido aquí (era a_estresta)
    
    if camino:
        print("\n¡Camino encontrado!")
        print(f"Longitud del camino: {len(camino)-1} pasos")
        print("\nLaberinto con solución:")
        laberinto.mostrar(camino)
        
        print("\nPasos del camino:")
        for i, pos in enumerate(camino):
            print(f"Paso {i}: {pos}")
    else:
        print("\nNo se encontró un camino seguro al queso. ¡Los gatos bloquearon el camino!")