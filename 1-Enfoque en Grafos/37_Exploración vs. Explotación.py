import random
import numpy as np

# Parámetros del entorno
size = 5  # Tamaño de la cuadrícula (5x5)
meta = (4, 4)  # Meta en la esquina inferior derecha

# Recompensas en cada celda (penalizaciones y bonificaciones)
recompensas = np.random.uniform(-1, 1, (size, size))
recompensas[meta] = 10  # Recompensa alta en la meta

# Parámetros de Q-learning
alpha = 0.1    # Tasa de aprendizaje
gamma = 0.9    # Factor de descuento
epsilon = 0.1  # Probabilidad de exploración
episodios = 1000

# Inicialización de Q(s, a)
Q = {}
acciones = ['arriba', 'abajo', 'izquierda', 'derecha']

# Función para elegir acción (ε-greedy)
def elegir_accion(estado):
    if random.random() < epsilon:  # Exploración
        return random.choice(acciones)
    else:  # Explotación
        # Elegir la acción con el mayor valor Q
        valores_q = [Q.get((estado, accion), 0) for accion in acciones]
        max_q = max(valores_q)
        mejores_acciones = [acciones[i] for i, q in enumerate(valores_q) if q == max_q]
        return random.choice(mejores_acciones)

# Función para mover en la cuadrícula
def mover(estado, accion):
    x, y = estado
    if accion == 'arriba' and x > 0:
        return (x - 1, y)
    elif accion == 'abajo' and x < size - 1:
        return (x + 1, y)
    elif accion == 'izquierda' and y > 0:
        return (x, y - 1)
    elif accion == 'derecha' and y < size - 1:
        return (x, y + 1)
    return estado  # Si se sale del borde, el agente permanece en el mismo estado

# Q-learning
for episodio in range(episodios):
    estado = (0, 0)  # El agente empieza en la esquina superior izquierda
    while estado != meta:
        accion = elegir_accion(estado)
        siguiente_estado = mover(estado, accion)
        recompensa = recompensas[siguiente_estado]
        futuros_qs = [Q.get((siguiente_estado, a), 0) for a in acciones]
        max_q_siguiente = max(futuros_qs) if futuros_qs else 0
        Q[(estado, accion)] = Q.get((estado, accion), 0) + alpha * (recompensa + gamma * max_q_siguiente - Q.get((estado, accion), 0))
        estado = siguiente_estado

# Mostrar la política aprendida
print("\n--- Política final aprendida ---")
for i in range(size):
    for j in range(size):
        estado = (i, j)
        if estado == meta:
            print(f"En {estado}, META")
        else:
            # Obtener la acción recomendada
            valores_q = [Q.get((estado, a), 0) for a in acciones]
            max_q = max(valores_q)
            index = valores_q.index(max_q)
            mejor_accion = acciones[index]
            print(f"En {estado}, {mejor_accion} (Q: {max_q:.2f})")

# Opcional: graficar la cuadrícula de recompensas
import matplotlib.pyplot as plt

plt.imshow(recompensas, cmap='coolwarm', origin='lower')
plt.colorbar(label='Recompensa')
plt.title("Mapa de Recompensas del Entorno")
plt.show()
