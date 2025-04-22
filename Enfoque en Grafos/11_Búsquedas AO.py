# Importación de librerías necesarias
import random  # Para generar números aleatorios y mezclar listas
from math import sqrt  # Para calcular raíz cuadrada (en la distancia euclidiana)
from typing import List, Tuple, Dict  # Para anotaciones de tipo

# Definimos un tipo de dato Punto como una tupla con:
# - float: coordenada x
# - float: coordenada y 
# - str: nombre del lugar
Punto = Tuple[float, float, str]

class RepartidorPizzas:
    def __init__(self, ubicaciones: List[Punto]):
        """Inicializa el repartidor con:
        - ubicaciones: lista de puntos a visitar
        - mejor_ruta: para almacenar la mejor solución encontrada
        - mejor_distancia: distancia de la mejor ruta (inicialmente infinito)"""
        self.ubicaciones = ubicaciones
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')  # Inicializado a infinito para que cualquier ruta sea mejor
    
    def distancia(self, a: Punto, b: Punto) -> float:
        """Calcula la distancia euclidiana entre dos puntos (a y b)
        Fórmula: sqrt((x2-x1)² + (y2-y1)²)"""
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def distancia_total(self, ruta: List[Punto]) -> float:
        """Calcula la distancia total de una ruta completa:
        1. Suma las distancias entre puntos consecutivos
        2. Agrega la distancia de regreso al punto inicial"""
        total = 0
        # Sumar distancias entre cada par de puntos consecutivos
        for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        # Agregar distancia de regreso al punto inicial (para completar el circuito)
        total += self.distancia(ruta[-1], ruta[0])
        return total
    
    def generar_vecino(self, ruta: List[Punto]) -> List[Punto]:
        """Genera una ruta vecina mediante:
        1. Copiar la ruta actual
        2. Seleccionar dos índices aleatorios
        3. Intercambiar los puntos en esos índices"""
        vecino = ruta.copy()  # Crear copia para no modificar la original
        # Seleccionar dos índices diferentes aleatoriamente
        i, j = random.sample(range(len(vecino)), 2)
        # Intercambiar los puntos en esas posiciones
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino
    
    def escalar_colina(self, max_iter=1000):
        """Algoritmo principal de ascensión de colinas:
        1. Comienza con ruta aleatoria
        2. Genera vecinos (soluciones cercanas)
        3. Se mueve a mejores vecinos
        4. Repite hasta max_iter o no encontrar mejoras"""
        # Paso 1: Generar ruta inicial aleatoria
        ruta_actual = self.ubicaciones.copy()
        random.shuffle(ruta_actual)
        distancia_actual = self.distancia_total(ruta_actual)
        
        # Paso 2: Bucle principal de iteraciones
        for _ in range(max_iter):
            # Generar una solución vecina
            vecino = self.generar_vecino(ruta_actual)
            distancia_vecino = self.distancia_total(vecino)
            
            # Comparar con solución actual
            if distancia_vecino < distancia_actual:  # ¿Es mejor?
                # Moverse a la solución vecina
                ruta_actual, distancia_actual = vecino, distancia_vecino
                
                # Actualizar mejor solución global si corresponde
                if distancia_actual < self.mejor_distancia:
                    self.mejor_ruta = ruta_actual.copy()
                    self.mejor_distancia = distancia_actual
            else:
                # Continuar buscando (aquí se podrían agregar criterios adicionales)
                continue
        
        # Retornar la mejor solución encontrada
        return self.mejor_ruta, self.mejor_distancia

# Bloque principal de ejecución
if __name__ == "__main__":
    # Definición de los puntos de entrega:
    # Cada tupla contiene (coordenada_x, coordenada_y, nombre_del_lugar)
    ubicaciones = [
        (0, 0, "Pizzería"),       # Punto de partida (origen)
        (2, 4, "Casa de Juan"),
        (3, 1, "Oficina A"),
        (5, 2, "Oficina B"),
        (4, 5, "Casa de María"),
        (1, 3, "Parque")
    ]
    
    # Crear instancia del repartidor
    repartidor = RepartidorPizzas(ubicaciones)
    # Ejecutar el algoritmo de ascensión de colinas
    mejor_ruta, distancia = repartidor.escalar_colina()
    
    # Mostrar resultados
    print("🚴 Optimización de Ruta para Repartidor de Pizzas 🍕")
    print("\n📍 Puntos de entrega:")
    for punto in ubicaciones:
        print(f"- {punto[2]} ({punto[0]}, {punto[1]})")
    
    # Mostrar la mejor ruta encontrada
    print("\n🔍 Mejor ruta encontrada:")
    for i, punto in enumerate(mejor_ruta, 1):  # enumerate empieza en 1
        print(f"{i}. {punto[2]} ({punto[0]}, {punto[1]})")
    print(f"↩️ Volver a Pizzería (0, 0)")  # Para completar el circuito
    
    # Mostrar distancia total optimizada
    print(f"\n📏 Distancia total: {distancia:.2f} km")
    
    # Visualización ASCII del mapa
    print("\n🗺️ Representación gráfica:")
    # Calcular dimensiones del mapa
    max_x = max(p[0] for p in ubicaciones) + 1  # Ancho máximo + margen
    max_y = max(p[1] for p in ubicaciones) + 1  # Alto máximo + margen
    
    # Dibujar mapa fila por fila (de arriba a abajo)
    for y in range(int(max_y), -1, -1):  # Desde max_y hasta 0
        # Dibujar cada columna en la fila actual
        for x in range(int(max_x)+1):  # Desde 0 hasta max_x
            # Buscar si hay un punto de la ruta en esta coordenada
            for punto in mejor_ruta:
                if x == punto[0] and y == punto[1]:
                    print("📍", end="")  # Marcar punto de entrega
                    break
            else:  # Si no es punto de entrega
                if x == 0 and y == 0:
                    print("🍕", end="")  # Marcar pizzería
                else:
                    print("·", end="")  # Punto vacío
        print()  # Nueva línea al final de cada fila