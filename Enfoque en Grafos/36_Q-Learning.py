import random

# Estados: nodos de la red
estados = [0, 1, 2, 3, 4, 5]
acciones_posibles = {
    0: [1, 2],
    1: [3],
    2: [3, 4],
    3: [5],
    4: [5],
    5: []  # Nodo final, fuente de energía
}

# Recompensas (algunas zonas dan energía, otras son zonas de pérdida)
recompensas = {
    (0, 1): -1,
    (0, 2): 0,
    (1, 3): 0,
    (2, 3): 1,
    (2, 4): -2,
    (3, 5): 10,
    (4, 5): 2
}

# Parámetros de Q-learning
alpha = 0.1      # Tasa de aprendizaje
gamma = 0.9      # Descuento futuro
epsilon = 0.1    # Exploración
episodios = 5000

# Inicializar Q(s, a)
Q = {}
for estado in estados:
    for accion in acciones_posibles.get(estado, []):
        Q[(estado, accion)] = 0.0

# Función para elegir acción (ε-greedy)
def elegir_accion(estado):
    if random.random() < epsilon:
        return random.choice(acciones_posibles[estado])
    else:
        acciones = acciones_posibles[estado]
        valores = [Q[(estado, a)] for a in acciones]
        max_valor = max(valores)
        mejores = [a for a in acciones if Q[(estado, a)] == max_valor]
        return random.choice(mejores)

# Entrenamiento
for _ in range(episodios):
    estado = 0
    while estado != 5:
        accion = elegir_accion(estado)
        siguiente_estado = accion
        recompensa = recompensas[(estado, accion)]
        futuros_qs = [Q.get((siguiente_estado, a), 0) for a in acciones_posibles.get(siguiente_estado, [])]
        max_q_siguiente = max(futuros_qs) if futuros_qs else 0
        Q[(estado, accion)] += alpha * (recompensa + gamma * max_q_siguiente - Q[(estado, accion)])
        estado = siguiente_estado

# Mostrar la mejor política aprendida
print("\n--- Política final aprendida ---")
for estado in estados:
    if acciones_posibles.get(estado):
        mejor_accion = max(acciones_posibles[estado], key=lambda a: Q[(estado, a)])
        print(f"En nodo {estado}, ir a {mejor_accion} (Q: {Q[(estado, mejor_accion)]:.2f})")
