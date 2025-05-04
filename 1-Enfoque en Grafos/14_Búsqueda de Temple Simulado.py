# 📚 Importamos las librerías necesarias

import random  # Para generar números aleatorios (pasos del robot, probabilidades)
import math    # Para funciones matemáticas como sin(), cos(), exp(), etc.
import matplotlib.pyplot as plt  # Para graficar el escenario y los pasos del robot

# 🎭 Definimos la función que queremos minimizar (el escenario del show)
# Esta función tiene muchos picos y valles, como un paisaje montañoso
def espectacularidad(x):
    return x**2 + 5 * math.sin(3*x) + 3 * math.cos(5*x)
    # x**2: una parábola
    # sin(3x): agrega ondas grandes
    # cos(5x): agrega ondas pequeñas

# 🎲 Movimiento aleatorio del robot (vecino)
def mover_robot(x):
    return x + random.uniform(-0.5, 0.5)
    # El robot da un paso aleatorio entre -0.5 y 0.5 desde su posición actual

# 🔥 Algoritmo principal de Temple Simulado
def buscar_mejor_paso():
    temperatura = 100             # Temperatura inicial alta (más libertad)
    enfriamiento = 0.95           # Factor para ir bajando la temperatura
    minimo_temp = 0.1             # Temperatura mínima para detenerse

    x = random.uniform(-10, 10)   # Posición inicial aleatoria del robot
    mejor_x = x                   # Registramos esta como la mejor posición inicial
    mejor_espectaculo = espectacularidad(x)  # Evaluamos la función en esa posición

    historial = [x]               # Guardamos todos los pasos del robot

    print("🕺 Buscando la mejor pose del robot bailarín...")

    # 🔁 Bucle principal del algoritmo
    while temperatura > minimo_temp:
        nuevo_x = mover_robot(x)                     # Proponemos una nueva posición
        actual = espectacularidad(x)                 # Valor actual de la función
        nuevo = espectacularidad(nuevo_x)            # Valor en la nueva posición

        delta = nuevo - actual  # Cambio en la "espectacularidad"

        # ¿Aceptamos el nuevo paso?
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            x = nuevo_x                              # Aceptamos el paso
            historial.append(x)                      # Lo agregamos al historial

            if nuevo < mejor_espectaculo:            # Si es el mejor paso hasta ahora
                mejor_x = nuevo_x
                mejor_espectaculo = nuevo

        temperatura *= enfriamiento  # Bajamos la temperatura

    print(f"\n🎉 ¡Mejor paso encontrado en x = {mejor_x:.2f} con espectáculo = {mejor_espectaculo:.2f}")
    return historial, mejor_x

# 🧪 Ejecutamos el algoritmo
historial, mejor = buscar_mejor_paso()

# 📊 Visualizamos el escenario y el camino del robot

# Creamos una lista de valores x desde -10 hasta 10
x_vals = [i * 0.1 for i in range(-100, 100)]
# Calculamos la función en cada punto x
y_vals = [espectacularidad(x) for x in x_vals]

# Dibujamos la curva del escenario
plt.plot(x_vals, y_vals, label="Escenario del show")

# Dibujamos los pasos del robot con puntos rojos
plt.plot(historial, [espectacularidad(x) for x in historial], 'ro-', label="Pasos del robot")

# Línea vertical donde se encontró el mejor paso
plt.axvline(x=mejor, color='green', linestyle='--', label='¡Paso perfecto!')

# Personalizamos la gráfica
plt.title("🤖 Temple Simulado: El robot busca su mejor paso")
plt.xlabel("Posición del robot")
plt.ylabel("Espectacularidad")
plt.legend()
plt.grid(True)
plt.show()
