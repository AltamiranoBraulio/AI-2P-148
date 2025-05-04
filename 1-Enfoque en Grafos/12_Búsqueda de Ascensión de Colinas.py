"""
Este programa resuelve el clásico problema de las 8 reinas usando el algoritmo
de Ascensión de Colinas. El objetivo es colocar 8 reinas en un tablero de ajedrez
sin que se ataquen entre sí (ni en filas, columnas ni diagonales).
"""

import random  # Para generar números aleatorios
from typing import List, Tuple  # Para anotaciones de tipo

class Puzzle8Reinas:
    """
    Clase principal que implementa la solución al problema de las 8 reinas.
    Utiliza el algoritmo de Ascensión de Colinas para encontrar una disposición
    válida de las reinas en el tablero.
    """
    
    def __init__(self):
        """Inicializa el puzzle con parámetros básicos"""
        self.tamano = 8  # Tamaño estándar del tablero de ajedrez (8x8)
        self.max_iter = 1000  # Número máximo de iteraciones permitidas
        
    def generar_estado_inicial(self) -> List[int]:
        """
        Genera una configuración inicial aleatoria de las reinas.
        
        Returns:
            List[int]: Una lista donde cada índice representa una columna (0-7)
                      y el valor representa la fila (0-7) donde se coloca la reina.
        """
        return [random.randint(0, self.tamano-1) for _ in range(self.tamano)]
    
    def calcular_conflictos(self, estado: List[int]) -> int:
        """
        Calcula cuántos pares de reinas se están atacando mutuamente.
        
        Args:
            estado (List[int]): La disposición actual de las reinas.
            
        Returns:
            int: Número total de conflictos (pares de reinas atacándose).
        """
        conflictos = 0
        # Compara cada reina con todas las demás
        for i in range(len(estado)):
            for j in range(i+1, len(estado)):
                # Conflicto si están en la misma fila o en diagonal
                if estado[i] == estado[j] or abs(i-j) == abs(estado[i]-estado[j]):
                    conflictos += 1
        return conflictos
    
    def generar_vecino(self, estado: List[int]) -> List[int]:
        """
        Genera un estado vecino moviendo una sola reina a una nueva fila.
        
        Args:
            estado (List[int]): La disposición actual de las reinas.
            
        Returns:
            List[int]: Una nueva disposición con un pequeño cambio.
        """
        vecino = estado.copy()  # Copia el estado actual
        col = random.randint(0, self.tamano-1)  # Elige una columna aleatoria
        # Mueve la reina a una fila aleatoria (puede ser la misma)
        vecino[col] = random.randint(0, self.tamano-1)
        return vecino
    
    def escalar_colina(self) -> Tuple[List[int], int]:
        """
        Implementa el algoritmo de Ascensión de Colinas:
        1. Comienza con un estado aleatorio
        2. Genera vecinos (pequeñas modificaciones)
        3. Se mueve al vecino con menos conflictos
        4. Repite hasta encontrar solución o alcanzar max_iter
        
        Returns:
            Tuple[List[int], int]: La mejor solución encontrada y su número de conflictos.
        """
        estado_actual = self.generar_estado_inicial()
        conflictos_actual = self.calcular_conflictos(estado_actual)
        
        for iteracion in range(self.max_iter):
            # Si encontramos solución perfecta, terminar
            if conflictos_actual == 0:
                break
                
            # Generar un estado vecino
            vecino = self.generar_vecino(estado_actual)
            conflictos_vecino = self.calcular_conflictos(vecino)
            
            # Si el vecino es mejor, movernos a él
            if conflictos_vecino < conflictos_actual:
                estado_actual, conflictos_actual = vecino, conflictos_vecino
        
        return estado_actual, conflictos_actual
    
    def imprimir_tablero(self, estado: List[int]):
        """
        Muestra gráficamente el tablero con las reinas.
        
        Args:
            estado (List[int]): La disposición de las reinas a mostrar.
        """
        print("\nTablero:")
        for fila in range(self.tamano):
            for col in range(self.tamano):
                if estado[col] == fila:
                    print("♛ ", end="")  # Imprime una reina
                else:
                    print("· ", end="")  # Imprime casilla vacía
            print()  # Nueva línea al final de cada fila

# Bloque principal de ejecución
if __name__ == "__main__":
    print("♟️♟️♟️ Resolviendo el Problema de las 8 Reinas ♟️♟️♟️")
    print("Objetivo: Colocar 8 reinas sin que se ataquen mutuamente")
    print("Algoritmo: Búsqueda de Ascensión de Colinas\n")
    
    puzzle = Puzzle8Reinas()
    
    print("Buscando solución... (Puede tomar varios intentos)")
    solucion, conflictos = puzzle.escalar_colina()
    
    if conflictos == 0:
        print("\n✅ ¡Solución encontrada! Ninguna reina se ataca")
    else:
        print(f"\n⚠️ Mejor solución encontrada (con {conflictos} pares en conflicto)")
    
    # Mostrar resultados
    puzzle.imprimir_tablero(solucion)
    
    print("\n📊 Detalle de posiciones (Columna:Fila):")
    for col, fila in enumerate(solucion):
        print(f"Columna {col+1}: Fila {fila+1}")
    
    if conflictos > 0:
        print("\n💡 Consejo: Ejecute nuevamente el programa para buscar una solución mejor")