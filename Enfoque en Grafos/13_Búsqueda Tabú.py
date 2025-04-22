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
def generar_vecinos(self, ruta: List[Punto]) -> List[List[Punto]]:
        """Genera vecinos intercambiando dos puntos aleatorios"""
        vecinos = []
        for _ in range(5):  # Generar 5 vecinos
            vecino = ruta.copy()
            i, j = random.sample(range(len(vecino)), 2)
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
        return vecinos

 def criterio_aspiración(self, distancia: float) -> bool:
        """Determina si un movimiento tabú debe ser permitido"""
        return distancia < self.mejor_distancia * 0.9  # 10% mejor que el mejor

def busqueda_tabu(self, max_iter: int = 100):
        """Algoritmo de Búsqueda Tabú"""
        # 1. Solución inicial aleatoria
        ruta_actual = self.ubicaciones.copy()
        random.shuffle(ruta_actual)
        distancia_actual = self.distancia_total(ruta_actual)
        
        self.mejor_ruta = ruta_actual.copy()
        self.mejor_distancia = distancia_actual
        
        for iteracion in range(max_iter):
            # 2. Generar vecindario
            vecinos = self.generar_vecinos(ruta_actual)
            
            # 3. Evaluar vecinos
            mejor_vecino = None
            mejor_distancia = float('inf')
            mejor_movimiento = None