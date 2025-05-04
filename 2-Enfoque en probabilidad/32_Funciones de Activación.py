# ---------------------------------------------------
# 📚 Importamos librerías necesarias

import numpy as np  # Importamos NumPy, que es una librería para operaciones matemáticas y matrices (arreglos)
import matplotlib.pyplot as plt  # Importamos Matplotlib para poder graficar nuestros resultados de forma visual

# ---------------------------------------------------
# 🔢 Definimos funciones matemáticas llamadas "Funciones de Activación"
# Son usadas en redes neuronales para decidir si una neurona "se activa" o no.

# 📈 Función Sigmoide
def sigmoid(x):  # Definimos una función llamada sigmoid que toma una variable 'x'
    return 1 / (1 + np.exp(-x))  # Devuelve el resultado de la fórmula 1 / (1 + e^(-x)), que siempre da valores entre 0 y 1

# 🟩 Función ReLU (Rectified Linear Unit)
def relu(x):  # Definimos la función ReLU que toma 'x'
    return np.maximum(0, x)  # Devuelve 'x' si es positivo y 0 si es negativo (es decir, filtra todos los valores negativos)

# 🔄 Función Tangente Hiperbólica (Tanh)
def tanh(x):  # Definimos la función tanh que toma 'x'
    return np.tanh(x)  # Devuelve el valor tanh de 'x', que siempre estará entre -1 y 1 (más fuerte que sigmoide)

# 🎯 Función Softmax (convierte un vector en probabilidades)
def softmax(x):  # Definimos la función softmax que toma 'x' (puede ser un array)
    e_x = np.exp(x - np.max(x))  # Calculamos e^x para cada elemento pero primero le restamos el máximo para estabilización numérica
    return e_x / e_x.sum(axis=0)  # Dividimos cada e^x por la suma total, así obtenemos "probabilidades" que suman 1

# ---------------------------------------------------
# 🎨 Graficamos las funciones para entenderlas visualmente

# Creamos un array llamado 'x' que contiene 100 valores entre -10 y 10 (espaciados de forma uniforme)
x = np.linspace(-10, 10, 100)

# Creamos una figura donde vamos a poner 4 gráficos. Ajustamos su tamaño a 12x8 pulgadas.
plt.figure(figsize=(12, 8))

# ---------------------------------------------------
# 🔵 Graficamos la función Sigmoide

plt.subplot(2, 2, 1)  # Dividimos la ventana en 2 filas y 2 columnas y usamos el primer espacio
plt.plot(x, sigmoid(x), color='blue')  # Graficamos los valores de x contra su valor sigmoide, en color azul
plt.title('Sigmoide')  # Ponemos título al gráfico
plt.grid(True)  # Activamos la grilla para mejor visualización

# ---------------------------------------------------
# 🟩 Graficamos la función ReLU

plt.subplot(2, 2, 2)  # Usamos el segundo espacio en la ventana (arriba a la derecha)
plt.plot(x, relu(x), color='green')  # Graficamos x contra ReLU(x), en color verde
plt.title('ReLU')  # Título del gráfico
plt.grid(True)  # Activamos grilla

# ---------------------------------------------------
# 🟣 Graficamos la función Tanh

plt.subplot(2, 2, 3)  # Tercer espacio (abajo a la izquierda)
plt.plot(x, tanh(x), color='purple')  # Graficamos x contra tanh(x), en color púrpura
plt.title('Tanh')  # Título del gráfico
plt.grid(True)  # Activamos grilla

# ---------------------------------------------------
# 🟠 Graficamos la función Softmax

plt.subplot(2, 2, 4)  # Cuarto espacio (abajo a la derecha)

# Creamos un pequeño vector [1, 2, 3] y lo pasamos a la función softmax para obtener sus probabilidades
vector_softmax = softmax(np.array([x1 for x1 in [1, 2, 3]]))  

# Graficamos un gráfico de barras para visualizar la salida softmax
plt.bar([1, 2, 3], vector_softmax, color='orange')  # Dibujamos 3 barras con los valores resultantes y color naranja
plt.title('Softmax (vector)')  # Título del gráfico
plt.grid(True)  # Activamos grilla

# ---------------------------------------------------
# 📏 Ajustamos la distribución de los gráficos para que no se encimen
plt.tight_layout()

# 👁️ Mostramos la ventana con todos los gráficos
plt.show()
