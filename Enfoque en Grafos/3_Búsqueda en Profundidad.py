import time 
from collections import defaultdict

    videojuegos = {
        'The Witcher 3': ['RPG', 'Aventura', 'Mundo Abierto'],
    'Skyrim': ['RPG', 'Mundo Abierto', 'Fantasía'],
    'Dark Souls': ['RPG', 'Difícil', 'Fantasía'],
    'Overwatch': ['FPS', 'Competitivo', 'Multijugador'],
    'Valorant': ['FPS', 'Competitivo', 'Multijugador'],
    'Stardew Valley': ['Simulación', 'Relajante'],
    'Civilization VI': ['Estrategia', 'Turnos', 'Histórico'],
    'Portal 2': ['Puzzle', 'FPS', 'Ciencia Ficción'],
    'Hollow Knight': ['Metroidvania', 'Difícil', 'Aventura']
}

grafos_recomendaciones = defaultdict(list)
for juego, generos in videojuegos.items():
    for genero in generos:
        grafos_recomendaciones[genero].append(juego)

def dfs_recomendaciones(inicio, profundidad_max=3):

    visitados = set()
    recomendaciones = []

    pila = [(inicio, 0)]

    while pila:
        nodo, profundidad, camino = pila.pop()


        if nodo not in visitados and profundidad <= profundidad_max:
            visitados.add(nodo)
           
           if nodo in videojuegos ans nodo != inicio:
                recomendaciones.append(nodo, camino.copy(), profundidad)

                if nodo in grafos_recomendaciones:
                     for conexiones in grafos_recomendaciones[nodo]:
                       if conexion not in visitados:
                            nuevo_camino = camino + [conexiones]
                            pila.append((conexion, profundidad + 1, nuevo_camino))

            elif nodo in videojuegos:
                for genero in videojuegos[nodo]:
                     if genero not in visitados:
                          nuevo_camino = camino + [genero]
                          pila.append((genero, profundidad + 1, nuevo_camino))