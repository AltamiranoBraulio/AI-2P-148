import random

# --- Variables posibles ---
states = ['Intruso', 'NoIntruso']
alarms = ['Alarma', 'NoAlarma']

# --- Probabilidades iniciales ---
P_Intruso_0 = {'Intruso': 0.1, 'NoIntruso': 0.9}

# --- Probabilidad de transición ---
# P(Intruso_t | Intruso_t-1)
P_transition = {
    'Intruso': {'Intruso': 0.7, 'NoIntruso': 0.3},
    'NoIntruso': {'Intruso': 0.05, 'NoIntruso': 0.95}
}

# --- Probabilidad de observación ---
# P(Alarma_t | Intruso_t)
P_observation = {
    'Intruso': {'Alarma': 0.9, 'NoAlarma': 0.1},
    'NoIntruso': {'Alarma': 0.2, 'NoAlarma': 0.8}  # Falsas alarmas
}

# --- Inicialización ---
def sample_from_distribution(prob_dist):
    r = random.random()
    cumulative = 0.0
    for key, prob in prob_dist.items():
        cumulative += prob
        if r < cumulative:
            return key
    return key  # fallback

# Simulación del sistema durante T pasos de tiempo
def simulate_dynamics(T=10):
    intruso_history = []
    alarma_history = []

    # Estado inicial
    state = sample_from_distribution(P_Intruso_0)

    for t in range(T):
        # Generar observación según estado actual
        observacion = sample_from_distribution(P_observation[state])

        # Guardar historia
        intruso_history.append(state)
        alarma_history.append(observacion)

        print(f"⏱️ t={t} | Estado: {state} | Alarma: {observacion}")

        # Transicionar al siguiente estado
        state = sample_from_distribution(P_transition[state])

    return intruso_history, alarma_history

# Ejecutar simulación
simulate_dynamics(T=15)
