import random
import matplotlib.pyplot as plt

# --- Definimos nuestro "universo" de planetas y probabilidades de transición --- #

# Lista de planetas
planetas = ['Tierra', 'Marte', 'Júpiter', 'Saturno', 'Neptuno']

# Matriz de transición (fila: planeta actual, columna: planeta destino)
# Cada fila suma aproximadamente 1.0
transiciones = {
    'Tierra': {'Tierra': 0.1, 'Marte': 0.6, 'Júpiter': 0.2, 'Saturno': 0.05, 'Neptuno': 0.05},
    'Marte': {'Tierra': 0.2, 'Marte': 0.2, 'Júpiter': 0.4, 'Saturno': 0.1, 'Neptuno': 0.1},
    'Júpiter': {'Tierra': 0.1, 'Marte': 0.2, 'Júpiter': 0.4, 'Saturno': 0.2, 'Neptuno': 0.1},
    'Saturno': {'Tierra': 0.1, 'Marte': 0.1, 'Júpiter': 0.4, 'Saturno': 0.3, 'Neptuno': 0.1},
    'Neptuno': {'Tierra': 0.05, 'Marte': 0.05, 'Júpiter': 0.1, 'Saturno': 0.3, 'Neptuno': 0.5},
}

# --- Función para realizar un salto basado en la matriz de transición --- #
def siguiente_planeta(actual):
    """
    Dado un planeta actual, selecciona el siguiente planeta basándose en las probabilidades de transición.
    """
    destinos = list(transiciones[actual].keys())
    probabilidades = list(transiciones[actual].values())
    return random.choices(destinos, weights=probabilidades, k=1)[0]

# --- Función principal para simular el recorrido --- #
def simular_exploracion(inicio, pasos):
    """
    Simula el recorrido de un explorador saltando entre planetas usando Monte Carlo en Cadenas de Markov.
    """
    recorrido = [inicio]
    actual = inicio

    for _ in range(pasos):
        proximo = siguiente_planeta(actual)  # Saltamos al siguiente planeta
        recorrido.append(proximo)
        actual = proximo

    return recorrido

# --- Parámetros de simulación --- #
inicio = 'Tierra'  # Empezamos en la Tierra
pasos = 500        # Número de saltos

# --- Ejecutamos la simulación --- #
recorrido = simular_exploracion(inicio, pasos)

# --- Analizamos cuántas veces se visitó cada planeta --- #
frecuencia = {planeta: recorrido.count(planeta) for planeta in planetas}

# --- Mostramos resultados --- #
print("🪐 Frecuencia de visitas a cada planeta:\n")
for planeta, veces in frecuencia.items():
    print(f"{planeta}: {veces} veces")

# --- Visualizamos los resultados --- #
plt.bar(frecuencia.keys(), frecuencia.values(), color='skyblue')
plt.title('Frecuencia de Visitas a Planetas (MCMC)')
plt.xlabel('Planeta')
plt.ylabel('Número de visitas')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
