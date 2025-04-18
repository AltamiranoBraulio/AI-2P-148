import random
from math import sqrt
from typing import List, Tuple, Dict

# Representación de puntos en el mapa (coordenadas x, y y nombre del lugar)
Punto = Tuple[float, float, str]

class RepartidorPizzas:
    def __init__(self, ubicaciones: List[Punto]):
        self.ubicaciones = ubicaciones
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
    
    def distancia(self, a: Punto, b: Punto) -> float:
        """Calcula la distancia euclidiana entre dos puntos"""
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def distancia_total(self, ruta: List[Punto]) -> float:
        """Calcula la distancia total de una ruta"""
        total = 0
        for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        # Regresar al punto inicial
        total += self.distancia(ruta[-1], ruta[0])
        return total
    
    def generar_vecino(self, ruta: List[Punto]) -> List[Punto]:
        """Genera una ruta vecina intercambiando dos puntos aleatorios"""
        vecino = ruta.copy()
        i, j = random.sample(range(len(vecino)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino
    
    def escalar_colina(self, max_iter=1000):
        """Implementación de la búsqueda de ascensión de colinas"""
        # Ruta inicial aleatoria
        ruta_actual = self.ubicaciones.copy()
        random.shuffle(ruta_actual)
        distancia_actual = self.distancia_total(ruta_actual)
        
        for _ in range(max_iter):
            # Generar vecino
            vecino = self.generar_vecino(ruta_actual)
            distancia_vecino = self.distancia_total(vecino)
            
            # Si el vecino es mejor, movernos allí
            if distancia_vecino < distancia_actual:
                ruta_actual, distancia_actual = vecino, distancia_vecino
                
                # Actualizar mejor solución encontrada
                if distancia_actual < self.mejor_distancia:
                    self.mejor_ruta = ruta_actual.copy()
                    self.mejor_distancia = distancia_actual
            else:
                # Podríamos agregar aquí criterios de terminación temprana
                continue
        
        return self.mejor_ruta, self.mejor_distancia

# Ejemplo de uso
if __name__ == "__main__":
    # Pizzería y puntos de entrega
    ubicaciones = [
        (0, 0, "Pizzería"),       # Punto de partida
        (2, 4, "Casa de Juan"),
        (3, 1, "Oficina A"),
        (5, 2, "Oficina B"),
        (4, 5, "Casa de María"),
        (1, 3, "Parque")
    ]
    
    repartidor = RepartidorPizzas(ubicaciones)
    mejor_ruta, distancia = repartidor.escalar_colina()
    
    print("🚴 Optimización de Ruta para Repartidor de Pizzas 🍕")
    print("\n📍 Puntos de entrega:")
    for punto in ubicaciones:
        print(f"- {punto[2]} ({punto[0]}, {punto[1]})")
    
    print("\n🔍 Mejor ruta encontrada:")
    for i, punto in enumerate(mejor_ruta, 1):
        print(f"{i}. {punto[2]} ({punto[0]}, {punto[1]})")
    print(f"↩️ Volver a Pizzería (0, 0)")
    
    print(f"\n📏 Distancia total: {distancia:.2f} km")
    
    # Visualización simple
    print("\n🗺️ Representación gráfica:")
    max_x = max(p[0] for p in ubicaciones) + 1
    max_y = max(p[1] for p in ubicaciones) + 1
    
    for y in range(int(max_y), -1, -1):
        for x in range(int(max_x)+1):
            for punto in mejor_ruta:
                if x == punto[0] and y == punto[1]:
                    print("📍", end="")
                    break
            else:
                if x == 0 and y == 0:
                    print("🍕", end="")
                else:
                    print("·", end="")
        print()