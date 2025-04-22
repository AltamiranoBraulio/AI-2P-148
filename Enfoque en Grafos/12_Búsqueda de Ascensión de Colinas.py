import random
from math import sqrt
from typing import List, Tuple, Dict

Punto = Tuple[float, float, str]

class RepartidorPizzas:
    def __init__(self, ubicaciones: List[Punto]):
        self.ubicaciones = ubicaciones
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')

    def distancia(self, a: Punto, b: Punto) -> float:
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def distancia_total(self, ruta: List[Punto]) -> float:
        total = 0
        for i in range(len(ruta)-1):
            total += self.distancia(ruta[i], ruta[i+1])
        total += self.distancia(ruta[-1], ruta[0])
        return total
    
        def generar_vecino(self, ruta: List[Punto]) -> List[Punto]:
        vecino = ruta.copy()
        i, j = random.sample(range(len(vecino)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino
    
        def escalar_colina(self, max_iter=1000):
        ruta_actual = self.ubicaciones.copy()
        random.shuffle(ruta_actual)
        distancia_actual = self.distancia_total(ruta_actual)


        for _ in range(max_iter):
            vecino = self.generar_vecino(ruta_actual)
            distancia_vecino = self.distancia_total(vecino)

            if distancia_vecino < distancia_actual:
                ruta_actual = vecino
               
                           else:

continue
        return self.mejor_ruta, self.mejor_distancia

if __name__ == "__main__":

    ubicaciones = [
0, 0, "Pizzería"),       # Punto de partida
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