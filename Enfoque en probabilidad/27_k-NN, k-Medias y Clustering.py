# ---------------------------------------------
# 1. 🚀 Importamos las librerías necesarias
# ---------------------------------------------

# Numpy es una librería que nos ayuda a trabajar con arreglos multidimensionales
import numpy as np
# Matplotlib se usa para crear gráficos y visualizar datos
import matplotlib.pyplot as plt
# KMeans es el algoritmo de clustering que vamos a usar para agrupar clientes
from sklearn.cluster import KMeans
# KNeighborsClassifier es el algoritmo de clasificación k-NN que usaremos para predecir el grupo de un cliente
from sklearn.neighbors import KNeighborsClassifier
# train_test_split se usa para dividir los datos en un conjunto de entrenamiento y uno de prueba
from sklearn.model_selection import train_test_split
# StandardScaler se usa para normalizar nuestros datos (hacer que todas las características estén en la misma escala)
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------
# 2. 📊 Datos ficticios de clientes (Edad, Ingreso, Frecuencia de Compra)
# ---------------------------------------------
# Definimos los datos de clientes: cada fila es un cliente con tres características:
# [Edad, Ingreso Anual, Frecuencia de Compra al Año]
clientes = np.array([
    [25, 50000, 10],  # Cliente 1: Edad = 25, Ingreso = 50000, Frecuencia de Compra = 10 veces al año
    [35, 80000, 5],   # Cliente 2
    [45, 120000, 2],  # Cliente 3
    [23, 30000, 15],  # Cliente 4
    [33, 60000, 7],   # Cliente 5
    [50, 150000, 1],  # Cliente 6
    [29, 70000, 12],  # Cliente 7
    [41, 100000, 3],  # Cliente 8
    [28, 65000, 8],   # Cliente 9
    [39, 90000, 4],   # Cliente 10
])

# ---------------------------------------------
# 3. 🎯 Características: Edad, Ingreso, Frecuencia de Compra
# ---------------------------------------------
# Extraemos las dos primeras columnas que son las características (Edad, Ingreso)
X = clientes[:, :-1]  # [:, :-1] significa que tomamos todas las filas y todas las columnas menos la última
# Extraemos la última columna, que es la frecuencia de compra, y la usaremos como las etiquetas reales
y_real = clientes[:, -1]  # [:, -1] significa que tomamos la última columna (Frecuencia de Compra)

# ---------------------------------------------
# 4. 📊 Preprocesamiento de datos: Normalizamos las características
# ---------------------------------------------
# Creamos un objeto de StandardScaler, que nos ayudará a normalizar las características
scaler = StandardScaler()
# Normalizamos las características (Edad, Ingreso)
X_scaled = scaler.fit_transform(X)  # fit_transform ajusta y transforma los datos de X

# ---------------------------------------------
# 5. 🔍 Clustering de clientes con k-Means
# ---------------------------------------------
# Creamos el modelo k-Means con 3 grupos (porque estamos segmentando en 3 tipos de clientes)
kmeans = KMeans(n_clusters=3, random_state=42)
# Ajustamos el modelo k-Means a nuestros datos normalizados (Edad, Ingreso)
clusters = kmeans.fit_predict(X_scaled)  # fit_predict ajusta el modelo y devuelve las etiquetas del grupo

# ---------------------------------------------
# 6. 📈 Visualización de los clusters
# ---------------------------------------------
# Creamos un gráfico de dispersión para ver cómo se distribuyen los clientes en los clusters
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis')  # X_scaled[:, 0] es Edad, X_scaled[:, 1] es Ingreso
# Título del gráfico
plt.title('Segmentación de Clientes (k-Means)')
# Etiquetas de los ejes
plt.xlabel('Edad Normalizada')
plt.ylabel('Ingreso Normalizado')
# Añadimos una barra de colores que representa los diferentes grupos
plt.colorbar(label='Grupo de Cliente')
# Mostramos el gráfico
plt.show()

# ---------------------------------------------
# 7. 👥 Dividir los datos para el modelo k-NN
# ---------------------------------------------
# Usamos los grupos generados por k-Means como etiquetas (y) para el modelo k-NN
y = clusters  # Las etiquetas para el entrenamiento son los grupos que k-Means creó

# Dividimos los datos en dos conjuntos: uno de entrenamiento y otro de prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
# Esto significa que el 30% de los datos se usarán para prueba y el 70% para entrenamiento

# ---------------------------------------------
# 8. ⚙️ Entrenamiento de modelo k-NN
# ---------------------------------------------
# Creamos el clasificador k-NN con 3 vecinos más cercanos
knn = KNeighborsClassifier(n_neighbors=3)
# Entrenamos el modelo k-NN con los datos de entrenamiento
knn.fit(X_train, y_train)

# ---------------------------------------------
# 9. 🔮 Predicción para un nuevo cliente
# ---------------------------------------------
# Supongamos que tenemos un nuevo cliente con Edad = 30 e Ingreso = 75000
nuevo_cliente = np.array([[30, 75000]])
# Normalizamos las características del nuevo cliente con el mismo escalador utilizado antes
nuevo_cliente_scaled = scaler.transform(nuevo_cliente)  # transform() aplica la misma transformación a los nuevos datos

# ---------------------------------------------
# 10. 🧩 Predicción del grupo al que pertenece el nuevo cliente
# ---------------------------------------------
# Usamos el modelo k-NN para predecir a qué grupo pertenece el nuevo cliente
grupo_predicho = knn.predict(nuevo_cliente_scaled)

# ---------------------------------------------
# 11. 📊 Visualización de la predicción
# ---------------------------------------------
# Mostramos en consola el grupo predicho para el nuevo cliente
print(f"El nuevo cliente pertenece al Grupo {grupo_predicho[0]}")

# ---------------------------------------------
# 12. 📈 Visualización de los resultados
# ---------------------------------------------
# Ahora visualizamos los resultados de la clasificación k-NN y mostramos el nuevo cliente
# Primero, graficamos los datos de entrenamiento
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='viridis', label='Entrenamiento')
# Luego, mostramos al nuevo cliente como un punto rojo
plt.scatter(nuevo_cliente_scaled[:, 0], nuevo_cliente_scaled[:, 1], c='red', marker='x', s=200, label='Nuevo Cliente')
# Título del gráfico
plt.title('Clasificación de Clientes con k-NN')
# Etiquetas de los ejes
plt.xlabel('Edad Normalizada')
plt.ylabel('Ingreso Normalizado')
# Mostramos la leyenda para identificar el nuevo cliente
plt.legend()
# Mostramos el gráfico
plt.show()
