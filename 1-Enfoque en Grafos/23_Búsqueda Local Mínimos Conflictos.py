import random  # Importa la librería random para generar números aleatorios.
import numpy as np  # Importa la librería numpy, que se usa para trabajar con arreglos de manera eficiente.

class NReinasMinimosConflictos:
    def __init__(self, n=8):
        """Inicializa el tablero de N-Reinas"""
        self.n = n  # El tamaño del tablero, n es el número de reinas y también el tamaño del tablero (n x n)
        self.reinas = list(range(n))  # Inicializa una lista de reinas. Cada reina está representada por un índice de columna, y el valor en ese índice es la fila de la reina.
        self.conflictos = [0] * n  # Lista para almacenar el número de conflictos de cada reina (por columna).

        # Inicializa las reinas colocándolas en posiciones aleatorias de filas (las columnas son fijas)
        random.shuffle(self.reinas)  # Mezcla la lista de las filas de las reinas para una distribución aleatoria.
        self.actualizar_todos_conflictos()  # Calcula el número de conflictos de cada reina después de la colocación aleatoria.

    def calcular_conflictos(self, col, fila):
        """Calcula cuántas reinas atacan a la reina en (col, fila)"""
        count = 0  # Inicializa un contador para los conflictos.
        for otra_col in range(self.n):  # Recorre todas las columnas (todas las reinas en el tablero).
            if otra_col == col:  # Si la columna es la misma que la que estamos evaluando, no hay conflicto.
                continue
            otra_fila = self.reinas[otra_col]  # Obtiene la fila de la otra reina.
            
            # Verifica si las reinas están en la misma fila o en la misma diagonal.
            if otra_fila == fila or abs(otra_fila - fila) == abs(otra_col - col):  # Verifica si hay conflicto en fila o diagonal.
                count += 1  # Incrementa el contador de conflictos.
        return count  # Retorna el número total de conflictos para esa reina.

    def actualizar_todos_conflictos(self):
        """Actualiza el contador de conflictos para todas las reinas"""
        for col in range(self.n):  # Recorre todas las columnas.
            self.conflictos[col] = self.calcular_conflictos(col, self.reinas[col])  # Actualiza el número de conflictos de cada reina.

    def reina_mas_conflictiva(self):
        """Encuentra una de las reinas con más conflictos (puede haber empates)"""
        max_conflictos = max(self.conflictos)  # Encuentra el número máximo de conflictos.
        candidatas = [col for col, c in enumerate(self.conflictos) if c == max_conflictos]  # Encuentra todas las reinas con el número máximo de conflictos.
        return random.choice(candidatas)  # Devuelve aleatoriamente una de las reinas con más conflictos.

    def mover_reina_min_conflictos(self, col):
        """Mueve la reina en 'col' a la fila con menos conflictos"""
        conflictos_por_fila = []  # Inicializa una lista para almacenar los conflictos de cada fila en la columna 'col'.
        for fila in range(self.n):  # Recorre todas las filas.
            conflictos = self.calcular_conflictos(col, fila)  # Calcula los conflictos para esa reina si se moviera a esa fila.
            conflictos_por_fila.append(conflictos)  # Agrega el número de conflictos de esa fila a la lista.

        min_conflictos = min(conflictos_por_fila)  # Encuentra el mínimo número de conflictos.
        mejores_filas = [fila for fila, c in enumerate(conflictos_por_fila) if c == min_conflictos]  # Encuentra todas las filas con el número mínimo de conflictos.

        # Elige aleatoriamente una de las mejores filas (puede ser la misma fila que tiene actualmente la reina).
        nueva_fila = random.choice(mejores_filas)
        self.reinas[col] = nueva_fila  # Mueve la reina a la nueva fila.
        self.conflictos[col] = min_conflictos  # Actualiza el número de conflictos de la reina.

    def resolver(self, max_iter=1000):
        """Algoritmo principal de mínimos conflictos"""
        for paso in range(max_iter):  # Limita el número de iteraciones para evitar un bucle infinito.
            if sum(self.conflictos) == 0:  # Si el total de conflictos es cero, significa que hemos encontrado una solución.
                print(f"¡Solución encontrada en {paso} pasos!")  # Imprime cuántos pasos fueron necesarios.
                return True  # Devuelve True indicando que se ha encontrado una solución.
                
            # 1. Seleccionar una reina conflictiva
            col = self.reina_mas_conflictiva()  # Selecciona la reina con más conflictos.
            
            # 2. Moverla a la posición con menos conflictos
            self.mover_reina_min_conflictos(col)  # Mueve esa reina a la fila con menos conflictos.
            
            # 3. Actualizar conflictos de reinas afectadas
            for otra_col in range(self.n):  # Recorre todas las columnas (excepto la columna actual).
                if otra_col != col:  # Si la reina no es la seleccionada.
                    fila = self.reinas[otra_col]  # Obtiene la fila de la reina.
                    self.conflictos[otra_col] = self.calcular_conflictos(otra_col, fila)  # Recalcula los conflictos de esa reina.

        print("No se encontró solución en el número máximo de iteraciones")  # Si no se encuentra solución, informa al usuario.
        return False  # Devuelve False indicando que no se ha encontrado una solución.

    def dibujar_tablero(self):
        """Visualización ASCII del tablero"""
        tablero = np.zeros((self.n, self.n), dtype=int)  # Crea una matriz de ceros para representar el tablero vacío.
        for col, fila in enumerate(self.reinas):  # Recorre todas las reinas.
            tablero[fila][col] = 1  # Marca la posición de cada reina en el tablero (1 significa que hay una reina en esa celda).
            
        print("\nTablero actual:")  # Imprime el tablero.
        for fila in tablero:  # Recorre cada fila del tablero.
            print(" ".join("♛" if celda else "·" for celda in fila))  # Muestra un símbolo de reina (♛) o un punto (·) dependiendo si hay una reina.
        print(f"Conflictos totales: {sum(self.conflictos)}\n")  # Muestra el total de los conflictos actuales.

# Ejemplo de uso interactivo
if __name__ == "__main__":  # Si se ejecuta el script, comienza este bloque.
    print("♟️ Resolviendo el Problema de las N-Reinas con Mínimos Conflictos ♟️")  # Imprime un mensaje introductorio.
    n = int(input("Ingrese el número de reinas (ej. 8): "))  # Solicita al usuario el número de reinas.

    solver = NReinasMinimosConflictos(n)  # Crea un objeto del solucionador con el número de reinas.
    print("\nConfiguración inicial:")  # Muestra la configuración inicial del tablero.
    solver.dibujar_tablero()  # Dibuja el tablero con las reinas en posiciones aleatorias.

    input("Presione Enter para comenzar la búsqueda...")  # Espera a que el usuario presione Enter para empezar.

    if solver.resolver():  # Intenta resolver el problema de las N-Reinas.
        print("\nSolución final encontrada:")  # Si se encuentra una solución, muestra el tablero final.
        solver.dibujar_tablero()  # Dibuja el tablero con la solución final.
        print("Posiciones de las reinas (columna:fila):")  # Muestra las posiciones finales de las reinas.
        for col, fila in enumerate(solver.reinas):
            print(f"Columna {col}: Fila {fila}")  # Imprime la posición de cada reina en el tablero.
    else:
        solver.dibujar_tablero()  # Si no se encuentra solución, muestra el tablero final.
        print("Intente ejecutar nuevamente o aumentar el número máximo de iteraciones")  # Informa al usuario que intente de nuevo.
