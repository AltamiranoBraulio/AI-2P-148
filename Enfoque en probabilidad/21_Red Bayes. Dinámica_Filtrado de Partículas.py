import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 🐉 Escenario: El Dragón en el Bosque Mágico
# -----------------------------
# Número de partículas (representan posibles ubicaciones del dragón)
num_particulas = 1000

# Número de pasos de tiempo (simulamos 50 pasos de vuelo)
num_pasos = 50

# Inicialización de la ubicación y energía del dragón
posicion_latente = np.zeros(num_pasos)  # Posiciones latentes del dragón
energia_latente = np.zeros(num_pasos)  # Energía real del dragón

# Mediciones ruidosas (lo que "vemos" del dragón)
posicion_observada = np.zeros(num_pasos)
energia_observada = np.zeros(num_pasos)

# Simulamos el vuelo del dragón (latentes)
for t in range(1, num_pasos):
    # El dragón vuela, y su posición cambia con ruido del entorno
    posicion_latente[t] = posicion_latente[t-1] + np.random.normal(0, 2)  # Ruido de vuelo
    energia_latente[t] = energia_latente[t-1] - np.random.normal(0, 0.5)  # Ruido de energía

    # Mediciones ruidosas (sensor místico que mide la posición y energía)
    posicion_observada[t] = posicion_latente[t] + np.random.normal(0, 3)  # Ruido de medición
    energia_observada[t] = energia_latente[t] + np.random.normal(0, 1)  # Ruido de medición

# -----------------------------
# 🌲 Inicialización del Filtrado de Partículas (Dragón)
# -----------------------------
# Inicializamos las partículas con posiciones y energías aleatorias
particulas_posicion = np.random.normal(0, 10, num_particulas)  # Posición inicial aleatoria
particulas_energia = np.random.normal(100, 50, num_particulas)  # Energía inicial aleatoria

# -----------------------------
# 🧙‍♂️ Función de Actualización del Dragón (Vuelo Mágico)
# -----------------------------
# Actualiza las partículas basándose en un vuelo aleatorio del dragón
def actualizar_particulas(particulas, ruido, delta=0.1):
    # El 'delta' es el cambio en la posición o energía
    return particulas + delta + np.random.normal(0, ruido, num_particulas)  # Agrega ruido al vuelo

# -----------------------------
# 🔮 Función de Reponderación (Medición Mágica)
# -----------------------------
# Reponderamos las partículas según las mediciones mágicas (ruidosas)
def reponderar_particulas(particulas, medicion, sigma):
    # Calculamos las distancias entre las partículas y la medición observada
    distancias = np.abs(particulas - medicion)
    # Calculamos los pesos basados en la probabilidad de estar cerca de la medición
    pesos = np.exp(-distancias**2 / (2 * sigma**2))  # Probabilidad de la distancia
    # Normalizamos los pesos para que sumen 1
    pesos /= np.sum(pesos)  
    return pesos

# -----------------------------
# 🔮 Función de Re-muestreo (Reemplace a las Partículas)
# -----------------------------
# Re-muestreamos las partículas según los pesos calculados
def re_muestrear_particulas(particulas, pesos):
    # Elegimos partículas con probabilidad proporcional a sus pesos
    indices = np.random.choice(range(num_particulas), size=num_particulas, p=pesos)
    return particulas[indices]

# -----------------------------
# 🐉 Proceso de Filtrado de Partículas (Dragón Mágico)
# -----------------------------

# Arreglos para las estimaciones de la posición y energía
estimaciones_posicion = []
estimaciones_energia = []

for t in range(1, num_pasos):
    # El dragón vuela y actualiza su posición y energía
    particulas_posicion = actualizar_particulas(particulas_posicion, ruido=2)  # Actualización con ruido
    particulas_energia = actualizar_particulas(particulas_energia, ruido=1)  # Actualización con ruido

    # Mediciones mágicas de la posición y energía del dragón (lo que se observa)
    medicion_posicion = posicion_observada[t]  
    medicion_energia = energia_observada[t]  

    # Reponderamos las partículas con base en las mediciones
    pesos_posicion = reponderar_particulas(particulas_posicion, medicion_posicion, sigma=3)  # Ponderamos posición
    pesos_energia = reponderar_particulas(particulas_energia, medicion_energia, sigma=1)  # Ponderamos energía

    # Re-muestreamos las partículas según los pesos calculados
    particulas_posicion = re_muestrear_particulas(particulas_posicion, pesos_posicion)
    particulas_energia = re_muestrear_particulas(particulas_energia, pesos_energia)

    # Estimamos la posición y energía del dragón como la media de las partículas
    estimacion_posicion = np.mean(particulas_posicion)  # Promedio de las posiciones
    estimacion_energia = np.mean(particulas_energia)    # Promedio de las energías

    # Guardamos las estimaciones para graficarlas después
    estimaciones_posicion.append(estimacion_posicion)
    estimaciones_energia.append(estimacion_energia)

# -----------------------------
# 🎨 Visualización de los Resultados del Vuelo Mágico
# -----------------------------

# Graficamos las estimaciones junto con las mediciones ruidosas
plt.figure(figsize=(12, 6))

# Gráfica de Posición del Dragón
plt.subplot(1, 2, 1)
plt.plot(posicion_latente, label='Posición Real', color='g', linewidth=2)  # Posición real del dragón
plt.plot(estimaciones_posicion, label='Estimación Posición', color='b', linestyle='--', linewidth=2)  # Estimación
plt.scatter(range(num_pasos), posicion_observada, label='Mediciones Ruidosas', color='r', alpha=0.5)  # Mediciones ruidosas
plt.xlabel('Tiempo')
plt.ylabel('Posición del Dragón')
plt.title('Filtrado de Partículas - Estimación de Posición')
plt.legend()
plt.grid(True)

# Gráfica de Energía del Dragón
plt.subplot(1, 2, 2)
plt.plot(energia_latente, label='Energía Real', color='g', linewidth=2)  # Energía real del dragón
plt.plot(estimaciones_energia, label='Estimación Energía', color='b', linestyle='--', linewidth=2)  # Estimación
plt.scatter(range(num_pasos), energia_observada, label='Mediciones Ruidosas', color='r', alpha=0.5)  # Mediciones ruidosas
plt.xlabel('Tiempo')
plt.ylabel('Energía del Dragón')
plt.title('Filtrado de Partículas - Estimación de Energía')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
