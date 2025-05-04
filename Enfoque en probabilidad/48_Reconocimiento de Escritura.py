# Importamos las librerías necesarias
import tensorflow as tf  # Librería principal de TensorFlow, utilizada para el manejo de redes neuronales
from tensorflow.keras import layers, models  # Keras es una API de alto nivel de TensorFlow para construir redes neuronales
import matplotlib.pyplot as plt  # Utilizada para mostrar las imágenes y los resultados visualmente

# Cargamos el dataset EMNIST (Extended MNIST) desde TensorFlow
# EMNIST es una extensión de MNIST que incluye letras manuscritas en lugar de solo dígitos
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.emnist.load_data()

# Preprocesamos los datos: normalizamos y redimensionamos las imágenes
# Las imágenes son de tamaño 28x28 píxeles y están en escala de grises (1 canal de color)
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))  # Redimensionamos las imágenes para agregar la dimensión del canal (en este caso 1)
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))  # Hacemos lo mismo para el conjunto de prueba

# Normalizamos las imágenes para que los valores estén entre 0 y 1
# Dividimos entre 255 porque las imágenes tienen valores de píxel de 0 a 255
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalización para mejorar el rendimiento de la red neuronal

# Construcción del modelo CNN
model = models.Sequential()  # Usamos un modelo secuencial, que apila capas de manera lineal

# Primera capa de Convolución: extrae características espaciales de las imágenes (por ejemplo, bordes, patrones simples)
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))  # 32 filtros, tamaño de filtro 3x3, activación ReLU
model.add(layers.MaxPooling2D((2, 2)))  # Capa de max-pooling para reducir la dimensionalidad (tamaño de la imagen)

# Segunda capa de Convolución: extracción de características más complejas
model.add(layers.Conv2D(64, (3, 3), activation='relu'))  # 64 filtros de 3x3
model.add(layers.MaxPooling2D((2, 2)))  # Nuevamente max-pooling para reducir el tamaño de la imagen

# Capa de aplanamiento (Flatten): convierte la salida 2D de la convolución a un vector 1D
model.add(layers.Flatten())  # La imagen se aplana para pasar a la capa densa

# Capa densa completamente conectada: las neuronas de esta capa se conectan con todas las neuronas de la capa anterior
model.add(layers.Dense(64, activation='relu'))  # 64 neuronas, función de activación ReLU

# Capa de salida: 26 neuronas para las 26 letras del alfabeto (A-Z)
model.add(layers.Dense(26, activation='softmax'))  # Función softmax para clasificación multiclase (26 letras)

# Compilamos el modelo
model.compile(optimizer='adam',  # Optimizador Adam, que ajusta los pesos para minimizar la función de pérdida
              loss='sparse_categorical_crossentropy',  # Pérdida para clasificación múltiple
              metrics=['accuracy'])  # Queremos seguir la precisión durante el entrenamiento

# Entrenamos el modelo
history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))
# El modelo entrenará durante 5 épocas con un tamaño de batch de 64 imágenes, y validará el desempeño en el conjunto de prueba

# Evaluamos el modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(x_test, y_test)  # Evaluación del modelo en datos de prueba
print(f"Precisión en el conjunto de prueba: {test_acc}")  # Imprimimos la precisión obtenida

# Mostramos una imagen de prueba y su predicción
plt.imshow(x_test[0].reshape(28, 28), cmap='gray')  # Mostramos la imagen de prueba (convertida a 28x28 píxeles)
plt.title(f"Predicción: {model.predict(x_test[0].reshape(1, 28, 28, 1)).argmax()}")  # Predicción de la letra
plt.show()  # Mostramos la imagen y el título con la predicción
