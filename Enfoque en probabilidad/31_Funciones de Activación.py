# ---------------------------------------------------
# 📚 Importamos librerías
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 🔢 Definimos funciones de activación

# Sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# ReLU
def relu(x):
    return np.maximum(0, x)

# Tanh
def tanh(x):
    return np.tanh(x)

# Softmax (para un vector completo)
def softmax(x):
    e_x = np.exp(x - np.max(x))  # Estabilización numérica
    return e_x / e_x.sum(axis=0)

# ---------------------------------------------------
# 🎨 Graficamos las funciones
x = np.linspace(-10, 10, 100)

plt.figure(figsize=(12, 8))

# Sigmoide
plt.subplot(2, 2, 1)
plt.plot(x, sigmoid(x), color='blue')
plt.title('Sigmoide')
plt.grid(True)

# ReLU
plt.subplot(2, 2, 2)
plt.plot(x, relu(x), color='green')
plt.title('ReLU')
plt.grid(True)

# Tanh
plt.subplot(2, 2, 3)
plt.plot(x, tanh(x), color='purple')
plt.title('Tanh')
plt.grid(True)

# Softmax (en vector)
plt.subplot(2, 2, 4)
# Tomamos un vector con 3 valores para simular softmax
vector_softmax = softmax(np.array([x1 for x1 in [1, 2, 3]]))
plt.bar([1, 2, 3], vector_softmax, color='orange')
plt.title('Softmax (vector)')
plt.grid(True)

plt.tight_layout()
plt.show()
