import time

mazmorra = {
    "entrada": ["sala1", "sala2"],
    "sala1": ["sala3", "sala4"],
    "sala2": ["sala5"],
    "sala3": [],
    "Sala 4": ["Tesoro"],
    "Sala 5": [],
    "Tesoro": []

}

# DFS con límite de profundidad
def dfs_limitado(nodo, objetivo, limite, camino):
    print(f"Explorando: {nodo} (límite: {limite})")
    time.sleep(0.5)  # Efecto visual
    camino.append(nodo)

     if nodo == objetivo:
        return camino
    
    if limite <= 0:
        camino.pop()
        return None

    for vecino in mazmorra.get(nodo, []):
        resultado = dfs_limitado(vecino, objetivo, limite - 1, camino)
        if resultado:
            return resultado
    