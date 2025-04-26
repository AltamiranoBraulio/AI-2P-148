import random

# Configuración del restaurante
mesas = [0, 1, 2, 3, 4]
propinas = {
    0: 0.1,
    1: 0.5,
    2: -0.2,
    3: 1.0,
    4: 2.0
}

# Política fija
policy = {m: m+1 for m in mesas[:-1]}
policy[4] = None

gamma = 0.9
episodes = 3000

# Inicialización de valores
values = {m: 0 for m in mesas}
returns = {m: [] for m in mesas}

# Funciones
def generate_episode():
    episode = []
    mesa_actual = 0
    while mesa_actual is not None:
        reward = propinas[mesa_actual]
        episode.append((mesa_actual, reward))
        mesa_actual = policy[mesa_actual]
    return episode

# Aprendizaje pasivo
for ep in range(episodes):
    episode = generate_episode()
    
    G = 0
    for idx in reversed(range(len(episode))):
        mesa, reward = episode[idx]
        G = reward + gamma * G
        returns[mesa].append(G)
        values[mesa] = sum(returns[mesa]) / len(returns[mesa])

# Resultados
print("\n--- Valores aprendidos de cada mesa ---")
for mesa in mesas:
    print(f"Mesa {mesa}: Valor estimado = {values[mesa]:.2f}")
