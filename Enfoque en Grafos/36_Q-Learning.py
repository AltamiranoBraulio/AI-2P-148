import random  # Importamos la librería 'random' para decisiones aleatorias en el agente (exploración)

# -----------------------------
# DEFINICIÓN DEL ENTORNO
# -----------------------------

# Lista de estados posibles (nodos del grafo/red)
estados = [0, 1, 2, 3, 4, 5]

# Diccionario de acciones posibles desde cada estado
# Cada clave representa un nodo y su valor es la lista de nodos a los que se puede mover
acciones_posibles = {
    0: [1, 2],    # Desde nodo 0 se puede ir a 1 o 2
    1: [3],       # Desde nodo 1 solo se puede ir a 3
    2: [3, 4],    # Desde 2 se puede ir a 3 o 4
    3: [5],       # Desde 3 a 5 (final)
    4: [5],       # Desde 4 a 5 (final)
    5: []         # Nodo final, sin acciones posibles
}

# Recompensas asociadas a cada transición (acción)
# Algunas transiciones dan energía (recompensa positiva), otras castigan (negativas)
recompensas = {
    (0, 1): -1,   # Ir de 0 a 1 da -1 (zona peligrosa)
    (0, 2): 0,    # Ir de 0 a 2 no da ni quita energía
    (1, 3): 0,    # Ir de 1 a 3 tampoco da recompensa
    (2, 3): 1,    # Ir de 2 a 3 da +1 (energía)
    (2, 4): -2,   # Ir de 2 a 4 da -2 (muy mala ruta)
    (3, 5): 10,   # Ir de 3 a 5 da +10 (el mejor camino)
    (4, 5): 2     # Ir de 4 a 5 da +2 (bueno pero no tanto)
}

# -----------------------------
# PARÁMETROS DEL Q-LEARNING
# -----------------------------

alpha = 0.1      # Tasa de aprendizaje (cuánto nos afecta la nueva info)
gamma = 0.9      # Factor de descuento (valor del futuro)
epsilon = 0.1    # Probabilidad de explorar en vez de explotar
episodios = 5000 # Cuántas veces entrenamos al agente

# -----------------------------
# INICIALIZACIÓN DE Q(s, a)
# -----------------------------

# Creamos una tabla Q vacía (diccionario) para cada par estado-acción
Q = {}
for estado in estados:
    for accion in acciones_posibles.get(estado, []):
        Q[(estado, accion)] = 0.0  # Inicializamos todo en cero

# -----------------------------
# FUNCIÓN DE SELECCIÓN DE ACCIÓN (ε-greedy)
# -----------------------------

# Esta función decide qué acción tomar desde un estado, explorando o explotando
def elegir_accion(estado):
    if random.random() < epsilon:
        # Exploramos: elegimos una acción aleatoria
        return random.choice(acciones_posibles[estado])
    else:
        # Explotamos: elegimos la mejor acción según los valores Q actuales
        acciones = acciones_posibles[estado]
        valores = [Q[(estado, a)] for a in acciones]
        max_valor = max(valores)
        mejores = [a for a in acciones if Q[(estado, a)] == max_valor]
        return random.choice(mejores)  # Rompemos empate aleatoriamente

# -----------------------------
# ENTRENAMIENTO DEL AGENTE
# -----------------------------

for _ in range(episodios):  # Repetimos el entrenamiento varias veces
    estado = 0              # Siempre empezamos en el nodo 0
    while estado != 5:      # Terminamos cuando llegamos al nodo final (estado 5)
        accion = elegir_accion(estado)              # Elegimos una acción desde el estado actual
        siguiente_estado = accion                   # En este caso, la acción es el siguiente estado
        recompensa = recompensas[(estado, accion)]  # Obtenemos la recompensa por esa acción
        
        # Buscamos el mejor Q del siguiente estado para actualizar
        futuros_qs = [Q.get((siguiente_estado, a), 0) for a in acciones_posibles.get(siguiente_estado, [])]
        max_q_siguiente = max(futuros_qs) if futuros_qs else 0  # Si no hay acciones, el Q futuro es 0
        
        # Actualizamos Q usando la fórmula de Q-Learning
        Q[(estado, accion)] += alpha * (recompensa + gamma * max_q_siguiente - Q[(estado, accion)])
        
        # Avanzamos al siguiente estado
        estado = siguiente_estado

# -----------------------------
# MOSTRAR LA POLÍTICA FINAL
# -----------------------------

print("\n--- Política final aprendida ---")
for estado in estados:
    if acciones_posibles.get(estado):  # Solo mostramos estados con acciones posibles
        mejor_accion = max(acciones_posibles[estado], key=lambda a: Q[(estado, a)])  # Escogemos la mejor acción
        print(f"En nodo {estado}, ir a {mejor_accion} (Q: {Q[(estado, mejor_accion)]:.2f})")
