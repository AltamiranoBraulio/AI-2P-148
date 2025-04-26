import numpy as np
import random

# Configuración del mapa
island = [
    ['🍌', '❓', '🛖', '❓', '🚁'],
    ['❓', '🕳️', '❓', '🕳️', '❓'],
    ['❓', '❓', '🍌', '❓', '❓']
]

reward_map = {
    '❓': -0.04,
    '🍌': 1,
    '🛖': 2,
    '🚁': 10,
    '🕳️': -10
}

rows, cols = len(island), len(island[0])
states = [(i, j) for i in range(rows) for j in range(cols) if island[i][j] != '🕳️']
actions = ['↑', '↓', '←', '→']
gamma = 0.9
theta = 0.01

# Probabilidad de transición (80% directo, 10% a cada lado perpendicular)
transition_probs = {
    '↑': [('↑', 0.8), ('←', 0.1), ('→', 0.1)],
    '↓': [('↓', 0.8), ('←', 0.1), ('→', 0.1)],
    '←': [('←', 0.8), ('↑', 0.1), ('↓', 0.1)],
    '→': [('→', 0.8), ('↑', 0.1), ('↓', 0.1)]
}

move_delta = {
    '↑': (-1, 0),
    '↓': (1, 0),
    '←': (0, -1),
    '→': (0, 1)
}

V = np.zeros((rows, cols))

def is_valid(i, j):
    return 0 <= i < rows and 0 <= j < cols and island[i][j] != '🕳️'

def move(i, j, action):
    di, dj = move_delta[action]
    ni, nj = i + di, j + dj
    return (ni, nj) if is_valid(ni, nj) else (i, j)

def value_iteration():
    while True:
        delta = 0
        new_V = V.copy()
        for i, j in states:
            max_val = float('-inf')
            for a in actions:
                val = 0
                for dir, prob in transition_probs[a]:
                    ni, nj = move(i, j, dir)
                    reward = reward_map[island[ni][nj]]
                    val += prob * (reward + gamma * V[ni][nj])
                max_val = max(max_val, val)
            delta = max(delta, abs(max_val - V[i][j]))
            new_V[i][j] = max_val
        V[:, :] = new_V
        if delta < theta:
            break

def extract_policy():
    policy = [['⬛' for _ in range(cols)] for _ in range(rows)]
    for i, j in states:
        best_action = None
        best_value = float('-inf')
        for a in actions:
            val = 0
            for dir, prob in transition_probs[a]:
                ni, nj = move(i, j, dir)
                reward = reward_map[island[ni][nj]]
                val += prob * (reward + gamma * V[ni][nj])
            if val > best_value:
                best_value = val
                best_action = a
        policy[i][j] = {'↑': '🔼', '↓': '🔽', '←': '◀️', '→': '▶️'}[best_action]
    return policy

def print_policy(policy):
    print("\n🧭 POLÍTICA ÓPTIMA PARA SOBREVIVIR EN LA ISLA:")
    for i in range(rows):
        row = ''
        for j in range(cols):
            if island[i][j] == '🕳️':
                row += '🕳️ '
            elif island[i][j] == '🚁':
                row += '🚁 '
            else:
                row += policy[i][j] + ' '
        print(row)

value_iteration()
final_policy = extract_policy()
print_policy(final_policy)
