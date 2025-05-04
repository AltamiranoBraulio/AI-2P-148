import random

# Definimos las cuevas
cuevas = [0, 1, 2, 3, 4, 5]  # Estados
acciones_posibles = {
    0: [1, 2],
    1: [3],
    2: [3, 4],
    3: [5],
    4: [5],
    5: []  # Meta
}

# Recompensas escondidas
recompensas = {
    (0, 1): 0,
    (0, 2): 1,
    (1, 3): 1,
    (2, 3): 2,
    (2, 4): -1,
    (3, 5): 10,
    (4, 5): 5
}

# Parámetros de aprendizaje
epsilon = 0.2  # Probabilidad de explorar
gamma = 0.9    # Factor de descuento
alpha = 0.1    # Tasa de aprendizaje
episodios = 5000

# Inicialización de Q(s, a)
Q = {}
for estado in cuevas:
    for accion in acciones_posibles.get(estado, []):
        Q[(estado, accion)] = 0.0

# Función para seleccionar acción ε-greedy
def seleccionar_accion(estado):
    if random.random() < epsilon:
        return random.choice(acciones_posibles[estado])
    else:
        qs = [(accion, Q[(estado, accion)]) for accion in acciones_posibles[estado]]
        max_q = max(qs, key=lambda x: x[1])[1]
        mejores_acciones = [accion for accion, q in qs if q == max_q]
        return random.choice(mejores_acciones)

# Entrenamiento
for ep in range(episodios):
    estado = 0  # Siempre comenzamos en la entrada
    while estado != 5:  # Mientras no lleguemos al final
        accion = seleccionar_accion(estado)
        nueva_cueva = accion  # Acción indica a qué cueva ir
        recompensa = recompensas[(estado, nueva_cueva)]
        
        # Actualización Q-learning
        futuros_qs = [Q[(nueva_cueva, a)] for a in acciones_posibles.get(nueva_cueva, [])] or [0]
        mejor_futuro = max(futuros_qs)
        
        Q[(estado, accion)] += alpha * (recompensa + gamma * mejor_futuro - Q[(estado, accion)])
        
        estado = nueva_cueva

# Mostrar resultados
print("\n--- Política aprendida ---")
for estado in cuevas[:-1]:  # No incluimos el estado final
    acciones = acciones_posibles[estado]
    if acciones:
        mejor_accion = max(acciones, key=lambda a: Q[(estado, a)])
        print(f"En cueva {estado}, ir a cueva {mejor_accion} (valor estimado: {Q[(estado, mejor_accion)]:.2f})")

