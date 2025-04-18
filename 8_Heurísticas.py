# Importamos el módulo math para operaciones matemáticas avanzadas
# (como sqrt para calcular raíces cuadradas)
import math

# Importamos namedtuple del módulo collections para crear estructuras de datos ligeras
# que combinan las ventajas de tuplas y diccionarios
from collections import namedtuple

# Creamos un tipo de dato llamado "Ciudad" usando namedtuple
# Esto es como definir una clase minimalista con campos fijos:
# - nombre: String con el nombre de la ciudad
# - x: Coordenada horizontal (puede ser longitud o posición en grid)
# - y: Coordenada vertical (puede ser latitud o posición en grid)
Ciudad = namedtuple('Ciudad', ['nombre', 'x', 'y'])

# Creamos un diccionario que mapea identificadores de ciudad (letras)
# a objetos Ciudad con sus coordenadas específicas
# Ejemplo: 'A' -> Ciudad(nombre='A', x=0, y=0)
ciudades = {
    'A': Ciudad('A', 0, 0),  # Ciudad A en el origen (0,0)
    'B': Ciudad('B', 2, 4),  # Ciudad B en posición (2,4)
    'C': Ciudad('C', 5, 2),  # Ciudad C en posición (5,2)
    'D': Ciudad('D', 6, 6),  # Ciudad D en posición (6,6)
    'E': Ciudad('E', 8, 3)   # Ciudad E en posición (8,3)
}

# Definición de la heurística de distancia euclidiana (línea recta)
# Parámetros:
# - actual: Objeto Ciudad de partida
# - objetivo: Objeto Ciudad destino
def distancia_euclidiana(actual, objetivo):
    # Calculamos la diferencia en el eje x (delta x)
    dx = actual.x - objetivo.x
    
    # Calculamos la diferencia en el eje y (delta y)
    dy = actual.y - objetivo.y
    
    # Teorema de Pitágoras: sqrt(dx² + dy²)
    return math.sqrt(dx**2 + dy**2)

# Definición de la heurística de distancia Manhattan (suma de diferencias)
# Ideal para movimientos en cuadrícula (como calles perpendiculares)
def distancia_manhattan(actual, objetivo):
    # Suma del valor absoluto de las diferencias en x e y
    return abs(actual.x - objetivo.x) + abs(actual.y - objetivo.y)

# Definición de la heurística de distancia Chebyshev (máxima diferencia)
# Útil cuando los movimientos diagonales tienen el mismo costo que los rectos
def distancia_chebyshev(actual, objetivo):
    # Tomamos el máximo valor entre las diferencias en x e y
    return max(abs(actual.x - objetivo.x), abs(actual.y - objetivo.y))

# Seleccionamos la ciudad origen (en este caso 'A')
origen = ciudades['A']  # Obtenemos el objeto Ciudad correspondiente a 'A'

# Seleccionamos la ciudad destino (en este caso 'D')
destino = ciudades['D']  # Obtenemos el objeto Ciudad correspondiente a 'D'

# Mostramos un encabezado con emojis para mejor visualización
# Usamos f-strings para formateo dinámico (disponible desde Python 3.6+)
print(f"📡 Calculando heurísticas de {origen.nombre} a {destino.nombre}:")

# Calculamos y mostramos la distancia euclidiana
# :.2f formatea el número con 2 decimales
print(f"📍 CDMX: {distancia_euclidiana(origen, destino):.2f} km")

# Calculamos y mostramos la distancia Manhattan
print(f"📍 GDL: {distancia_manhattan(origen, destino)} km")

# Calculamos y mostramos la distancia Chebyshev
print(f"📍 MTY: {distancia_chebyshev(origen, destino)} km")