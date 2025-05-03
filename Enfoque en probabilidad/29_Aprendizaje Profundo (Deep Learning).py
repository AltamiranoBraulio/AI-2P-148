# Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# ---------------------------------------------
# 1. Cargar el conjunto de datos MNIST
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

# ---------------------------------------------
# 2. Preprocesamiento de datos
# Normalizamos los píxeles (de 0-255 a 0-1)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Convertimos etiquetas a one-hot
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# ---------------------------------------------
# 3. Crear el modelo Deep Learning
model = Sequential([
    Flatten(input_shape=(28, 28)),      # Aplanamos imagen 28x28 a vector
    Dense(128, activation='relu'),      # Capa oculta con 128 neuronas
    Dense(64, activation='relu'),       # Otra capa oculta
    Dense(10, activation='softmax')     # Salida: 10 clases (dígitos 0-9)
])

# Compilamos el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# ---------------------------------------------
# 4. Entrenar el modelo
history = model.fit(X_train, y_train_cat, epochs=5, validation_split=0.1, verbose=2)

# ---------------------------------------------
# 5. Evaluar el modelo
test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
print(f"Precisión en datos de prueba: {test_acc:.2f}")

# ---------------------------------------------
# 6. Visualizar predicciones
predictions = model.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)

# Mostrar 12 imágenes aleatorias de prueba y su predicción
plt.figure(figsize=(12, 6))
for i in range(12):
    index = np.random.randint(0, len(X_test))
    plt.subplot(3, 4, i + 1)
    plt.imshow(X_test[index], cmap='gray')
    plt.axis('off')
    # Título: si acertó, verde ✔️; si falló, rojo ❌
    color = 'green' if predicted_labels[index] == y_test[index] else 'red'
    plt.title(f"Pred: {predicted_labels[index]}", color=color)
plt.suptitle('Predicciones de la Red Neuronal', fontsize=16)
plt.show()
