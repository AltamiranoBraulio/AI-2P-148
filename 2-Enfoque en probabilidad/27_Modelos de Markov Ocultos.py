import numpy as np
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

# ---------------------------------------------
# 🌸 Datos de Observación: Temperaturas diarias
# Vamos a usar temperaturas ficticias para representar los días pasados
temperaturas = np.array([22, 24, 19, 18, 20, 21, 26, 28, 30, 25, 18, 17, 23]).reshape(-1, 1)

# ---------------------------------------------
# 🌿 Definición del Modelo de Markov Oculto (HMM)
# Usamos un modelo HMM con 2 estados ocultos (Soleado, Nublado)
modelo = GaussianHMM(n_components=2, covariance_type="full", random_state=42)

# Establecer las probabilidades iniciales (probabilidades de estar en un estado al principio)
modelo.startprob_ = np.array([0.5, 0.5])  # 50% de probabilidad de estar en Soleado o Nublado al principio

# Establecer las probabilidades de transición entre estados ocultos
modelo.transmat_ = np.array([[0.7, 0.3],  # Si es Soleado, hay 70% de probabilidad de seguir Soleado
                             [0.4, 0.6]]) # Si es Nublado, hay 60% de probabilidad de seguir Nublado

# Establecer las probabilidades de emisión (relación entre temperatura y estado oculto)
modelo.emissionprob_ = np.array([[0.1, 0.7, 0.2],  # Soleado: baja probabilidad para frío, alta probabilidad para templado, baja para caliente
                                 [0.3, 0.5, 0.2]]) # Nublado: probabilidad más equilibrada

# ---------------------------------------------
# 🔄 Ajustar el modelo a las observaciones (temperaturas)
modelo.fit(temperaturas)

# ---------------------------------------------
# 🌿 Predicción de los estados ocultos (Soleado o Nublado)
predicciones = modelo.predict(temperaturas)

# ---------------------------------------------
# 🌸 Mostrar resultados
# Imprimir las predicciones de los estados ocultos
print("Observaciones (Temperaturas):", temperaturas.flatten())
print("Predicciones de Clima (0= Soleado, 1= Nublado):", predicciones)

# ---------------------------------------------
# 🌸 Visualización de los resultados
plt.plot(temperaturas.flatten(), label="Temperaturas Observadas", marker="o")
plt.plot(predicciones, label="Estados Ocultos Predichos", marker="x", linestyle="--")
plt.title("Predicción de Clima usando Modelo de Markov Oculto")
plt.legend()
plt.xlabel("Días")
plt.ylabel("Temperatura / Estado de Clima")
plt.show()
