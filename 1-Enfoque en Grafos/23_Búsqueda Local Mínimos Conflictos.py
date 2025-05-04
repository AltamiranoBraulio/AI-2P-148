import random
import numpy as np

class NReinasMinimosConflictos:
    def __init__(self, n=8):
        """Inicializa el tablero de N-Reinas"""
        self.n = n
        self.reinas = list(range(n))  # Cada índice es una columna, el valor es la fila
        self.conflictos = [0] * n     # Contador de conflictos por reina
        
        # Inicializar colocando cada reina en una fila aleatoria
        random.shuffle(self.reinas)
        self.actualizar_todos_conflictos()
        
    def calcular_conflictos(self, col, fila):
        """Calcula cuántas reinas atacan a la reina en (col, fila)"""
        count = 0
        for otra_col in range(self.n):
            if otra_col == col:
                continue
            otra_fila = self.reinas[otra_col]
            # Misma fila o misma diagonal
            if otra_fila == fila or abs(otra_fila - fila) == abs(otra_col - col):
                count += 1
        return count
    
    def actualizar_todos_conflictos(self):
        """Actualiza el contador de conflictos para todas las reinas"""
        for col in range(self.n):
            self.conflictos[col] = self.calcular_conflictos(col, self.reinas[col])
    
    def reina_mas_conflictiva(self):
        """Encuentra una de las reinas con más conflictos (puede haber empates)"""
        max_conflictos = max(self.conflictos)
        candidatas = [col for col, c in enumerate(self.conflictos) if c == max_conflictos]
        return random.choice(candidatas)
    
    def mover_reina_min_conflictos(self, col):
        """Mueve la reina en 'col' a la fila con menos conflictos"""
        conflictos_por_fila = []
        for fila in range(self.n):
            conflictos = self.calcular_conflictos(col, fila)
            conflictos_por_fila.append(conflictos)
        
        min_conflictos = min(conflictos_por_fila)
        mejores_filas = [fila for fila, c in enumerate(conflictos_por_fila) if c == min_conflictos]
        
        # Elegir aleatoriamente entre las mejores filas (puede incluir la actual)
        nueva_fila = random.choice(mejores_filas)
        self.reinas[col] = nueva_fila
        self.conflictos[col] = min_conflictos
    
    def resolver(self, max_iter=1000):
        """Algoritmo principal de mínimos conflictos"""
        for paso in range(max_iter):
            if sum(self.conflictos) == 0:  # Solución encontrada
                print(f"¡Solución encontrada en {paso} pasos!")
                return True
                
            # 1. Seleccionar una reina conflictiva
            col = self.reina_mas_conflictiva()
            
            # 2. Moverla a la posición con menos conflictos
            self.mover_reina_min_conflictos(col)
            
            # 3. Actualizar conflictos de reinas afectadas
            for otra_col in range(self.n):
                if otra_col != col:
                    fila = self.reinas[otra_col]
                    self.conflictos[otra_col] = self.calcular_conflictos(otra_col, fila)
        
        print("No se encontró solución en el número máximo de iteraciones")
        return False
    
    def dibujar_tablero(self):
        """Visualización ASCII del tablero"""
        tablero = np.zeros((self.n, self.n), dtype=int)
        for col, fila in enumerate(self.reinas):
            tablero[fila][col] = 1
            
        print("\nTablero actual:")
        for fila in tablero:
            print(" ".join("♛" if celda else "·" for celda in fila))
        print(f"Conflictos totales: {sum(self.conflictos)}\n")

# Ejemplo de uso interactivo
if __name__ == "__main__":
    print("♟️ Resolviendo el Problema de las N-Reinas con Mínimos Conflictos ♟️")
    n = int(input("Ingrese el número de reinas (ej. 8): "))
    
    solver = NReinasMinimosConflictos(n)
    print("\nConfiguración inicial:")
    solver.dibujar_tablero()
    
    input("Presione Enter para comenzar la búsqueda...")
    
    if solver.resolver():
        print("\nSolución final encontrada:")
        solver.dibujar_tablero()
        print("Posiciones de las reinas (columna:fila):")
        for col, fila in enumerate(solver.reinas):
            print(f"Columna {col}: Fila {fila}")
    else:
        solver.dibujar_tablero()
        print("Intente ejecutar nuevamente o aumentar el número máximo de iteraciones")