# Importación de librerías necesarias
import time  # Para pausas en la ejecución
from collections import defaultdict  # Para crear diccionarios con valores por defecto

# =============================================
# BASE DE DATOS DE VIDEOJUEGOS Y SUS GÉNEROS
# =============================================
# Diccionario donde cada clave es un juego y el valor es una lista de sus géneros
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

# =============================================
# CONSTRUCCIÓN DEL GRAFO DE RECOMENDACIONES
# =============================================
# Creamos un grafo que mapea géneros a juegos que pertenecen a ese género
grafo_recomendaciones = defaultdict(list)  # Crea un diccionario con listas vacías por defecto

# Iteramos sobre cada juego y sus géneros para construir el grafo
for juego, generos in videojuegos.items():
    for genero in generos:
        # Añadimos el juego a la lista de juegos de este género
        grafo_recomendaciones[genero].append(juego)

# =============================================
# ALGORITMO DFS PARA RECOMENDACIONES
# =============================================
def dfs_recomendaciones(inicio, profundidad_max=3):
    """
    Implementación de Depth-First Search (DFS) para encontrar juegos relacionados.
    
    Parámetros:
    - inicio: Nombre del juego de partida (str)
    - profundidad_max: Máxima profundidad de búsqueda (int)
    
    Retorna:
    - Lista de tuplas con (juego recomendado, camino de conexión, profundidad)
    """
    
    # Conjunto para llevar registro de nodos ya visitados
    visitados = set()
    
    # Lista para almacenar las recomendaciones encontradas
    recomendaciones = []
    
    # Pila para implementar DFS: cada elemento es una tupla (nodo, profundidad, camino)
    pila = [(inicio, 0, [inicio])]  # Inicializamos con el nodo de inicio
    
    # Mientras haya nodos por explorar en la pila
    while pila:
        # Extraemos el último nodo añadido (LIFO - Last In First Out)
        nodo, profundidad, camino = pila.pop()
        
        # Verificamos si el nodo no ha sido visitado y está dentro de la profundidad máxima
        if nodo not in visitados and profundidad <= profundidad_max:
            # Marcamos el nodo como visitado
            visitados.add(nodo)
            
            # Si el nodo es un juego (no género) y no es el juego inicial
            if nodo in videojuegos and nodo != inicio:
                # Añadimos a las recomendaciones: (juego, camino, profundidad)
                recomendaciones.append((nodo, camino.copy(), profundidad))
            
            # Si el nodo es un género (existe en grafo_recomendaciones)
            if nodo in grafo_recomendaciones:
                # Exploramos todos los juegos de este género
                for conexion in grafo_recomendaciones[nodo]:
                    if conexion not in visitados:
                        # Creamos nuevo camino añadiendo esta conexión
                        nuevo_camino = camino + [conexion]
                        # Añadimos a la pila con profundidad + 1
                        pila.append((conexion, profundidad + 1, nuevo_camino))
            
            # Si el nodo es un juego (para explorar sus géneros)
            elif nodo in videojuegos:
                # Exploramos todos los géneros de este juego
                for genero in videojuegos[nodo]:
                    if genero not in visitados:
                        # Creamos nuevo camino añadiendo este género
                        nuevo_camino = camino + [genero]
                        # Añadimos a la pila con profundidad + 1
                        pila.append((genero, profundidad + 1, nuevo_camino))
    
    return recomendaciones

# =============================================
# INTERFAZ DE USUARIO
# =============================================
print("🎮 Sistema de Recomendación de Videojuegos 🎮")
print("Juegos disponibles:", ", ".join(videojuegos.keys()))

# Solicitamos al usuario que ingrese un juego
juego_inicio = input("\n¿Qué juego te gustó? (Escribe el nombre exacto): ")

# Verificamos si el juego existe en nuestra base de datos
if juego_inicio in videojuegos:
    print(f"\nBuscando recomendaciones similares a {juego_inicio}...")
    time.sleep(1)  # Pequeña pausa dramática
    
    # Obtenemos las recomendaciones usando DFS
    recomendaciones = dfs_recomendaciones(juego_inicio)
    
    # Mostramos las recomendaciones encontradas
    print("\n🔍 Recomendaciones encontradas (ordenadas por similitud):")
    
    # Iteramos sobre las primeras 5 recomendaciones
    for i, (juego, camino, profundidad) in enumerate(recomendaciones[:5], 1):
        print(f"\n{i}. {juego}")
        print(f"   Conexión: {' → '.join(camino)}")
        print(f"   Nivel de relación: {profundidad} saltos")
        print(f"   Géneros: {', '.join(videojuegos[juego])}")
else:
    print("⚠️ Juego no encontrado. Intenta copiando exactamente el nombre de la lista.")