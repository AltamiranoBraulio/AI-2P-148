import math
from collections import namedtuple
Ciudad = namedtuple('Ciudad', ['nombre', 'x', 'y'])
ciudades = {
    'A': Ciudad('A', 0, 0),
    'B': Ciudad('B', 2, 4),
    'C': Ciudad('C', 5, 2),
    'D': Ciudad('D', 6, 6),
    'E': Ciudad('E', 8, 3)
}

def distancia_euclidiana(actual, objetivo):
    dx = actual.x - objetivo.x
    dy = actual.y - objetivo.y
    return math.sqrt(dx**2 + dy**2)
def distancia_manhattan(actual, objetivo):
    return abs(actual.x - objetivo.x) + abs(actual.y - objetivo.y)
def distancia_chebyshev(actual, objetivo):
    return max(abs(actual.x - objetivo.x), abs(actual.y - objetivo.y))
origen = ciudades['A']
destino = ciudades['D']
print(f"📡 Calculando heurísticas de {origen.nombre} a {destino.nombre}:")
print(f"📍 CDMX: {distancia_euclidiana(origen, destino):.2f} km")
print(f"📍 GDL: {distancia_manhattan(origen, destino)} km")
print(f"📍 MTY: {distancia_chebyshev(origen, destino)} km")
