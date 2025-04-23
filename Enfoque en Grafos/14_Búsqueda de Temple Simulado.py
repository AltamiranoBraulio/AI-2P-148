import random
import math
import matplotlib.pyplot as plt

def espectacularidad(x):
    return x**2 + 5 * math.sin(3*x) + 3 * math.cos(5*x)
def mover_robot(x):
    return x + random.uniform(-0.5, 0.5)
def buscar_mejor_paso():
    temperatura = 100
    enfriamiento = 0.95
    minimo_temp = 0.1
x = random.uniform(-10, 10)
    mejor_x = x
    mejor_espectaculo = espectacularidad(x)

    historial = [x]

print("🕺 Buscando la mejor pose del robot bailarín...")

    while temperatura > minimo_temp:
        nuevo_x = mover_robot(x)
        actual = espectacularidad(x)
        nuevo = espectacularidad(nuevo_x)

        delta = nuevo - actual

        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            x = nuevo_x
            historial.append(x)

            if nuevo < mejor_espectaculo:
                mejor_x = nuevo_x
                mejor_espectaculo = nuevo

        temperatura *= enfriamiento
print(f"\n🎉 ¡Mejor paso encontrado en x = {mejor_x:.2f} con espectáculo = {mejor_espectaculo:.2f}")
    return historial, mejor_x

# 🧪 Ejecutamos
historial, mejor = buscar_mejor_paso()

# 📊 Visualización
x_vals = [i * 0.1 for i in range(-100, 100)]
y_vals = [espectacularidad(x) for x in x_vals]

plt.plot(x_vals, y_vals, label="Escenario del show")
plt.plot(historial, [espectacularidad(x) for x in historial], 'ro-', label="Pasos del robot")
plt.axvline(x=mejor, color='green', linestyle='--', label='¡Paso perfecto!')
plt.title("🤖 Temple Simulado: El robot busca su mejor paso")
plt.xlabel("Posición del robot")
plt.ylabel("Espectacularidad")
plt.legend()
plt.grid(True)
plt.show()