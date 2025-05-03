# ---------------------------------------------
# 💡 Agrupamiento de Películas con K-means
# ---------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ---------------------------------------------
# 1. 📊 Datos Simulados de Películas
# Características: [Duración (minutos), Número de Reseñas, Calificación Promedio]
X = np.array([
    [90, 1200, 4.5],  # Película 1
    [150, 3000, 4.8], # Película 2
    [100, 200, 3.9],  # Película 3
    [140, 1500, 4.2], # Película 4
    [85, 300, 4.0],   # Película 5
    [110, 4000, 4.7], # Película 6
    [120, 1800, 4.3], # Película 7
])

# ---------------------------------------------
# 2. 🔄 Aplicación de K-means
# Vamos a agrupar las películas en 2 grupos: Acción y Drama (como ejemplo)

modelo_kmeans = KMeans(n_clusters=2, random_state=42)
modelo_kmeans.fit(X)

# ---------------------------------------------
# 3. 🎨 Visualización de los Resultados
# Dibujamos las películas en función de su duración y calificación

plt.figure(figsize=(8, 6))

# Usamos los colores de los clusters para diferenciar las películas
plt.scatter(X[:, 0], X[:, 2], c=modelo_kmeans.labels_, cmap='viridis', s=100)

# Etiquetas de los ejes
plt.title('💡 Agrupamiento de Películas: Acción vs Drama')
plt.xlabel('Duración (minutos)')
plt.ylabel('Calificación Promedio')

# Mostramos los centros de los clusters (medias de duración y calificación)
centros = modelo_kmeans.cluster_centers_
plt.scatter(centros[:, 0], centros[:, 2], c='red', marker='X', s=200, label='Centros de Clusters')

# Mostramos la leyenda
plt.legend()

# Mostramos el gráfico
plt.show()

# ---------------------------------------------
# 4. 📊 Imprimir los Centros de los Clusters
print("Centros de los Clusters encontrados por K-means (Duración, Calificación):")
print(centros)
