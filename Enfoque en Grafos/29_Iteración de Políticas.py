import numpy as np

# Prisión con emojis
prison_map = [
    ['❓', '❓', '❓', '🚪'],
    ['❓', '🧱', '❓', '🔥'],
    ['❓', '❓', '❓', '❓'],
    ['🔥', '🧱', '❓', '❓']
]

reward_dict = {'❓': -0.04, '🚪': 10, '🔥': -10, '🧱': 0}
emoji_policy = {'↑': '🔼', '↓': '🔽', '←': '◀️', '→': '▶️'}
gamma = 0.9
rows, cols = len(prison_map), len(prison_map[0])

V = np.zeros((rows, cols))
policy = np.random.choice(list(emoji_policy.keys()), size=(rows, cols))

moves = {
    '↑': (-1, 0),
    '↓': (1, 0),
    '←': (0, -1),
    '→': (0, 1)
}

def is_valid(i, j):
    return 0 <= i < rows and 0 <= j < cols and prison_map[i][j] != '🧱'

def move(i, j, di, dj):
    ni, nj = i + di, j + dj
    return (ni, nj) if is_valid(ni, nj) else (i, j)

def policy_evaluation():
    while True:
        delta = 0
        new_V = V.copy()
        for i in range(rows):
            for j in range(cols):
                tile = prison_map[i][j]
                if tile in ['🧱', '🚪', '🔥']:
                    continue
                action = policy[i][j]
                di, dj = moves[action]
                ni, nj = move(i, j, di, dj)
                r = reward_dict[prison_map[ni][nj]]
                val = r + gamma * V[ni][nj]
                delta = max(delta, abs(val - V[i][j]))
                new_V[i][j] = val
        V[:, :] = new_V
        if delta < 0.001:
            break

def policy_improvement():
    stable = True
    for i in range(rows):
        for j in range(cols):
            if prison_map[i][j] in ['🧱', '🚪', '🔥']:
                continue
            best_action = None
            best_value = -float('inf')
            for a, (di, dj) in moves.items():
                ni, nj = move(i, j, di, dj)
                r = reward_dict[prison_map[ni][nj]]
                val = r + gamma * V[ni][nj]
                if val > best_value:
                    best_value = val
                    best_action = a
            if policy[i][j] != best_action:
                stable = False
            policy[i][j] = best_action
    return stable

def policy_iteration():
    while True:
        policy_evaluation()
        if policy_improvement():
            break

def print_policy():
    print("🏃 POLÍTICA FINAL PARA ESCAPAR DE LA PRISIÓN:")
    for i in range(rows):
        row = ''
        for j in range(cols):
            tile = prison_map[i][j]
            if tile == '❓':
                row += emoji_policy[policy[i][j]] + ' '
            else:
                row += tile + ' '
        print(row)

policy_iteration()
print_policy()
