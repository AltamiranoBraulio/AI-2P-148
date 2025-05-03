import numpy as np  # Importamos numpy para trabajar con matrices y álgebra lineal
import matplotlib.pyplot as plt  # Importamos matplotlib para graficar resultados

# ---------------------------------------------
# 🚗 Simulación: Auto en movimiento
# Queremos estimar la posición y velocidad del auto con un filtro de Kalman
# ---------------------------------------------

# Establecemos el intervalo de tiempo entre cada medición
dt = 1.0  # intervalo de tiempo (1 segundo)

# Generamos un array de tiempos de 0 a 20 segundos, en pasos de 1 segundo
tiempos = np.arange(0, 20, dt)  # 20 segundos

# El auto se mueve a una velocidad constante de 2 metros por segundo
# La verdadera posición sigue una función lineal con pendiente 2
verdadera_posicion = 2 * tiempos  # Establecemos la posición real, 2 m/s
# La verdadera velocidad es constante y vale 2 m/s
verdadera_velocidad = 2 * np.ones_like(tiempos)  # Velocidad constante

# Simulamos las mediciones del GPS, las cuales tienen ruido (desviación estándar de 2 metros)
ruido_sensor = np.random.normal(0, 2, size=tiempos.shape)  # Ruido gaussiano (desviación estándar 2)
# Las mediciones son las posiciones reales más el ruido
mediciones = verdadera_posicion + ruido_sensor  # Mediciones ruidosas (con error)

# ---------------------------------------------
# 🔧 Filtro de Kalman en 2D (posición y velocidad)
# ---------------------------------------------

# El estado inicial es [posición, velocidad], lo comenzamos en [0, 0]
# Esto significa que al principio, no sabemos ni la posición ni la velocidad
x = np.array([[0],  # posición inicial
              [0]])  # velocidad inicial

# La incertidumbre inicial sobre nuestro estado es alta, porque no tenemos información precisa
P = np.array([[1000, 0],  # Gran incertidumbre en posición
              [0, 1000]])  # Gran incertidumbre en velocidad

# El modelo de transición F describe cómo se actualiza el estado del auto con el tiempo
# El auto se mueve con velocidad constante: posición actual = posición anterior + velocidad * dt
F = np.array([[1, dt],  # [posición, velocidad] en el siguiente paso, para la posición
              [0, 1]])  # La velocidad no cambia con el tiempo en este caso (aceleración constante = 0)

# La matriz de control B no se utiliza aquí, porque no estamos controlando la aceleración directamente
B = np.array([[0],  # Sin aceleración externa
              [0]])  # Sin control sobre la velocidad

# La matriz de observación H mapea el estado (posición, velocidad) a las mediciones visibles
# En este caso, solo medimos la posición, no la velocidad
H = np.array([[1, 0]])  # La medición solo depende de la posición, no de la velocidad

# Incertidumbre del sensor: R define la varianza del ruido en las mediciones
# En este caso, el GPS tiene un error de 2 metros (varianza = 4)
R = np.array([[4]])  # Ruido de medición (desviación estándar de 2 metros)

# La matriz de ruido del proceso Q define la incertidumbre en el modelo de movimiento
# Como estamos trabajando con velocidad constante, asumimos que la incertidumbre en la posición es baja y en la velocidad es mayor
Q = np.array([[1, 0],  # Un pequeño error en la posición
              [0, 3]])  # Un poco más de incertidumbre en la velocidad

# Creamos una lista para almacenar las estimaciones de la posición a lo largo del tiempo
estimaciones = []

# ---------------------------------------------
# 🌀 Ciclo del filtro: para cada medición, hacemos predicción y corrección
# ---------------------------------------------
for z in mediciones:  # Para cada medición (ruidosa)
    # ----------------------
    # Paso 1: Predicción 🔮
    # ----------------------
    # Predicción del estado: cómo se actualiza la posición y la velocidad en función del modelo F
    x = F @ x + B  # Predicción del estado futuro. Multiplicamos F por el estado actual y agregamos B
    P = F @ P @ F.T + Q  # Predicción de la incertidumbre. La nueva incertidumbre depende de la anterior y del ruido del proceso (Q)

    # ----------------------
    # Paso 2: Actualización 🛠️
    # ----------------------
    # Calculamos la ganancia de Kalman (K), que decide cuánto confiar en la medición frente a la predicción
    # S es la incertidumbre total de la medición
    S = H @ P @ H.T + R  # La incertidumbre total es la incertidumbre del estado predicho + el ruido de la medición
    K = P @ H.T @ np.linalg.inv(S)  # La ganancia de Kalman

    # Ahora corregimos el estado predicho con la nueva medición
    z = np.array([[z]])  # Convertimos la medición en un array para hacer la resta
    y = z - H @ x  # Innovación (diferencia entre la medición y lo predicho por el modelo)

    # Actualización del estado usando la ganancia de Kalman y la innovación
    x = x + K @ y  # El nuevo estado es la predicción corregida

    # Actualización de la incertidumbre (para futuras predicciones)
    P = (np.eye(2) - K @ H) @ P  # La incertidumbre se actualiza restando la ganancia de Kalman multiplicada por H

    # Guardamos la estimación de la posición del auto
    estimaciones.append(x[0, 0])  # Solo nos interesa la posición, que es x[0, 0]

# ---------------------------------------------
# 🎨 Visualización
# ---------------------------------------------
# Graficamos el resultado final para comparar la verdadera posición, las mediciones y las estimaciones del filtro de Kalman
plt.figure(figsize=(10, 6))  # Creamos una figura de 10x6 pulgadas para la gráfica

# Graficamos la posición real del auto (sin ruido)
plt.plot(tiempos, verdadera_posicion, label='🚗 Posición real', color='g', linewidth=2)

# Graficamos las mediciones con ruido (GPS)
plt.scatter(tiempos, mediciones, label='📡 Mediciones (con ruido)', color='r', marker='x')

# Graficamos las estimaciones de la posición usando el filtro de Kalman
plt.plot(tiempos, estimaciones, label='🎯 Estimación por Kalman', color='b', linestyle='--', linewidth=2)

# Añadimos etiquetas y título
plt.xlabel('Tiempo (s)')  # Eje x es el tiempo en segundos
plt.ylabel('Posición (m)')  # Eje y es la posición en metros
plt.title('Filtro de Kalman - Seguimiento de un auto 🚗')  # Título de la gráfica

# Añadimos una leyenda para explicar las líneas
plt.legend()

# Activamos una cuadrícula para facilitar la lectura de la gráfica
plt.grid(True)

# Mostramos la gráfica
plt.show()
