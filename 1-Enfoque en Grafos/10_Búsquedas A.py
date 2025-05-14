# =====================
# IMPORTACIÓN DE LIBRERÍAS
# =====================

import heapq  # Proporciona funciones para manejar colas de prioridad (min-heaps), crucial para seleccionar el siguiente nodo a explorar en A*
import math   # Módulo de funciones matemáticas. En este código no se usa directamente, pero es común en problemas de búsqueda con heurísticas.
from typing import List, Tuple, Dict, Optional  # Importa tipos para anotar funciones y variables. Mejora la legibilidad y evita errores de tipo.

# =====================
# DEFINICIÓN DE CLASE LABERINTO
# =====================

class Laberinto:
    """
    Clase que representa el laberinto donde se mueve el ratón.
    Permite colocar elementos, validar celdas y mostrar el estado del laberinto.
    """

    SIMBOLOS = {
        ' ': ' ',     # Espacio transitable
        '#': '▓',     # Pared infranqueable
        'R': '🐭',     # Ratón (inicio)
        'Q': '🧀',     # Queso (meta)
        'G': '🐱',     # Gato (obstáculo dinámico)
        '*': '·',     # Camino hallado por A*
        'V': 'V'      # Celda visitada (solo para debug)
    }

    def __init__(self, filas: int, columnas: int):
        """Inicializa un laberinto vacío con dimensiones dadas"""
        self.filas = filas
        self.columnas = columnas
        self.grid = [[' ' for _ in range(columnas)] for _ in range(filas)]  # Matriz de espacios vacíos
        self.raton_pos = None     # Posición inicial del ratón
        self.queso_pos = None     # Posición del queso
        self.gatos_pos = []       # Lista de posiciones de los gatos

    def agregar_elemento(self, fila: int, col: int, elemento: str):
        """Coloca un elemento ('#', 'R', 'Q', 'G') en el laberinto y guarda su posición si es relevante"""
        if elemento == 'R':
            self.raton_pos = (fila, col)
        elif elemento == 'Q':
            self.queso_pos = (fila, col)
        elif elemento == 'G':
            self.gatos_pos.append((fila, col))
        self.grid[fila][col] = elemento

    def es_valido(self, fila: int, col: int) -> bool:
        """Verifica que una celda no sea una pared ni esté fuera del laberinto ni tenga gato"""
        return (0 <= fila < self.filas and 
                0 <= col < self.columnas and 
                self.grid[fila][col] not in ('#', 'G'))

    def mostrar(self, camino: List[Tuple[int, int]] = None):
        """Muestra el laberinto en consola. Puede mostrar el camino si se le pasa una lista."""
        for i in range(self.filas):
            for j in range(self.columnas):
                if camino and (i, j) in camino:
                    print('*', end=' ')  # Marca camino
                else:
                    print(self.SIMBOLOS.get(self.grid[i][j], ' '), end=' ')  # Símbolo correspondiente
            print()  # Nueva línea por cada fila

# =====================
# HEURÍSTICA: DISTANCIA DE CHEBYSHEV
# =====================

def distancia_chebyshev(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    Devuelve la distancia de Chebyshev entre dos puntos.
    Es útil para considerar movimientos diagonales (máximo entre diferencias de filas y columnas).
    """
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

# =====================
# ALGORITMO A* PARA BUSCAR CAMINO
# =====================

def a_estrella(laberinto: Laberinto) -> Optional[List[Tuple[int, int]]]:
    """
    Implementación del algoritmo A* para encontrar el camino más corto entre el ratón y el queso.

    Returns:
        Lista de coordenadas del camino óptimo o None si no hay solución.
    """

    if not laberinto.raton_pos or not laberinto.queso_pos:
        return None  # No hay inicio o meta

    # 8 direcciones posibles (movimiento total)
    movimientos = [(-1,-1), (-1,0), (-1,1),
                   (0,-1),          (0,1),
                   (1,-1),  (1,0),  (1,1)]

    abiertos = []  # Cola de prioridad: nodos por explorar
    cerrados = set()  # Nodos ya evaluados

    # Registro: g (costo real), h (heurística), padre (de dónde vino)
    registro = {
        laberinto.raton_pos: {
            'g': 0,
            'h': distancia_chebyshev(laberinto.raton_pos, laberinto.queso_pos),
            'padre': None
        }
    }

    # Agregar nodo inicial a la cola
    heapq.heappush(abiertos, (registro[laberinto.raton_pos]['g'] + registro[laberinto.raton_pos]['h'], laberinto.raton_pos))

    while abiertos:
        _, actual = heapq.heappop(abiertos)  # Extraer el de menor f = g + h

        if actual == laberinto.queso_pos:  # ¿Llegamos al queso?
            camino = []
            while actual:
                camino.append(actual)
                actual = registro[actual]['padre']
            return camino[::-1]  # Retorna el camino de inicio a fin

        cerrados.add(actual)  # Marcar como visitado

        for dx, dy in movimientos:
            vecino = (actual[0] + dx, actual[1] + dy)

            if not laberinto.es_valido(*vecino) or vecino in cerrados:
                continue  # Ignora movimientos inválidos o ya evaluados

            costo = 1.4 if dx != 0 and dy != 0 else 1  # Diagonal cuesta 1.4, ortogonal 1
            g_nuevo = registro[actual]['g'] + costo

            if vecino not in registro or g_nuevo < registro[vecino]['g']:
                registro[vecino] = {
                    'g': g_nuevo,
                    'h': distancia_chebyshev(vecino, laberinto.queso_pos),
                    'padre': actual
                }
                f_nuevo = registro[vecino]['g'] + registro[vecino]['h']
                heapq.heappush(abiertos, (f_nuevo, vecino))

    return None  # No se encontró camino

# =====================
# CREACIÓN DE UN LABERINTO DE EJEMPLO
# =====================

def crear_laberinto_ejemplo() -> Laberinto:
    """
    Crea una instancia del laberinto con obstáculos, enemigos y un punto de inicio y meta.
    """
    lab = Laberinto(10, 15)

    # Paredes externas e internas
    paredes = [
        *[(0, i) for i in range(15)],
        *[(9, i) for i in range(15)],
        *[(i, 0) for i in range(1, 9)],
        *[(i, 14) for i in range(1, 9)],
        (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (4, 8), (4, 9), (4, 10), (4, 11),
        (6, 2), (6, 3), (6, 4), (6, 5),
        (8, 7), (8, 8), (8, 9), (8, 10)
    ]
    for fila, col in paredes:
        lab.agregar_elemento(fila, col, '#')

    # Gatos enemigos
    lab.agregar_elemento(3, 7, 'G')
    lab.agregar_elemento(7, 6, 'G')
    lab.agregar_elemento(5, 12, 'G')

    # Ratón y queso
    lab.agregar_elemento(1, 1, 'R')
    lab.agregar_elemento(8, 13, 'Q')

    return lab

# =====================
# PUNTO DE ENTRADA
# =====================

if __name__ == "__main__":
    print("🐭 LABERINTO DEL RATÓN - ALGORITMO A* 🧀")
    print("▓ = Pared | 🐭 = Ratón | 🧀 = Queso | 🐱 = Gato")

    laberinto = crear_laberinto_ejemplo()  # Creamos el laberinto
    print("\nLaberinto inicial:")
    laberinto.mostrar()  # Mostrar antes de buscar camino

    print("\nBuscando camino óptimo con A*...")
    camino = a_estrella(laberinto)

    if camino:
        print("\n¡Camino encontrado!")
        print(f"Longitud del camino: {len(camino)-1} pasos")  # Excluye el inicio
        print("\nLaberinto con solución:")
        laberinto.mostrar(camino)

        print("\nPasos del camino:")
        for i, paso in enumerate(camino):
            print(f"Paso {i}: {paso}")
    else:
        print("\nNo se encontró un camino seguro al queso. ¡Los gatos bloquearon el camino!")

"""
--- COMENTARIO GENERAL SOBRE EL CÓDIGO ---

Este programa implementa el algoritmo A* para encontrar el camino más corto desde un punto de inicio (el ratón 🐭) hasta una meta (el queso 🧀), dentro de un laberinto con obstáculos fijos (paredes) y dinámicos (gatos 🐱). 

1. Se define un objeto `Laberinto` que modela el entorno.
2. Se usa una heurística (distancia de Chebyshev) para evaluar qué tan lejos está un nodo del queso.
3. El algoritmo A* explora caminos eficientes usando una cola de prioridad.
4. Si encuentra un camino, lo imprime paso a paso en consola y visualiza el resultado.

Este enfoque es común en inteligencia artificial y videojuegos para navegación de personajes en mapas con obstáculos.
"""