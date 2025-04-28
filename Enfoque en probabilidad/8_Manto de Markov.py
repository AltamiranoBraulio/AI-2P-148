import random

# Definimos los estados financieros del jugador
estados = ["Rico", "Moderado", "Pobre"]

# Definimos la matriz de transición entre los estados
# Cada fila es un estado, y cada columna es la probabilidad de ir a otro estado
# Ejemplo: "Rico" -> [Probabilidad de estar en "Rico", "Moderado", "Pobre"]
matriz_transiciones = [
    [0.5, 0.3, 0.2],  # Rico -> [Rico, Moderado, Pobre]
    [0.2, 0.6, 0.2],  # Moderado -> [Rico, Moderado, Pobre]
    [0.1, 0.4, 0.5]   # Pobre -> [Rico, Moderado, Pobre]
]

# Definimos el estado inicial del jugador
estado_inicial = "Moderado"

# Función para determinar el siguiente estado basado en la matriz de transición
def siguiente_estado(estado_actual):
    # Obtener el índice del estado actual
    estado_idx = estados.index(estado_actual)
    
    # Obtener las probabilidades de transición
    probabilidades = matriz_transiciones[estado_idx]
    
    # Elegir el siguiente estado basándose en las probabilidades
    siguiente = random.choices(estados, probabilidades)[0]
    return siguiente

# Simulamos 10 rondas de apuestas
estado_actual = estado_inicial
rondas = 10

print(f"Estado inicial: {estado_actual}")
for ronda in range(1, rondas + 1):
    # Determinamos el siguiente estado
    estado_actual = siguiente_estado(estado_actual)
    print(f"Ronda {ronda}: El jugador está {estado_actual}")
