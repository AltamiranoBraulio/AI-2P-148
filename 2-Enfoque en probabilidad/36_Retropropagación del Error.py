# 📚 Importamos librerías necesarias
import numpy as np  # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para graficar
from sklearn.datasets import make_moons  # Para generar datos de juguete no lineales
from sklearn.model_selection import train_test_split  # Para separar datos en entrenamiento y prueba
from sklearn.preprocessing import OneHotEncoder  # Para convertir etiquetas en formato one-hot

# ----------------------------------------------------
# 🎲 Generamos un conjunto de datos (dos lunas entrelazadas)
X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)  # Generamos 1000 puntos con ruido

# 🎯 Convertimos las etiquetas en formato one-hot (ej: clase 0 ➔ [1, 0], clase 1 ➔ [0, 1])
encoder = OneHotEncoder(sparse_output=False)  # ✅ Usamos sparse_output=False para versiones nuevas de scikit-learn
y_onehot = encoder.fit_transform(y.reshape(-1, 1))  # Convertimos y a matriz one-hot

# 🔀 Separamos en datos de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2, random_state=42)

# ----------------------------------------------------
# 🧠 Clase que implementa una Red Neuronal Multicapa simple con retropropagación
class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        # Inicializamos los pesos de entrada a capa oculta (valores pequeños aleatorios)
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        # Inicializamos los pesos de capa oculta a capa de salida
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.lr = learning_rate  # Tasa de aprendizaje

    def sigmoid(self, x):
        # 🟢 Función de activación sigmoide (suaviza valores entre 0 y 1)
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        # 🟢 Derivada de la función sigmoide (usada en retropropagación)
        return x * (1 - x)

    def fit(self, X, y, epochs=1000):
        for epoch in range(epochs):
            # 🚀 FORWARD PASS (propagación hacia adelante)
            z1 = np.dot(X, self.W1)  # Entrada a capa oculta
            a1 = self.sigmoid(z1)  # Activación de capa oculta

            z2 = np.dot(a1, self.W2)  # Entrada a capa de salida
            a2 = self.sigmoid(z2)  # Activación (salida final)

            # 🎯 Calculamos el error (diferencia entre salida deseada y salida actual)
            error = y - a2

            # 🔁 BACKPROPAGATION (retropropagación del error)
            d2 = error * self.sigmoid_derivative(a2)  # Gradiente para capa salida
            d1 = np.dot(d2, self.W2.T) * self.sigmoid_derivative(a1)  # Gradiente para capa oculta

            # 🔄 Ajustamos pesos usando los gradientes
            self.W2 += self.lr * np.dot(a1.T, d2)
            self.W1 += self.lr * np.dot(X.T, d1)

            # 📢 Imprimimos el error cada 100 epochs
            if epoch % 100 == 0:
                loss = np.mean(np.abs(error))  # Error promedio
                print(f"Epoch {epoch}, Error: {loss:.4f}")

    def predict(self, X):
        # 🚀 Paso hacia adelante para predicciones
        z1 = np.dot(X, self.W1)
        a1 = self.sigmoid(z1)
        z2 = np.dot(a1, self.W2)
        a2 = self.sigmoid(z2)
        return np.argmax(a2, axis=1)  # Elegimos la clase con mayor probabilidad

# ----------------------------------------------------
# 🚀 Creamos y entrenamos la red neuronal
nn = SimpleNeuralNetwork(input_size=2, hidden_size=5, output_size=2, learning_rate=0.1)
nn.fit(X_train, y_train, epochs=1000)

# ----------------------------------------------------
# 🔎 Evaluamos la red en los datos de prueba
y_pred = nn.predict(X_test)  # Predicciones
y_true = np.argmax(y_test, axis=1)  # Etiquetas verdaderas

# 🎯 Calculamos la precisión
accuracy = np.mean(y_pred == y_true)
print(f"\n🔍 Precisión en datos de prueba: {accuracy * 100:.2f}%")

# ----------------------------------------------------
# 🎨 Graficamos la frontera de decisión aprendida por la red

# Creamos una malla de puntos para graficar
xx, yy = np.meshgrid(np.linspace(-2, 3, 100), np.linspace(-1.5, 2, 100))
grid = np.c_[xx.ravel(), yy.ravel()]

# Predicciones para cada punto en la malla
Z = nn.predict(grid)
Z = Z.reshape(xx.shape)

# 🔵 Dibujamos la frontera
plt.contourf(xx, yy, Z, alpha=0.5, cmap='coolwarm')

# 🔴 Dibujamos los puntos reales
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k')

plt.title('🔀 Frontera de decisión aprendida por la Red Neuronal')
plt.xlabel('x1')
plt.ylabel('x2')
plt.show()
