# 🔶 Importación de las librerías necesarias
import cv2  # Librería OpenCV para procesamiento de imágenes
import numpy as np  # Librería para operaciones numéricas
import matplotlib.pyplot as plt  # Librería para graficar las imágenes

# 🚩 Paso 1: Cargar la imagen
# Leemos la imagen original en escala de grises para trabajar en ella.
# La conversión a escala de grises facilita el análisis de texturas y sombras, ya que simplifica los colores a intensidades de píxel.
img = cv2.imread('tu_imagen.jpg', cv2.IMREAD_GRAYSCALE)

# Verificamos si la imagen fue cargada correctamente
if img is None:
    print("❌ Error: No se encontró la imagen. Asegúrate de que 'tu_imagen.jpg' esté en la carpeta.")
    exit()  # Finaliza el código si la imagen no se carga correctamente

# -----------------------------
# 🎯 Paso 2: Filtrado de texturas utilizando un filtro de suavizado (Blur)
# Los filtros de suavizado (blur) son útiles para eliminar detalles finos de la imagen, permitiendo resaltar texturas de baja frecuencia.
# Usamos un filtro gaussiano para suavizar la imagen, el cual difumina los píxeles cercanos y reduce el ruido en la imagen.
# La función cv2.GaussianBlur toma dos parámetros principales: la imagen de entrada y el tamaño del kernel.
blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Tamaño del kernel de 5x5 píxeles

# -----------------------------
# 🎯 Paso 3: Detección de bordes (enfoque en las texturas)
# Para resaltar las texturas de alta frecuencia, utilizamos el algoritmo de detección de bordes de Canny.
# Este algoritmo resalta los bordes más nítidos de las regiones en la imagen, lo cual es útil para identificar las texturas.
edges = cv2.Canny(img, 100, 200)  # Umbrales bajos y altos para la detección de bordes

# -----------------------------
# 🎯 Paso 4: Sombras - Realce de sombras
# Las sombras son áreas de la imagen con intensidad baja. Podemos intentar realzarlas usando un contraste adaptativo.
# Esto se logra mediante la función de ecualización del histograma, que mejora las áreas más oscuras.
equalized = cv2.equalizeHist(img)  # Ecualización de histograma para mejorar las sombras

# -----------------------------
# 🖼️ Paso 5: Visualizar los resultados
# Usamos matplotlib para visualizar las imágenes originales y los resultados del procesamiento.
# Mostramos la imagen original, la imagen con bordes detectados (texturas), la imagen suavizada (filtro) y la imagen con sombras mejoradas.
plt.figure(figsize=(12, 8))  # Define el tamaño de la figura.

# Imagen original
plt.subplot(2, 3, 1)  # Organiza el gráfico en una rejilla de 2x3, colocando la imagen original en la primera posición.
plt.imshow(img, cmap='gray')  # Muestra la imagen original en escala de grises.
plt.title('Imagen Original')  # Título de la imagen original
plt.axis('off')  # Elimina los ejes del gráfico

# Imagen suavizada (Blur)
plt.subplot(2, 3, 2)  # Coloca la imagen suavizada en la segunda posición.
plt.imshow(blurred, cmap='gray')  # Muestra la imagen suavizada para resaltar texturas de baja frecuencia.
plt.title('Imagen Suavizada (Blur)')  # Título de la imagen suavizada
plt.axis('off')  # Elimina los ejes del gráfico

# Detección de bordes (Texturas)
plt.subplot(2, 3, 3)  # Coloca la imagen de bordes en la tercera posición.
plt.imshow(edges, cmap='gray')  # Muestra los bordes detectados en la imagen para resaltar las texturas.
plt.title('Detección de Bordes (Texturas)')  # Título de la detección de bordes
plt.axis('off')  # Elimina los ejes del gráfico

# Imagen con sombras realzadas
plt.subplot(2, 3, 4)  # Coloca la imagen con sombras mejoradas en la cuarta posición.
plt.imshow(equalized, cmap='gray')  # Muestra la imagen con sombras mejoradas.
plt.title('Sombras Realzadas (Ecualización)')  # Título de la mejora de sombras
plt.axis('off')  # Elimina los ejes del gráfico

# Mostrar todas las imágenes procesadas en una ventana
plt.show()  # Muestra las imágenes con los diferentes resultados de procesamiento.
