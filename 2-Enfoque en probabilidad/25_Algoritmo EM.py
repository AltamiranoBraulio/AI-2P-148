# ---------------------------------------------
# 🌸 Clustering de flores usando Algoritmo EM (Gaussian Mixture)
# ---------------------------------------------

# Importamos numpy para manejar arreglos numéricos
import numpy as np
# Importamos matplotlib para crear gráficos
import matplotlib.pyplot as plt
# Importamos datasets reales de sklearn (como Iris)
from sklearn import datasets
# Importamos el modelo GaussianMixture que usa el algoritmo EM
from sklearn.mixture import GaussianMixture

# ---------------------------------------------
# 1. 📚 Cargar datos reales (dataset Iris)

# Cargamos el famoso dataset Iris que tiene datos de flores
iris = datasets.load_iris()

# Seleccionamos solo las primeras 2 características:
# (columna 0: largo del sépalo, columna 1: ancho del sépalo)
# Esto lo hacemos para poder graficar en 2D.
X = iris.data[:, :2]

# Guardamos las etiquetas reales (0 = Setosa, 1 = Versicolor, 2 = Virginica)
y_real = iris.target

# ---------------------------------------------
# 2. 🔄 Crear modelo EM con 3 componentes (porque hay 3 tipos de flores)

# Creamos un modelo GaussianMixture:
# - n_components=3 porque sabemos que hay 3 tipos de flores.
# - covariance_type='full' permite que cada componente tenga su propia forma elíptica.
# - random_state=0 asegura que los resultados sean siempre los mismos si volvemos a ejecutar.
modelo_em = GaussianMixture(n_components=3, covariance_type='full', random_state=0)

# Ajustamos el modelo a nuestros datos X:
# El algoritmo EM comienza a estimar las "mezclas gaussianas" que mejor explican los datos.
modelo_em.fit(X)

# Ahora usamos el modelo entrenado para predecir a qué grupo (cluster) pertenece cada flor.
# Esto devuelve un array con valores 0, 1 o 2 indicando el grupo asignado.
predicciones = modelo_em.predict(X)

# ---------------------------------------------
# 3. 🎨 Visualizar los resultados

# Creamos una nueva figura de tamaño 8x4 pulgadas
plt.figure(figsize=(8, 4))

# -----------------
# Subplot 1: Clusters hallados por EM
# -----------------

# Creamos el primer subplot (1 fila, 2 columnas, posición 1)
plt.subplot(1, 2, 1)

# Dibujamos un scatter plot (diagrama de puntos)
# - X[:, 0]: eje x (largo del sépalo)
# - X[:, 1]: eje y (ancho del sépalo)
# - c=predicciones: coloreamos los puntos según el cluster que el modelo EM asignó
# - cmap='viridis': usamos una paleta de colores bonita
# - s=50: tamaño de los puntos
plt.scatter(X[:, 0], X[:, 1], c=predicciones, cmap='viridis', s=50)

# Título del gráfico
plt.title('🔮 Clusters Encontrados (EM)')

# Etiqueta del eje x
plt.xlabel('Largo Sépalo (cm)')

# Etiqueta del eje y
plt.ylabel('Ancho Sépalo (cm)')

# -----------------
# Subplot 2: Etiquetas reales (por comparación)
# -----------------

# Creamos el segundo subplot (1 fila, 2 columnas, posición 2)
plt.subplot(1, 2, 2)

# Dibujamos otro scatter plot
# - Esta vez coloreamos usando y_real, que son las etiquetas verdaderas del dataset.
plt.scatter(X[:, 0], X[:, 1], c=y_real, cmap='viridis', s=50)

# Título del gráfico
plt.title('✅ Clusters Reales (Iris)')

# Etiqueta del eje x
plt.xlabel('Largo Sépalo (cm)')

# Etiqueta del eje y
plt.ylabel('Ancho Sépalo (cm)')

# -----------------
# Ajustamos automáticamente los espacios entre subplots para que no se encimen
plt.tight_layout()

# Mostramos la ventana con las 2 gráficas
plt.show()
