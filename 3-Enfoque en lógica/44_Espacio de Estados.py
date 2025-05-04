"""
SISTEMA DE BÚSQUEDA EN ESPACIO DE ESTADOS - RESOLUCIÓN DE LABERINTOS
Autor: DeepSeek Chat
Enfoque: Representación de estados, transiciones y algoritmos de búsqueda no informada
"""

from typing import List, Tuple, Dict, Set, Optional
from collections import deque
import heapq
import matplotlib.pyplot as plt
import numpy as np

# ==================== REPRESENTACIÓN DEL LABERINTO ====================
class Laberinto:
    """
    Clase que representa un laberinto como una matriz de celdas:
    - 0: Pasillo
    - 1: Pared
    - 2: Posición inicial
    - 3: Meta
    """
    def __init__(self, matriz: List[List[int]]):
        self.matriz = np.array(matriz)  # Convertimos a array de numpy para mejor manipulación
        self.filas, self.columnas = self.matriz.shape
        self.inicio = self._encontrar_posicion(2)  # Encontramos la posición inicial
        self.meta = self._encontrar_posicion(3)    # Encontramos la posición meta

    def _encontrar_posicion(self, valor: int) -> Tuple[int, int]:
        """Encuentra la posición (fila, columna) de un valor específico en el laberinto"""
        posiciones = np.argwhere(self.matriz == valor)
        if len(posiciones) == 0:
            raise ValueError(f"No se encontró el valor {valor} en el laberinto")
        return tuple(posiciones[0])  # Devolvemos la primera ocurrencia

    def es_valida(self, fila: int, columna: int) -> bool:
        """Verifica si una posición es válida (dentro de los límites y no es pared)"""
        return (0 <= fila < self.filas and 
                0 <= columna < self.columnas and 
                self.matriz[fila, columna] != 1)

    def dibujar(self, camino: List[Tuple[int, int]] = None):
        """Visualiza el laberinto y opcionalmente un camino solución"""
        plt.figure(figsize=(8, 8))
        
        # Creamos una copia para no modificar el original
        laberinto_visual = self.matriz.copy()
        
        # Marcamos el camino si se proporciona
        if camino:
            for paso in camino:
                laberinto_visual[paso] = 4  # Usamos 4 para representar el camino
        
        # Configuramos colores
        cmap = plt.cm.colors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
        
        plt.imshow(laberinto_visual, cmap=cmap, norm=norm)
        
        # Añadimos una cuadrícula
        plt.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
        plt.xticks(np.arange(-0.5, self.columnas, 1), [])
        plt.yticks(np.arange(-0.5, self.filas, 1), [])
        
        plt.show()

# ==================== REPRESENTACIÓN DEL ESPACIO DE ESTADOS ====================
class Estado:
    """
    Representa un estado en el espacio de búsqueda:
    - posición: (fila, columna) actual
    - padre: estado del que proviene este estado
    - accion: acción que llevó a este estado
    - costo: costo acumulado hasta este estado
    """
    def __init__(self, posicion: Tuple[int, int], 
                 padre: Optional['Estado'] = None, 
                 accion: Optional[str] = None, 
                 costo: int = 0):
        self.posicion = posicion
        self.padre = padre
        self.accion = accion
        self.costo = costo

    def __eq__(self, otro):
        return self.posicion == otro.posicion

    def __hash__(self):
        return hash(self.posicion)

    def __lt__(self, otro):
        return self.costo < otro.costo

    def expandir(self, laberinto: Laberinto) -> List['Estado']:
        """Genera todos los estados válidos alcanzables desde este estado"""
        movimientos = [
            ('arriba', (-1, 0)),
            ('abajo', (1, 0)),
            ('izquierda', (0, -1)),
            ('derecha', (0, 1))
        ]
        
        estados_hijos = []
        for nombre_accion, (df, dc) in movimientos:
            nueva_fila, nueva_columna = self.posicion[0] + df, self.posicion[1] + dc
            
            if laberinto.es_valida(nueva_fila, nueva_columna):
                nuevo_estado = Estado(
                    posicion=(nueva_fila, nueva_columna),
                    padre=self,
                    accion=nombre_accion,
                    costo=self.costo + 1
                )
                estados_hijos.append(nuevo_estado)
        
        return estados_hijos

    def reconstruir_camino(self) -> List[Tuple[int, int]]:
        """Reconstruye el camino desde el estado inicial hasta este estado"""
        camino = []
        estado_actual = self
        while estado_actual is not None:
            camino.append(estado_actual.posicion)
            estado_actual = estado_actual.padre
        return list(reversed(camino))  # Invertimos para ir del inicio al final

# ==================== ALGORITMOS DE BÚSQUEDA ====================
def busqueda_amplitud(laberinto: Laberinto) -> Optional[Estado]:
    """
    Búsqueda en amplitud (BFS) para encontrar el camino más corto en el laberinto.
    Explora todos los nodos en un nivel antes de pasar al siguiente nivel.
    """
    frontera = deque()  # Usamos una cola para FIFO
    explorados = set()  # Conjunto de posiciones ya exploradas
    
    estado_inicial = Estado(laberinto.inicio)
    frontera.append(estado_inicial)
    
    while frontera:
        estado_actual = frontera.popleft()
        
        # Verificamos si hemos llegado a la meta
        if estado_actual.posicion == laberinto.meta:
            return estado_actual
        
        explorados.add(estado_actual.posicion)
        
        # Expandimos el estado actual
        for hijo in estado_actual.expandir(laberinto):
            if hijo.posicion not in explorados and hijo not in frontera:
                frontera.append(hijo)
    
    return None  # No se encontró solución

def busqueda_profundidad(laberinto: Laberinto, limite_profundidad=100) -> Optional[Estado]:
    """
    Búsqueda en profundidad (DFS) con límite para evitar recursión infinita.
    Explora un camino hasta el final antes de probar alternativas.
    """
    frontera = []  # Usamos una pila para LIFO
    explorados = set()
    
    estado_inicial = Estado(laberinto.inicio)
    frontera.append(estado_inicial)
    
    while frontera:
        estado_actual = frontera.pop()
        
        if estado_actual.posicion == laberinto.meta:
            return estado_actual
        
        if estado_actual.costo >= limite_profundidad:
            continue  # No exploramos más allá del límite
            
        explorados.add(estado_actual.posicion)
        
        # Expandimos en orden inverso para un comportamiento DFS estándar
        for hijo in reversed(estado_actual.expandir(laberinto)):
            if hijo.posicion not in explorados and hijo not in frontera:
                frontera.append(hijo)
    
    return None

def busqueda_costo_uniforme(laberinto: Laberinto) -> Optional[Estado]:
    """
    Búsqueda de costo uniforme (Dijkstra) que expande el nodo con menor costo acumulado.
    """
    frontera = []
    heapq.heapify(frontera)  # Usamos un heap para mantener ordenados por costo
    explorados = set()
    
    estado_inicial = Estado(laberinto.inicio)
    heapq.heappush(frontera, estado_inicial)
    
    while frontera:
        estado_actual = heapq.heappop(frontera)
        
        if estado_actual.posicion == laberinto.meta:
            return estado_actual
        
        explorados.add(estado_actual.posicion)
        
        for hijo in estado_actual.expandir(laberinto):
            if hijo.posicion not in explorados and hijo not in frontera:
                heapq.heappush(frontera, hijo)
            elif hijo in frontera:
                # Actualizamos si encontramos un camino más corto
                for i, estado in enumerate(frontera):
                    if estado == hijo and estado.costo > hijo.costo:
                        frontera[i] = hijo
                        heapq.heapify(frontera)  # Reordenamos el heap
                        break
    
    return None

# ==================== EJEMPLO DE USO ====================
def main():
    # Definimos un laberinto de ejemplo
    laberinto_ejemplo = [
        [2, 0, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 0, 3]
    ]
    
    lab = Laberinto(laberinto_ejemplo)
    print("Visualización del laberinto inicial:")
    lab.dibujar()
    
    # Prueba de BFS
    print("\nBúsqueda en amplitud (BFS):")
    solucion_bfs = busqueda_amplitud(lab)
    if solucion_bfs:
        camino_bfs = solucion_bfs.reconstruir_camino()
        print(f"Solución encontrada en {len(camino_bfs)-1} pasos")
        lab.dibujar(camino_bfs)
    else:
        print("No se encontró solución con BFS")
    
    # Prueba de DFS
    print("\nBúsqueda en profundidad (DFS):")
    solucion_dfs = busqueda_profundidad(lab)
    if solucion_dfs:
        camino_dfs = solucion_dfs.reconstruir_camino()
        print(f"Solución encontrada en {len(camino_dfs)-1} pasos")
        lab.dibujar(camino_dfs)
    else:
        print("No se encontró solución con DFS")
    
    # Prueba de Costo Uniforme
    print("\nBúsqueda de costo uniforme:")
    solucion_costo = busqueda_costo_uniforme(lab)
    if solucion_costo:
        camino_costo = solucion_costo.reconstruir_camino()
        print(f"Solución encontrada con costo {solucion_costo.costo}")
        lab.dibujar(camino_costo)
    else:
        print("No se encontró solución con costo uniforme")

if __name__ == "__main__":
    main()