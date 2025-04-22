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

            for vecino in vecinos:
                # Encontrar qué puntos se intercambiaron
                cambios = [(i, vecino[i]) for i in range(len(vecino)) 
                          if vecino[i] != ruta_actual[i]]
                movimiento = tuple(sorted((cambios[0][0], cambios[1][0])))
                
                distancia = self.distancia_total(vecino)
                
                # 4. Verificar si es el mejor vecino no tabú o cumple aspiración
                if (movimiento not in self.lista_tabu) or \
                   (self.criterio_aspiración(distancia)):
                    if distancia < mejor_distancia:
                        mejor_vecino = vecino
                        mejor_distancia = distancia
                        mejor_movimiento = movimiento

                        if mejor_vecino is not None:
                ruta_actual = mejor_vecino
                distancia_actual = mejor_distancia
                
                # 6. Actualizar lista tabú
                self.lista_tabu.append(mejor_movimiento)
                if len(self.lista_tabu) > self.tamano_tabu:
                    self.lista_tabu.pop(0)
                
                # 7. Actualizar mejor solución global
                if distancia_actual < self.mejor_distancia:
                    self.mejor_ruta = ruta_actual.copy()
                    self.mejor_distancia = distancia_actual
                    print(f"Iter {iteracion}: Nueva mejor distancia: {self.mejor_distancia:.2f}")
        
        return self.mejor_ruta, self.mejor_distancia

if __name__ == "__main__":
    # Puntos en la ciudad: (x, y, nombre)
    puntos = [
        (0, 0, "Base"),          # Punto de partida
        (2, 4, "Aeropuerto"),
        (3, 1, "Centro Comercial"),
        (5, 2, "Estación Central"),
        (4, 5, "Teatro"),
        (1, 3, "Hospital")
    ]
    
    print("🚖 Optimización de Ruta para Taxi con Búsqueda Tabú 🚖")
    print("Objetivo: Minimizar la distancia recorrida visitando todos los puntos")
    
    optimizador = OptimizadorRutas(puntos)
    mejor_ruta, distancia = optimizador.busqueda_tabu()
    
    print("\n📍 Mejor ruta encontrada:")
    for i, punto in enumerate(mejor_ruta, 1):
        print(f"{i}. {punto[2]} ({punto[0]}, {punto[1]})")
    print(f"↩️ Volver a Base (0, 0)")
    