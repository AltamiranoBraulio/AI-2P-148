# Importamos deque desde collections, que es una estructura de datos tipo cola eficiente
from collections import deque

# Función que recomienda amigos usando una búsqueda en anchura (BFS) hasta cierto nivel
def recomendar_amigos(grafo_red, usuario_actual, niveles=3):
    # Creamos un diccionario donde cada clave será un nivel de conexión y su valor un conjunto de amigos
    recomendaciones = {i: set() for i in range(1, niveles+1)}

    # Conjunto para marcar qué usuarios ya hemos visitado, empezando con el usuario actual
    visitados = set([usuario_actual])

    # Cola para la búsqueda en anchura, que contiene tuplas (usuario, nivel)
    cola = deque([(usuario_actual, 0)])

    # Ejecutamos BFS
    while cola:
        # Extraemos un usuario y su nivel actual
        usuario, nivel_actual = cola.popleft()

        # Recorremos los amigos del usuario actual
        for amigo in grafo_red.get(usuario, []):
            # Si no lo hemos visitado antes
            if amigo not in visitados:
                # Marcamos como visitado
                visitados.add(amigo)

                # Si el siguiente nivel está dentro del rango permitido
                if 1 <= nivel_actual + 1 <= niveles:
                    # Lo añadimos al conjunto de recomendaciones del nivel adecuado
                    recomendaciones[nivel_actual + 1].add(amigo)

                # Añadimos al amigo a la cola con el nuevo nivel
                cola.append((amigo, nivel_actual + 1))

    # Convertimos los sets a listas y eliminamos los niveles sin recomendaciones
    return {k: list(v) for k, v in recomendaciones.items() if v}


# Grafo de ejemplo representando la red social
red_social = {
    "Ana": ["Carlos", "Beatriz", "David"],
    "Carlos": ["Ana", "Emilio"],
    "Beatriz": ["Ana", "Fernanda"],
    "David": ["Ana", "Carlos", "Gabriela"],
    "Emilio": ["Carlos", "Héctor"],
    "Fernanda": ["Beatriz", "Isabel"],
    "Gabriela": ["David"],
    "Héctor": ["Emilio"],
    "Isabel": ["Fernanda", "Juan"],
    "Juan": ["Isabel"]
}

# Llamamos a la función para obtener recomendaciones para "Ana" hasta 3 niveles
recomendaciones = recomendar_amigos(red_social, "Ana", 3)

# Imprimimos los resultados de manera ordenada
print("💡 Recomendaciones de amigos para Ana:")
if recomendaciones:
    for grado, amigos in recomendaciones.items():
        print(f"Amigos a {grado}° de conexión: {', '.join(amigos)}")
else:
    print("No hay recomendaciones disponibles.")
