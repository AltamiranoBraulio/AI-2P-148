import numpy as np
import matplotlib.pyplot as plt

# Mapa de la mazmorra
dungeon_map = [
    ['S', 'S', 'S', 'G'],
    ['S', '#', 'S', 'T'],
    ['S', 'S', 'S', 'S'],
    ['T', '#', 'S', 'S']
]

# Parámetros
rows, cols = len(dungeon_map), len(dungeon_map[0])
gamma = 0.9
threshold = 0.001
reward_dict = {'S': -0.04, 'G': 10, 'T': -10, '#': 0}

# Inicialización de valores
V = np.zeros((rows, cols))
policy = np.full((rows, cols), ' ')
directions = {
    '↑': (-1, 0),
    '↓': (1, 0),
    '←': (0, -1),
    '→': (0, 1)
}

def is_valid(i, j):
    return 0 <= i < rows and 0 <= j < cols and dungeon_map[i][j] != '#'

def one_step(i, j, di, dj):
    ni, nj = i + di, j + dj
    return (ni, nj) if is_valid(ni, nj) else (i, j)

def value_iteration():
    iteration = 0
    while True:
        delta = 0
        new_V = V.copy()
        for i in range(rows):
            for j in range(cols):
                tile = dungeon_map[i][j]
                if tile in ['#', 'G', 'T']:
                    continue

                values = []
                for a, (di, dj) in directions.items():
                    ni, nj = one_step(i, j, di, dj)
                    r = reward_dict[dungeon_map[ni][nj]]
                    values.append((r + gamma * V[ni][nj], a))

                max_val, best_action = max(values)
                new_V[i][j] = max_val
                policy[i][j] = best_action
                delta = max(delta, abs(V[i][j] - new_V[i][j]))

        V[:, :] = new_V
        iteration += 1
        if delta < threshold:
            break

value_iteration()

# Visualización
def display():
    fig, ax = plt.subplots()
    for i in range(rows):
        for j in range(cols):
            tile = dungeon_map[i][j]
            v = V[i][j]
            ax.add_patch(plt.Rectangle((j, rows-i-1), 1, 1, fill=True,
                         color='lightgrey' if tile == 'S' else
                               'black' if tile == '#' else
                               'gold' if tile == 'G' else
                               'red'))

            if tile == 'S':
                ax.text(j+0.5, rows-i-1+0.5, f"{v:.1f}\n{policy[i][j]}",
                        ha='center', va='center', fontsize=8)

            elif tile == 'G':
                ax.text(j+0.5, rows-i-1+0.5, "G", ha='center', va='center', fontsize=14, color='black')
            elif tile == 'T':
                ax.text(j+0.5, rows-i-1+0.5, "☠", ha='center', va='center', fontsize=14, color='white')

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.gca().invert_yaxis()
    plt.title("Política Óptima con Iteración de Valores")
    plt.show()

display()
