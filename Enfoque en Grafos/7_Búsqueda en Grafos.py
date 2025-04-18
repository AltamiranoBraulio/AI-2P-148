from collections import deque
def recomendar_amigos(grafo_red, usuario_actual, niveles=3):

    recomendaciones = {i: set() for i in range(1, niveles+1)}

