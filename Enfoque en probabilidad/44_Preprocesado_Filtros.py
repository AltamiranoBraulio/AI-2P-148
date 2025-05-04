import cv2  # Librería de visión por computadora OpenCV
import numpy as np  # Librería para manejo de arrays y matemáticas
import matplotlib.pyplot as plt  # Para mostrar imágenes de forma elegante

# 🚩 Leemos una imagen en escala de grises (más fácil para filtrado)
img = cv2.imread('tu_imagen.jpg', cv2.IMREAD_GRAYSCALE)

# 🔄 Verificamos que la imagen se haya leído correctamente
if img is None:
    print("❌ Error: Imagen no encontrada. Asegúrate que 'tu_imagen.jpg' está en la carpeta.")
    exit()

# --------------------
# 🎯 1) Filtro Suavizante (Gaussian Blur)
# Este filtro reduce el "ruido" de la imagen y suaviza los bordes
blurred = cv2.GaussianBlur(img, (9, 9), 0)  # (9,9) es el tamaño del filtro

# --------------------
# 🎯 2) Filtro Detector de Bordes (Sobel)
# El filtro Sobel resalta los bordes verticales y horizontales de la imagen

# Calculamos gradientes en dirección X (horizontal)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)

# Calculamos gradientes en dirección Y (vertical)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

# Combinamos ambos para obtener los bordes completos
edges = np.sqrt(sobelx**2 + sobely**2)
edges = np.uint8(edges / np.max(edges) * 255)  # Normalizamos para que sea de 0 a 255

# --------------------
# 🖼️ Mostramos las imágenes original, suavizada y con bordes

plt.figure(figsize=(12, 4))

# Imagen original
plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Imagen Original')
plt.axis('off')

# Imagen Suavizada
plt.subplot(1, 3, 2)
plt.imshow(blurred, cmap='gray')
plt.title('Filtro Suavizante (Blur)')
plt.axis('off')

# Imagen con Bordes Detectados
plt.subplot(1, 3, 3)
plt.imshow(edges, cmap='gray')
plt.title('Filtro de Bordes (Sobel)')
plt.axis('off')

plt.show()
