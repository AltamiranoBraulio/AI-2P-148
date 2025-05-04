# 📚 Importamos librerías necesarias
import numpy as np  # Para realizar cálculos matemáticos y operaciones con matrices
import matplotlib.pyplot as plt  # Para crear gráficos y visualizaciones
from sklearn.datasets import load_iris  # Para cargar el famoso conjunto de datos Iris

# ----------------------------------------------------
# 🧠 Clase que implementa un Mapa Autoorganizado (SOM)
class SelfOrganizingMap:
    def __init__(self, m, n, dim, learning_rate=0.5, radius=None, decay_rate=0.96):
        """
        m, n: Tamaño del mapa (m x n), cantidad de neuronas en el mapa
        dim: Dimensión de los vectores de entrada (ejemplo: 4 para Iris)
        """
        self.m = m  # Número de filas del mapa (alto del mapa)
        self.n = n  # Número de columnas del mapa (ancho del mapa)
        self.dim = dim  # Dimensión de los vectores de entrada (ejemplo: 4 características en Iris)
        self.learning_rate = learning_rate  # Tasa de aprendizaje inicial
        self.radius = max(m, n) / 2 if radius is None else radius  # Radio de vecindad inicial
        self.decay_rate = decay_rate  # Factor de decaimiento de la tasa de aprendizaje y el radio

        # 🔀 Inicializamos los pesos del SOM aleatoriamente dentro de un rango [0, 1]
        self.weights = np.random.rand(m, n, dim)  # (m, n) neuronas con dim características

    def _euclidean_distance(self, x, w):
        # 🔎 Calcula la distancia euclidiana entre el vector de entrada x y el peso w
        return np.linalg.norm(x - w)  # np.linalg.norm calcula la norma (distancia) de un vector

    def _find_bmu(self, x):
        """
        🕵️‍♂️ Encuentra la Neurona BMU (Best Matching Unit) para el dato x
        La BMU es la neurona que más se parece al dato de entrada
        """
        bmu_idx = (0, 0)  # Inicializamos la BMU (índice de la neurona más parecida)
        min_dist = np.inf  # Inicializamos la distancia mínima como infinita

        # Recorremos todas las neuronas del mapa para encontrar la BMU
        for i in range(self.m):  # Iteramos sobre las filas (m)
            for j in range(self.n):  # Iteramos sobre las columnas (n)
                dist = self._euclidean_distance(x, self.weights[i, j])  # Calculamos la distancia euclidiana
                if dist < min_dist:  # Si encontramos una distancia menor, actualizamos la BMU
                    min_dist = dist  # Actualizamos la distancia mínima
                    bmu_idx = (i, j)  # Actualizamos el índice de la BMU
        return bmu_idx  # Devolvemos la neurona más parecida al dato

    def fit(self, X, epochs=1000):
        """
        🧠 Método para entrenar el mapa SOM con los datos de entrada X
        """
        for epoch in range(epochs):  # Iteramos sobre las épocas (ciclos de entrenamiento)
            # 🔄 Calculamos el nuevo valor de la tasa de aprendizaje y el radio en cada época
            lr = self.learning_rate * (self.decay_rate ** epoch)  # Tasa de aprendizaje que disminuye con el tiempo
            rad = self.radius * (self.decay_rate ** epoch)  # Radio de vecindad que también disminuye con el tiempo

            # Recorremos todos los datos X para entrenar el mapa
            for x in X:
                # Encuentra la neurona BMU para cada dato
                bmu_idx = self._find_bmu(x)

                # 🔄 Ajustamos los pesos de las neuronas cercanas a la BMU
                for i in range(self.m):  # Iteramos sobre las filas (m)
                    for j in range(self.n):  # Iteramos sobre las columnas (n)
                        # Calculamos la distancia de cada neurona con la BMU
                        dist_to_bmu = np.linalg.norm(np.array([i, j]) - np.array(bmu_idx))
                        # Si la neurona está dentro del radio de vecindad de la BMU
                        if dist_to_bmu <= rad:
                            # Influencia de la neurona sobre la BMU disminuye con la distancia
                            influence = np.exp(-dist_to_bmu**2 / (2 * (rad**2)))  # Función gaussiana
                            # Actualizamos los pesos de la neurona
                            self.weights[i, j] += influence * lr * (x - self.weights[i, j])

            # 📢 Imprimimos información de la época cada 100 épocas para ver el progreso
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Radio: {rad:.4f}, LR: {lr:.4f}")

    def map_vects(self, X):
        """
        🔎 Mapea cada vector x de entrada en su BMU dentro del mapa (coordenadas i, j)
        """
        mapped = []  # Lista que almacenará los índices de la BMU para cada dato
        for x in X:
            bmu_idx = self._find_bmu(x)  # Encontramos la BMU para cada dato
            mapped.append(bmu_idx)  # Añadimos el índice de la BMU a la lista
        return mapped  # Devolvemos la lista de índices BMU

# ----------------------------------------------------
# 🎲 Cargamos los datos Iris (4 características: largo, ancho, etc)
iris = load_iris()  # Cargamos el conjunto de datos Iris
X = iris.data  # Los datos de las flores (150 muestras, 4 características)
y = iris.target  # Las etiquetas de las flores (0, 1, 2 para las 3 especies)

# 🧠 Creamos un SOM de 10x10 neuronas
som = SelfOrganizingMap(m=10, n=10, dim=4, learning_rate=0.5)
som.fit(X, epochs=1000)  # Entrenamos el SOM con los datos Iris durante 1000 épocas

# ----------------------------------------------------
# 🎨 Visualizamos el resultado
mapped = som.map_vects(X)  # Obtenemos las coordenadas (i, j) de la BMU para cada muestra

# 🎯 Dibujamos el mapa
plt.figure(figsize=(8, 8))  # Creamos una figura de tamaño 8x8 para el gráfico

# Usamos colores para cada clase de flores (rojo, verde, azul)
colors = ['r', 'g', 'b']
for i, m in enumerate(mapped):  # Iteramos sobre las coordenadas mapeadas
    plt.scatter(m[0], m[1], color=colors[y[i]], alpha=0.6)  # Dibujamos los puntos con colores según la clase

plt.title('🌐 Mapa Autoorganizado de Kohonen (SOM) - Iris')  # Título del gráfico
plt.xlabel('Coordenada X (Neuronas)')  # Etiqueta del eje X
plt.ylabel('Coordenada Y (Neuronas)')  # Etiqueta del eje Y
plt.grid(True)  # Activamos la cuadrícula en el gráfico
plt.show()  # Mostramos el gráfico
