from collections import deque

red_social= {
    'Tú': ['Ana', 'Juan', 'Luis'],
    'Ana': ['Tú', 'Carlos'],
    'Juan': ['Tú', 'Mario'],
    'Luis': ['Tú', 'Marta'],
    'Carlos': ['Ana', 'Pedro'],
    'Mario': ['Juan'],
    'Marta': ['Luis', 'Famoso'],  # ¡Marta conoce al famoso!
    'Pedro': ['Carlos'],
    'Famoso': ['Marta']
    }
def bfs(red, inicio, objetivo):
    """
     Búsqueda en Anchura (BFS) simplificada.
    Encuentra la conexión más corta entre dos personas.
    """
    cola = deque()  # 1. Creamos una cola vacía
    cola.append([inicio])  # 2. Añadimos el punto de partida (ej: 'Tú')
    while cola:  # 3. Mientras haya personas en la cola:
        camino = cola.popleft()  # 4. Sacamos el primer camino de la cola
        persona_actual = camino[-1]  # 5. Tomamos la última persona del camino
        
        if persona_actual == objetivo:  # 6. ¡Si es el objetivo, retornamos el camino!
            return camino
         # 7. Si no, exploramos sus amigos:
        for amigo in red.get(persona_actual, []):  # 8. get() evita errores si la persona no existe
            nuevo_camino = list(camino)  # 9. Copiamos el camino actual
            nuevo_camino.append(amigo)  # 10. Añadimos el nuevo amigo
            cola.append(nuevo_camino)  # 11. Agregamos este nuevo camino a la cola
    
    return None  # 12. Si no se encuentra, retornamos None
# --- Ejemplo de uso ---
inicio = 'Tú'
objetivo = 'Famoso'

print(f"Buscando conexión entre {inicio} y {objetivo}...")
camino = bfs(red_social, inicio, objetivo)

if camino:
    print("¡Conexión encontrada! 🎉")
    print(" -> ".join(camino))  # Ej: Tú -> Luis -> Marta -> Famoso
else:
    print("No hay conexión. 😢")