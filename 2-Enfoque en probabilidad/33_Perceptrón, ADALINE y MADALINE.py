# 📚 Importamos librerías necesarias
import numpy as np  # Librería para operaciones matemáticas, especialmente matrices y vectores
import matplotlib.pyplot as plt  # Librería para crear gráficos y visualizaciones

# ---------------------------------------------------
# 🧠 Definimos la clase Perceptron (modelo clásico de red neuronal)
class Perceptron:
    # Método para inicializar el objeto Perceptron
    def __init__(self, input_size, learning_rate=0.1):
        # Creamos un vector de pesos inicializados en cero. 
        # input_size + 1 es porque agregamos un peso adicional para el sesgo (bias).
        self.weights = np.zeros(input_size + 1)
        # Guardamos la tasa de aprendizaje que nos dice qué tan grandes son los ajustes en los pesos
        self.lr = learning_rate

    # Definimos la función de activación (función escalón)
    def activation_fn(self, x):
        # Si x es mayor o igual a 0, devuelve 1; si no, devuelve 0.
        # Esta función decide si la neurona "se activa" o no.
        return np.where(x >= 0, 1, 0)

    # Método para hacer una predicción con el perceptrón
    def predict(self, x):
        # Calculamos la suma ponderada (producto punto entre pesos y entradas)
        z = self.weights.T.dot(x)
        # Aplicamos la función de activación para obtener la salida final (0 o 1)
        return self.activation_fn(z)

    # Método para entrenar el perceptrón
    def fit(self, X, d, epochs=10):
        # Repetimos el proceso de entrenamiento varias veces (epochs)
        for _ in range(epochs):
            # Iteramos sobre cada par de muestra (xi) y su etiqueta deseada (target)
            for xi, target in zip(X, d):
                # Calculamos la predicción actual
                output = self.predict(xi)
                # Calculamos el error (deseado - predicho)
                error = target - output
                # Ajustamos los pesos según el error. 
                # La fórmula: nuevo_peso = peso_actual + tasa_aprendizaje * error * entrada
                self.weights += self.lr * error * xi

# ---------------------------------------------------
# 🧠 Definimos la clase ADALINE (versión mejorada del Perceptrón)
class Adaline:
    # Método para inicializar el objeto Adaline
    def __init__(self, input_size, learning_rate=0.01):
        # Pesos iniciales en cero (incluye el peso para el sesgo)
        self.weights = np.zeros(input_size + 1)
        # Tasa de aprendizaje
        self.lr = learning_rate

    # Calcula la suma ponderada de entradas y pesos (sin función de activación)
    def net_input(self, x):
        return self.weights.T.dot(x)

    # Función de activación (aquí es similar al perceptrón, pero se aplica después del ajuste)
    def activation_fn(self, x):
        # Si la suma es mayor o igual a 0.5, devuelve 1; si no, devuelve 0
        return np.where(x >= 0.5, 1, 0)

    # Método para predecir usando ADALINE
    def predict(self, x):
        # Calculamos la suma ponderada
        z = self.net_input(x)
        # Aplicamos la función de activación para obtener 0 o 1
        return self.activation_fn(z)

    # Método para entrenar ADALINE
    def fit(self, X, d, epochs=10):
        # Repetimos el entrenamiento varias veces
        for _ in range(epochs):
            # Iteramos sobre cada muestra y su salida deseada
            for xi, target in zip(X, d):
                # Calculamos la salida (sin activar)
                output = self.net_input(xi)
                # Calculamos el error
                error = target - output
                # Ajustamos los pesos usando la Regla Delta
                self.weights += self.lr * error * xi

# ---------------------------------------------------
# 📊 Definimos los datos de entrada para entrenar (caso: función OR lógica)
X = np.array([
    [1, 0, 0],  # Entrada 1: sesgo=1, x1=0, x2=0
    [1, 0, 1],  # Entrada 2: sesgo=1, x1=0, x2=1
    [1, 1, 0],  # Entrada 3: sesgo=1, x1=1, x2=0
    [1, 1, 1]   # Entrada 4: sesgo=1, x1=1, x2=1
])

# 🎯 Salidas deseadas (target) para la función OR
# OR(0,0)=0, OR(0,1)=1, OR(1,0)=1, OR(1,1)=1
d = np.array([0, 1, 1, 1])

# ---------------------------------------------------
# 🚀 Entrenamos y probamos el Perceptrón

# Creamos una instancia del Perceptrón con 2 entradas (x1 y x2)
p = Perceptron(input_size=2)
# Llamamos al método fit para entrenarlo con los datos X y las salidas d
p.fit(X, d)

# Imprimimos los resultados del Perceptrón después del entrenamiento
print("🔎 Perceptrón resultados:")
# Iteramos sobre cada entrada para hacer predicciones
for x in X:
    # Imprimimos las entradas (x1 y x2) y la predicción que hace el modelo
    print(f"Entrada: {x[1:]}, Predicción: {p.predict(x)}")

# ---------------------------------------------------
# 🚀 Entrenamos y probamos ADALINE

# Creamos una instancia de ADALINE con 2 entradas
a = Adaline(input_size=2)
# Entrenamos el ADALINE con los datos
a.fit(X, d)

# Imprimimos los resultados de ADALINE después del entrenamiento
print("\n🔎 ADALINE resultados:")
# Iteramos sobre cada entrada para hacer predicciones
for x in X:
    # Imprimimos las entradas y la predicción hecha por ADALINE
    print(f"Entrada: {x[1:]}, Predicción: {a.predict(x)}")

# ---------------------------------------------------
# 🎨 Graficamos los puntos de entrada en 2D para visualización

# Usamos scatter plot para graficar los puntos:
# Eje X: valores de x1 (0,0,1,1)
# Eje Y: valores de x2 (0,1,0,1)
# Colores: usamos 'd' para colorear según la clase (rojo=0, azul=1)
plt.scatter([0, 0, 1, 1], [0, 1, 0, 1], c=d, cmap='bwr', s=100)  # Tamaño 100 para que se vean grandes
plt.title('Puntos clasificados (rojo=0, azul=1)')  # Título del gráfico
plt.grid(True)  # Activamos la cuadrícula
plt.show()  # Mostramos el gráfico
