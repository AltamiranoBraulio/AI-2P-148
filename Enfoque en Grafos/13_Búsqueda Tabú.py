# Importación de módulos necesarios
import random  # Para generación de números aleatorios y selección aleatoria
from math import sqrt  # Para calcular raíces cuadradas (en la distancia euclidiana)
from typing import List, Tuple, Dict  # Para anotaciones de tipo que mejoran la legibilidad

# Definición de tipo personalizado: Punto es una tupla con:
# - float: coordenada x
# - float: coordenada y 
# - str: nombre del lugar
Punto = Tuple[float, float, str]

class OptimizadorRutas:
    """
    Clase principal que implementa el algoritmo de Búsqueda Tabú
    para optimizar rutas de taxi en una ciudad imaginaria.
    """
    
    def __init__(self, ubicaciones: List[Punto]):
        """
        Inicializa el optimizador con:
        - ubicaciones: Lista de puntos a visitar (incluyendo la base)
        - lista_tabu: Lista que almacena movimientos prohibidos temporalmente
        - tamano_tabu: Número máximo de movimientos a mantener en la lista tabú
        - mejor_ruta: Almacena la mejor solución encontrada hasta el momento
        - mejor_distancia: Distancia de la mejor ruta encontrada
        """
        self.ubicaciones = ubicaciones  # Lista completa de puntos a visitar
        self.lista_tabu = []  # Inicializa lista tabú vacía
        self.tamano_tabu = 5  # Tamaño máximo de la lista tabú (experimental)
        self.mejor_ruta = None  # Aquí se guardará la mejor ruta encontrada
        self.mejor_distancia = float('inf')  # Inicializado a infinito para cualquier ruta sea mejor
    
    def distancia(self, a: Punto, b: Punto) -> float:
        """
        Calcula la distancia euclidiana entre dos puntos en el plano 2D.
        Fórmula: sqrt((x2-x1)² + (y2-y1)²)
        
        Args:
            a: Primer punto (x1, y1, nombre1)
            b: Segundo punto (x2, y2, nombre2)
            
        Returns:
            float: Distancia entre los puntos a y b
        """
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def distancia_total(self, ruta: List[Punto]) -> float:
        """
        Calcula la distancia total de una ruta completa, incluyendo el
        regreso al punto de origen (para completar el circuito).
        
        Args:
            ruta: Lista ordenada de puntos a visitar
            
        Returns:
            float: Distancia total de la ruta (incluyendo regreso a inicio)
        """
        total = 0  # Acumulador de distancia
        
        # Sumar distancias entre puntos consecutivos
        for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        
        # Agregar distancia de regreso al punto inicial
        total += self.distancia(ruta[-1], ruta[0])
        
        return total
    
    def generar_vecinos(self, ruta: List[Punto]) -> List[List[Punto]]:
        """
        Genera soluciones vecinas intercambiando dos puntos aleatorios
        en la ruta actual. Genera 5 vecinos diferentes por defecto.
        
        Args:
            ruta: Ruta actual a partir de la cual generar vecinos
            
        Returns:
            List[List[Punto]]: Lista de rutas vecinas generadas
        """
        vecinos = []  # Lista para almacenar las rutas vecinas
        
        for _ in range(5):  # Generar exactamente 5 vecinos
            vecino = ruta.copy()  # Crear copia para no modificar la original
            # Seleccionar dos índices diferentes al azar
            i, j = random.sample(range(len(vecino)), 2)
            # Intercambiar los puntos en esas posiciones
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
        
        return vecinos
    
    def criterio_aspiración(self, distancia: float) -> bool:
        """
        Determina si un movimiento tabú debe ser permitido porque
        es excepcionalmente bueno (criterio de aspiración).
        
        Args:
            distancia: Distancia de la solución vecina a evaluar
            
        Returns:
            bool: True si el movimiento debe ser permitido a pesar de ser tabú
        """
        return distancia < self.mejor_distancia * 0.9  # 10% mejor que el mejor actual
    
    def busqueda_tabu(self, max_iter: int = 100):
        """
        Implementación del algoritmo de Búsqueda Tabú para optimización
        de rutas. Sigue estos pasos principales:
        1. Generar solución inicial aleatoria
        2. Generar vecindario de soluciones cercanas
        3. Seleccionar mejor vecino no tabú (o que cumpla aspiración)
        4. Actualizar lista tabú y mejor solución global
        5. Repetir hasta cumplir criterio de parada
        
        Args:
            max_iter: Número máximo de iteraciones permitidas
            
        Returns:
            Tuple[List[Punto], float]: Mejor ruta encontrada y su distancia
        """
        # 1. Inicialización: generar solución aleatoria
        ruta_actual = self.ubicaciones.copy()
        random.shuffle(ruta_actual)  # Mezclar para obtener ruta inicial aleatoria
        distancia_actual = self.distancia_total(ruta_actual)
        
        # Inicializar mejor solución global
        self.mejor_ruta = ruta_actual.copy()
        self.mejor_distancia = distancia_actual
        
        # 2. Bucle principal de iteraciones
        for iteracion in range(max_iter):
            # 3. Generación de vecindario
            vecinos = self.generar_vecinos(ruta_actual)
            
            # Variables para trackear el mejor vecino en esta iteración
            mejor_vecino = None
            mejor_distancia = float('inf')
            mejor_movimiento = None
            
            # 4. Evaluación de vecinos
            for vecino in vecinos:
                # Identificar qué índices se intercambiaron
                cambios = [(i, vecino[i]) for i in range(len(vecino)) 
                          if vecino[i] != ruta_actual[i]]
                # Crear tupla ordenada para representar el movimiento
                movimiento = tuple(sorted((cambios[0][0], cambios[1][0])))
                
                # Calcular distancia de esta solución vecina
                distancia = self.distancia_total(vecino)
                
                # 5. Criterios de aceptación:
                # - Movimiento no está en lista tabú O
                # - Cumple criterio de aspiración (es excepcionalmente bueno)
                if (movimiento not in self.lista_tabu) or \
                   (self.criterio_aspiración(distancia)):
                    if distancia < mejor_distancia:
                        # Actualizar mejor vecino de esta iteración
                        mejor_vecino = vecino
                        mejor_distancia = distancia
                        mejor_movimiento = movimiento
            
            # 6. Actualización de estado
            if mejor_vecino is not None:
                # Mover a la mejor solución vecina encontrada
                ruta_actual = mejor_vecino
                distancia_actual = mejor_distancia
                
                # Actualizar lista tabú con el movimiento realizado
                self.lista_tabu.append(mejor_movimiento)
                # Mantener tamaño fijo de lista tabú (eliminar el más viejo)
                if len(self.lista_tabu) > self.tamano_tabu:
                    self.lista_tabu.pop(0)
                
                # 7. Actualizar mejor solución global si corresponde
                if distancia_actual < self.mejor_distancia:
                    self.mejor_ruta = ruta_actual.copy()
                    self.mejor_distancia = distancia_actual
                    print(f"Iter {iteracion}: Nueva mejor distancia: {self.mejor_distancia:.2f}")
        
        # Devolver mejor solución encontrada
        return self.mejor_ruta, self.mejor_distancia

# Bloque principal de ejecución
if __name__ == "__main__":
    # Definición de puntos en la ciudad (coordenadas x, y y nombre)
    puntos = [
        (0, 0, "Base"),          # Punto de partida (origen)
        (2, 4, "Aeropuerto"),
        (3, 1, "Centro Comercial"),
        (5, 2, "Estación Central"),
        (4, 5, "Teatro"),
        (1, 3, "Hospital")
    ]
    
    # Presentación del programa
    print("🚖 Optimización de Ruta para Taxi con Búsqueda Tabú 🚖")
    print("Objetivo: Minimizar la distancia recorrida visitando todos los puntos\n")
    
    # Crear instancia del optimizador
    optimizador = OptimizadorRutas(puntos)
    # Ejecutar algoritmo de Búsqueda Tabú
    mejor_ruta, distancia = optimizador.busqueda_tabu()
    
    # Mostrar resultados
    print("\n📍 Mejor ruta encontrada:")
    for i, punto in enumerate(mejor_ruta, 1):  # enumerate empieza en 1
        print(f"{i}. {punto[2]} ({punto[0]}, {punto[1]})")
    print(f"↩️ Volver a Base (0, 0)")  # Para indicar el cierre del circuito
    
    # Mostrar métrica de calidad
    print(f"\n📏 Distancia total optimizada: {distancia:.2f} km")
    
    # Visualización ASCII del mapa
    print("\n🗺️ Mapa de la ruta optimizada:")
    # Calcular dimensiones del mapa
    max_x = max(p[0] for p in puntos) + 1  # Ancho máximo + margen
    max_y = max(p[1] for p in puntos) + 1  # Alto máximo + margen
    
    # Dibujar mapa fila por fila (de arriba a abajo)
    for y in range(int(max_y), -1, -1):  # Desde max_y hasta 0
        # Dibujar cada columna en la fila actual
        for x in range(int(max_x)+1):  # Desde 0 hasta max_x
            # Buscar si hay un punto de la ruta en esta coordenada
            for punto in mejor_ruta:
                if x == punto[0] and y == punto[1]:
                    print("🚖", end="")  # Marcar punto de entrega
                    break
            else:  # Si no es punto de entrega
                if x == 0 and y == 0:
                    print("🏠", end="")  # Marcar base (origen)
                else:
                    print("· ", end="")  # Punto vacío
        print()  # Nueva línea al final de cada fila