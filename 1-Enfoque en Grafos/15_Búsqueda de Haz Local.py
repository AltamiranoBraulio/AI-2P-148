import random
import math
import matplotlib.pyplot as plt
import numpy as np

# 🎢 Definimos la función del paisaje, que tiene valles y picos.
def paisaje(x):
    return x**2 + 5 * math.sin(3 * x) + 3 * math.cos(5 * x)
    # Imagina que esto es un terreno montañoso, con picos y valles

# 🎲 Función para mover aleatoriamente un explorador (vecino)
def mover(x):
    return x + random.uniform(-0.5, 0.5)

# 🔦 Función principal de Búsqueda de Haz Local con toque competitivo
def haz_local(k=5, iteraciones=50):
    # Generamos k exploradores con posiciones aleatorias
    exploradores = [random.uniform(-10, 10) for _ in range(k)]
    historial_mejores = []

    # Colores para los exploradores
    colores = plt.cm.jet(np.linspace(0, 1, k))

    print(f"\n🚀 ¡Comienza la carrera de exploradores con {k} agentes! Vamos a buscar el mejor paso...\n")

    # 🎯 Bucle principal para realizar las iteraciones
    for i in range(iteraciones):
        nuevos_exploradores = []
        for j in range(k):
            # Cada explorador genera dos vecinos aleatorios
            vecino1 = mover(exploradores[j])
            vecino2 = mover(exploradores[j])
            nuevos_exploradores.extend([vecino1, vecino2])

        # Seleccionamos los mejores k exploradores en cada iteración
        exploradores = sorted(nuevos_exploradores, key=paisaje)[:k]
        mejor_actual = exploradores[0]
        historial_mejores.append(mejor_actual)

        # Mostramos el progreso de la "competencia"
        print(f"🔁 Iteración {i+1:02}: Mejor x = {mejor_actual:.4f}, Valor = {paisaje(mejor_actual):.4f}")

    # 🎉 Obtenemos el mejor explorador al final
    mejor_final = exploradores[0]
    print(f"\n✅ ¡Mejor explorador! x = {mejor_final:.4f}, Valor = {paisaje(mejor_final):.4f}")
    return historial_mejores, mejor_final, colores

# 🧪 Ejecutamos el algoritmo
historial, mejor, colores = haz_local(k=5, iteraciones=50)

# 📊 Graficamos el paisaje y los caminos de los exploradores

# Generamos una lista de valores x desde -10 hasta 10
x_vals = np.linspace(-10, 10, 400)
y_vals = [paisaje(x) for x in x_vals]

# Graficamos el paisaje
plt.plot(x_vals, y_vals, label="Terreno montañoso")

# Graficamos cada explorador con su color
for idx, color in enumerate(colores):
    plt.plot(historial[idx::5], [paisaje(x) for x in historial[idx::5]], 'o-', label=f"Explorador {idx+1}", color=color)

# Marcamos el mejor punto final
plt.axvline(x=mejor, color='green', linestyle='--', label='¡Mejor paso encontrado!')

# Personalizamos la gráfica
plt.title("🌄 Competencia de Exploradores: Búsqueda de Haz Local")
plt.xlabel("Posición del explorador (x)")
plt.ylabel("Valor de la función (espectacularidad)")
plt.legend()
plt.grid(True)
plt.show()
