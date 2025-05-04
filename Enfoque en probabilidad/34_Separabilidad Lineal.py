# 📚 Importamos las librerías necesarias
import numpy as np  # Para operaciones numéricas y generación de datos
import matplotlib.pyplot as plt  # Para graficar datos y resultados

# ---------------------------------------------------
# 🧠 Definimos la clase Perceptrón (nuestro modelo de aprendizaje)
class Perceptron:
    # Método constructor: inicializa el perceptrón
    def __init__(self, input_size, learning_rate=0.1):
        # Creamos un vector de pesos inicializado en ceros (incluye bias, por eso +1)
        self.weights = np.zeros(input_size + 1)  # Ejemplo: si input_size=2, tendremos 3 pesos (w0, w1, w2)
        self.lr = learning_rate  # Tasa de aprendizaje (qué tan rápido aprende el perceptrón)

    # 🔥 Función de activación: devuelve 1 si la entrada es mayor o igual a 0, sino devuelve 0
    def activation_fn(self, x):
        return np.where(x >= 0, 1, 0)  # Implementa la función escalón

    # 🔮 Método para hacer una predicción
    def predict(self, x):
        # Producto punto entre pesos y entrada (x incluye bias)
        z = self.weights.T.dot(x)  # z = w0*x0 + w1*x1 + w2*x2
        return self.activation_fn(z)  # Aplica función escalón y devuelve 0 o 1

    # 🚀 Método para entrenar el perceptrón
    def fit(self, X, d, epochs=10):
        # Itera sobre el número de épocas (repeticiones sobre los datos)
        for _ in range(epochs):
            # Itera sobre cada muestra (xi) y su etiqueta (target)
            for xi, target in zip(X, d):
                output = self.predict(xi)  # Predicción actual
                error = target - output  # Calcula error (deseado - obtenido)
                # Actualiza pesos usando la regla delta: w = w + lr * error * x
                self.weights += self.lr * error * xi

# ---------------------------------------------------
# 🎲 Generamos datos aleatorios pero que sí son linealmente separables

# Generamos 50 puntos para la Clase 0, centrados cerca de (1,1)
class0 = np.random.randn(50, 2) * 0.3 + [1, 1]

# Generamos 50 puntos para la Clase 1, centrados cerca de (3,3)
class1 = np.random.randn(50, 2) * 0.3 + [3, 3]

# Unimos los puntos de ambas clases en un solo array
X_data = np.vstack((class0, class1))  # Ahora tenemos 100 puntos en total (50 + 50)

# 🚩 Agregamos columna de 1s para el bias
# Ejemplo: si X_data = [x1, x2], X_bias = [1, x1, x2]
X_bias = np.hstack((np.ones((X_data.shape[0], 1)), X_data))

# Creamos las etiquetas: primeros 50 puntos son clase 0, los otros 50 son clase 1
d_labels = np.array([0]*50 + [1]*50)

# ---------------------------------------------------
# 🚀 Entrenamos el Perceptrón con nuestros datos
p = Perceptron(input_size=2)  # Creamos una instancia del perceptrón (2 entradas: x1 y x2)
p.fit(X_bias, d_labels, epochs=20)  # Entrenamos durante 20 épocas

# ---------------------------------------------------
# 🎨 Graficamos los puntos en un plano

# Puntos rojos para la Clase 0
plt.scatter(class0[:,0], class0[:,1], color='red', label='Clase 0')
# Puntos azules para la Clase 1
plt.scatter(class1[:,0], class1[:,1], color='blue', label='Clase 1')

# 🎯 Ahora graficamos la línea separadora que aprendió el perceptrón

# 📏 Ecuación de la línea: w0*1 + w1*x + w2*y = 0
# Despejamos y: y = (-w0 - w1*x) / w2

# Generamos valores x (de 0 a 4) para trazar la línea
x_vals = np.linspace(0, 4, 100)

# Calculamos los valores y usando la ecuación aprendida
y_vals = (-p.weights[0] - p.weights[1]*x_vals) / p.weights[2]

# Dibujamos la línea verde
plt.plot(x_vals, y_vals, color='green', linewidth=2, label='Línea Separadora')

# 🏷️ Añadimos título y etiquetas
plt.title('Separabilidad Lineal aprendida por Perceptrón')
plt.xlabel('x1')
plt.ylabel('x2')

# 📜 Mostramos leyenda
plt.legend()

# 🗺️ Mostramos la cuadrícula
plt.grid(True)

# 🚀 Finalmente mostramos la gráfica
plt.show()
