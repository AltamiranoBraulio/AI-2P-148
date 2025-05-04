# 🔶 Importación de las librerías necesarias

import cv2  # Librería OpenCV para procesamiento de imágenes
import numpy as np  # Librería para operaciones numéricas, necesaria para manejar matrices
import matplotlib.pyplot as plt  # Librería para graficar imágenes de manera sencilla

# 🚩 Paso 1: Cargar la imagen en escala de grises
# Leemos la imagen de un archivo, en este caso 'tu_imagen.jpg', y la convertimos a escala de grises.
# La función cv2.imread recibe como parámetros el nombre del archivo y el modo de lectura.
# cv2.IMREAD_GRAYSCALE convierte la imagen a una sola capa de intensidad (escala de grises).
img = cv2.imread('tu_imagen.jpg', cv2.IMREAD_GRAYSCALE)

# Verificamos si la imagen fue cargada correctamente
# Si no se puede leer la imagen (por ejemplo, si no existe el archivo), se imprimirá un mensaje de error y se termina el programa.
if img is None:
    print("❌ Error: No se encontró la imagen. Asegúrate que 'tu_imagen.jpg' esté en la carpeta.")
    exit()  # Finaliza la ejecución del código si no se encuentra la imagen

# -----------------------------
# 🎯 Paso 2: Detección de Aristas (Edge Detection) con el algoritmo Canny
# El algoritmo Canny es uno de los más populares para detectar bordes en imágenes.
# Recibe dos parámetros que definen el umbral bajo (threshold1) y el umbral alto (threshold2)
# Para cada píxel, el algoritmo detecta los bordes dependiendo de los valores de intensidad.
edges = cv2.Canny(img, threshold1=100, threshold2=200)

# -----------------------------
# 🎯 Paso 3: Segmentación usando umbral simple (Thresholding)
# El thresholding convierte la imagen en una versión binaria (blanco y negro).
# Los píxeles cuya intensidad sea mayor al valor de umbral (127) se convierten en blanco (255),
# mientras que los píxeles con valores inferiores se convierten en negro (0).
# La función cv2.threshold devuelve el valor del umbral y la imagen segmentada.
ret, segmented = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# -----------------------------
# 🖼️ Paso 4: Mostrar los resultados en 3 subgráficos usando matplotlib
# Usamos matplotlib para visualizar las imágenes de manera sencilla.
# Se crea una figura con un tamaño específico para mostrar las imágenes de forma organizada.
plt.figure(figsize=(12, 4))  # La figura tendrá un tamaño de 12x4 pulgadas.

# Imagen original
# Mostramos la imagen original en escala de grises (la primera columna).
# Utilizamos cmap='gray' para que la imagen se muestre en escala de grises.
# plt.axis('off') elimina los ejes alrededor de la imagen.
plt.subplot(1, 3, 1)  # Organiza el gráfico en una fila con 3 columnas, y coloca la imagen original en la primera columna.
plt.imshow(img, cmap='gray')  # Muestra la imagen original en escala de grises.
plt.title('Imagen Original')  # Título de la imagen original
plt.axis('off')  # Elimina los ejes del gráfico

# Imagen con aristas detectadas
# Mostramos la imagen con las aristas detectadas usando Canny (la segunda columna).
plt.subplot(1, 3, 2)  # Coloca esta imagen en la segunda columna.
plt.imshow(edges, cmap='gray')  # Muestra las aristas detectadas.
plt.title('Detección de Aristas (Canny)')  # Título de la imagen de aristas detectadas.
plt.axis('off')  # Elimina los ejes del gráfico

# Imagen segmentada
# Mostramos la imagen segmentada (la tercera columna) que está en blanco y negro.
plt.subplot(1, 3, 3)  # Coloca esta imagen en la tercera columna.
plt.imshow(segmented, cmap='gray')  # Muestra la imagen segmentada.
plt.title('Segmentación (Threshold)')  # Título de la imagen segmentada.
plt.axis('off')  # Elimina los ejes del gráfico

# Finalmente, mostramos todas las imágenes usando plt.show(), que abre una ventana con los resultados.
plt.show()  # Muestra todas las imágenes en la pantalla.
