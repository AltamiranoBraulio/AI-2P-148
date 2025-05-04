# Importamos la librería OpenCV para procesamiento de imágenes
import cv2  

# Importamos NumPy para trabajar con arreglos y realizar operaciones matemáticas
import numpy as np  

# ---------------------------
# PASO 1: CARGAR LA IMAGEN
# ---------------------------

# Cargamos la imagen desde disco en escala de grises
# Usamos cv2.IMREAD_GRAYSCALE para trabajar solo con intensidad (sin color)
image = cv2.imread('imagen_ejemplo.png', cv2.IMREAD_GRAYSCALE)

# ---------------------------
# PASO 2: SUAVIZAR LA IMAGEN
# ---------------------------

# Aplicamos un filtro Gaussiano para suavizar la imagen y reducir el ruido
# Esto ayuda a que la detección de bordes sea más precisa
# El kernel (5, 5) define el tamaño del filtro, y 0 es la desviación estándar
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

# ---------------------------
# PASO 3: DETECCIÓN DE BORDES
# ---------------------------

# Aplicamos el detector de bordes Canny
# Este paso detecta los contornos en la imagen
# Los parámetros 50 y 150 son los umbrales para definir qué se considera borde
# apertureSize=3 define el tamaño del filtro Sobel que se usa internamente
edges = cv2.Canny(blurred_image, 50, 150, apertureSize=3)

# ---------------------------
# PASO 4: DETECCIÓN DE LÍNEAS
# ---------------------------

# Usamos la transformada de Hough para detectar líneas rectas en la imagen
# Parámetros:
# - 1: resolución en píxeles para el parámetro rho (distancia)
# - np.pi / 180: resolución en radianes para el parámetro theta (ángulo)
# - 100: umbral de votos para considerar una línea
# - minLineLength=100: longitud mínima que debe tener una línea para ser detectada
# - maxLineGap=10: separación máxima entre puntos para considerarlos en la misma línea
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

# ---------------------------
# PASO 5: DIBUJAR LAS LÍNEAS
# ---------------------------

# Convertimos la imagen en gris a color BGR para poder dibujar líneas de colores
# Esto crea una copia de la imagen original para no modificar la fuente
output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Recorremos cada línea detectada y la dibujamos
for line in lines:
    # Extraemos las coordenadas (x1, y1) y (x2, y2) de la línea
    x1, y1, x2, y2 = line[0]

    # Dibujamos la línea sobre la imagen:
    # - (x1, y1) es el punto inicial y (x2, y2) es el punto final
    # - (0, 0, 255) es el color rojo en formato BGR
    # - 2 es el grosor de la línea
    cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# ---------------------------
# PASO 6: MOSTRAR RESULTADOS
# ---------------------------

# Mostramos la imagen resultante con las líneas etiquetadas
cv2.imshow('Líneas Etiquetadas', output_image)

# Esperamos a que el usuario presione una tecla para cerrar la ventana
cv2.waitKey(0)

# Cerramos todas las ventanas abiertas por OpenCV
cv2.destroyAllWindows()
