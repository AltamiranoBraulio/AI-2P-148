# ---------------------------------------------------------------
# Importamos la librería 'deque' desde el módulo 'collections'
# 'deque' (Double-Ended Queue) es una estructura de datos tipo cola,
# que permite insertar y eliminar elementos por ambos extremos eficientemente.
from collections import deque

# ---------------------------------------------------------------
# Definimos un diccionario llamado 'red_social'
# Cada clave representa a una persona, y su valor es una lista de sus amistades.
# Esta estructura representa una red social como un grafo no dirigido.
red_social = {
    'Tú': ['Ana', 'Juan', 'Luis'],         # 'Tú' conoce a Ana, Juan y Luis
    'Ana': ['Tú', 'Carlos'],               # Ana conoce a 'Tú' y a Carlos
    'Juan': ['Tú', 'Mario'],               # Juan conoce a 'Tú' y a Mario
    'Luis': ['Tú', 'Marta'],               # Luis conoce a 'Tú' y a Marta
    'Carlos': ['Ana', 'Pedro'],            # Carlos conoce a Ana y Pedro
    'Mario': ['Juan'],                     # Mario conoce a Juan
    'Marta': ['Luis', 'Famoso'],           # Marta conoce a Luis y al 'Famoso' 👀
    'Pedro': ['Carlos'],                   # Pedro conoce a Carlos
    'Famoso': ['Marta']                    # El 'Famoso' conoce a Marta
}

# ---------------------------------------------------------------
# Definimos una función llamada 'bfs' (Breadth-First Search)
# Esta función implementa una búsqueda en anchura sobre la red social.
# Parámetros:
# - red: el grafo (diccionario) que representa la red social
# - inicio: nodo desde donde comienza la búsqueda (persona inicial)
# - objetivo: nodo que se desea encontrar (persona objetivo)
def bfs(red, inicio, objetivo):
    """
    Realiza una búsqueda en anchura para encontrar la ruta más corta
    entre 'inicio' y 'objetivo' dentro de la red social dada.
    """

    # 1. Creamos una cola vacía usando 'deque' para manejar los caminos por explorar
    cola = deque()

    # 2. Agregamos el camino inicial, que contiene solo la persona de inicio
    cola.append([inicio])  # Usamos una lista para almacenar la secuencia de personas visitadas

    # 3. Iniciamos un bucle que se ejecuta mientras la cola no esté vacía
    while cola:

        # 4. Sacamos (pop) el primer camino que está en la cola (FIFO)
        camino = cola.popleft()

        # 5. Tomamos la última persona del camino actual (la más reciente agregada)
        persona_actual = camino[-1]

        # 6. Verificamos si esta persona es el objetivo
        if persona_actual == objetivo:
            # Si es así, devolvemos el camino completo como resultado
            return camino

        # 7. Si no es el objetivo, exploramos a sus amigos (nodos adyacentes)
        for amigo in red.get(persona_actual, []):
            # 8. Usamos .get() para evitar errores si la persona no tiene amigos registrados
            # 9. Creamos una copia del camino actual
            nuevo_camino = list(camino)

            # 10. Agregamos al amigo al nuevo camino
            nuevo_camino.append(amigo)

            # 11. Añadimos el nuevo camino a la cola para explorarlo más adelante
            cola.append(nuevo_camino)

    # 12. Si se recorren todos los caminos y no se encuentra el objetivo, devolvemos None
    return None

# ---------------------------------------------------------------
# --- Bloque principal del programa: ejemplo de uso de la función ---

# Definimos el nodo inicial desde donde parte la búsqueda
inicio = 'Tú'

# Definimos el objetivo a encontrar
objetivo = 'Famoso'

# Imprimimos un mensaje indicando que se está realizando la búsqueda
print(f"Buscando conexión entre {inicio} y {objetivo}...")

# Llamamos a la función bfs y guardamos el resultado (el camino encontrado)
camino = bfs(red_social, inicio, objetivo)

# Verificamos si se encontró una ruta válida
if camino:
    # Si se encontró, imprimimos un mensaje de éxito
    print("¡Conexión encontrada! 🎉")
    
    # Mostramos el camino encontrado con flechas indicando la secuencia
    print(" -> ".join(camino))  # Ejemplo de salida: Tú -> Luis -> Marta -> Famoso
else:
    # Si no se encontró, imprimimos un mensaje indicando la falta de conexión
    print("No hay conexión. 😢")
