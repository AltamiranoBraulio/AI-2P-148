from collections import deque

def recomendar_amigos(grafo_red, usuario_actual, niveles=3):
    """
    Encuentra posibles amigos a través de conexiones existentes
    usando BFS en grafos con límite de profundidad
    """
    recomendaciones = {i: set() for i in range(1, niveles+1)}
    visitados = set([usuario_actual])
    cola = deque([(usuario_actual, 0)])
    
    while cola:
        usuario, nivel_actual = cola.popleft()
        
        for amigo in grafo_red.get(usuario, []):
            if amigo not in visitados:
                visitados.add(amigo)
                if 1 <= nivel_actual + 1 <= niveles:
                    recomendaciones[nivel_actual + 1].add(amigo)
                cola.append((amigo, nivel_actual + 1))
    
    return {k: list(v) for k, v in recomendaciones.items() if v}

# Red social corregida (observa los cierres de llaves)
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
}  # <-- Aquí estaba el error: faltaba esta llave de cierre

recomendaciones = recomendar_amigos(red_social, "Ana", 3)

print("💡 Recomendaciones de amigos para Ana:")
for grado, amigos in recomendaciones.items():
    print(f"Amigos a {grado}° de conexión: {', '.join(amigos)}")