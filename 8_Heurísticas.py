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
