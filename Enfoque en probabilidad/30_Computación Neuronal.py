# ---------------------------------------------
# 🧠 Computación Neuronal: Clasificación de frutas
# ---------------------------------------------

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ---------------------------------------------
# 1. 📊 Datos de ejemplo (peso en gramos y tamaño en cm)
# Etiqueta 0 = Ligera, 1 = Pesada
# Ejemplo: [peso, tamaño]
datos = np.array([
    [100, 5],   # Ligera
    [150, 6],   # Ligera
    [200, 7],   # Pesada
    [250, 8],   # Pesada
    [90, 4.5],  # Ligera
    [300, 9],   # Pesada
])

# Etiquetas
etiquetas = np.array([0, 0, 1, 1, 0, 1])

# ---------------------------------------------
# 2. 🔥 Crear modelo de Red Neuronal (Computación Neuronal)
modelo = keras.Sequential([
    layers.Dense(4, activation='relu', input_shape=(2,)),  # Capa oculta con 4 neuronas
    layers.Dense(1, activation='sigmoid')  # Capa de salida (0 o 1)
])

# ---------------------------------------------
# 3. ⚙️ Compilar el modelo
modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ---------------------------------------------
# 4. 🎯 Entrenar la red neuronal
modelo.fit(datos, etiquetas, epochs=50, verbose=0)

# ---------------------------------------------
# 5. 🔮 Probar con un nuevo dato
nueva_fruta = np.array([[180, 7]])  # Peso: 180g, Tamaño: 7cm
prediccion = modelo.predict(nueva_fruta)

# Mostrar resultado
if prediccion[0][0] > 0.5:
    print("✅ La fruta es PESADA")
else:
    print("🍏 La fruta es LIGERA")
