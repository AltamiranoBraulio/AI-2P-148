import random

# --- Definición del mundo ---
states = ['Bosque', 'Playa', 'Montaña', 'Cueva', 'Tesoro']
actions = ['Norte', 'Sur', 'Este', 'Oeste']
observations = ['Olor a sal', 'Ecos', 'Sombra', 'Aroma dulce', 'Silencio']

# Modelo de transición simple: moverse aleatoriamente
def transition(state, action):
    probs = {
        'Bosque': {'Norte': 'Montaña', 'Sur': 'Playa', 'Este': 'Cueva', 'Oeste': 'Bosque'},
        'Playa': {'Norte': 'Bosque', 'Sur': 'Playa', 'Este': 'Playa', 'Oeste': 'Playa'},
        'Montaña': {'Norte': 'Montaña', 'Sur': 'Bosque', 'Este': 'Montaña', 'Oeste': 'Montaña'},
        'Cueva': {'Norte': 'Cueva', 'Sur': 'Tesoro', 'Este': 'Cueva', 'Oeste': 'Bosque'},
        'Tesoro': {'Norte': 'Tesoro', 'Sur': 'Tesoro', 'Este': 'Tesoro', 'Oeste': 'Tesoro'}
    }
    return probs[state].get(action, state)

# Modelo de observación: probabilidades de lo que se percibe en cada estado
observation_model = {
    'Bosque': ['Sombra', 'Silencio'],
    'Playa': ['Olor a sal', 'Silencio'],
    'Montaña': ['Ecos', 'Sombra'],
    'Cueva': ['Ecos', 'Aroma dulce'],
    'Tesoro': ['Aroma dulce', 'Silencio']
}

# Función de recompensa
def reward(state):
    if state == 'Tesoro':
        return 100
    else:
        return -1

# Inicialización: creencia uniforme
belief = {state: 1/len(states) for state in states}

# Función para actualizar la creencia basada en la observación
def update_belief(belief, observation):
    new_belief = {}
    for state in states:
        if observation in observation_model[state]:
            new_belief[state] = belief[state] * 0.9  # Alta probabilidad si la observación es típica
        else:
            new_belief[state] = belief[state] * 0.1  # Baja probabilidad si no es típica
    # Normalizar
    total = sum(new_belief.values())
    for state in new_belief:
        new_belief[state] /= total
    return new_belief

# Función para elegir la acción basada en la creencia
def choose_action(belief):
    # Simplemente ir hacia el lugar que creemos más probable que tenga el Tesoro
    best_state = max(belief, key=belief.get)
    if best_state == 'Cueva':
        return 'Sur'
    elif best_state == 'Bosque':
        return random.choice(['Este', 'Sur'])
    elif best_state == 'Montaña':
        return 'Sur'
    elif best_state == 'Playa':
        return 'Norte'
    else:
        return random.choice(actions)

# Simulación principal
current_state = random.choice(states)
print(f"🌍 Estado inicial oculto: {current_state}")

for step in range(10):
    obs = random.choice(observation_model[current_state])
    print(f"\n👀 Observación recibida: {obs}")
    belief = update_belief(belief, obs)
    print(f"🤔 Creencia actualizada: {belief}")
    action = choose_action(belief)
    print(f"➡️ Acción elegida: {action}")
    current_state = transition(current_state, action)
    print(f"🌍 Nuevo estado oculto: {current_state}")
    if current_state == 'Tesoro':
        print("🏆 ¡Tesoro encontrado!")
        break
