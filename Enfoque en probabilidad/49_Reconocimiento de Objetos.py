# 🔶 Importación de las librerías necesarias
import cv2  # OpenCV para procesamiento de imágenes
import matplotlib.pyplot as plt  # Para mostrar la imagen y resultados

# 🚩 Paso 1: Cargar la imagen y el clasificador HOG
# Cargamos la imagen que contiene los objetos a detectar.
# En este caso, usamos una imagen de ejemplo que contiene personas.
img = cv2.imread('tu_imagen_con_personas.jpg')

# Verificamos si la imagen fue cargada correctamente
if img is None:
    print("❌ Error: No se encontró la imagen. Asegúrate de que 'tu_imagen_con_personas.jpg' esté en la carpeta.")
    exit()

# 🚩 Paso 2: Inicialización del detector HOG de OpenCV
# OpenCV viene con un detector HOG pre-entrenado para la detección de personas.
hog = cv2.HOGDescriptor()  # Creamos un descriptor HOG
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  # Usamos el detector pre-entrenado

# 🚩 Paso 3: Detectar personas en la imagen
# La función detectMultiScale se utiliza para detectar objetos en la imagen.
# Devuelve una lista de rectángulos que contienen las personas detectadas.
# El parámetro 'scale' ayuda a ajustar la detección a diferentes tamaños de personas.
# 'winStride' y 'padding' ajustan la precisión de la detección.
boxes, weights = hog.detectMultiScale(img, winStride=(8, 8), padding=(8, 8), scale=1.05)

# 🚩 Paso 4: Dibujar los resultados en la imagen
# Dibujamos un rectángulo alrededor de cada persona detectada.
for (x, y, w, h) in boxes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Dibuja el rectángulo en color verde

# 🚩 Paso 5: Mostrar la imagen con los objetos detectados
# Convertimos la imagen a RGB para poder mostrarla correctamente con matplotlib.
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Mostramos la imagen con los objetos detectados
plt.imshow(img_rgb)
plt.title('Detección de Personas con HOG')  # Título
plt.axis('off')  # Eliminar los ejes
plt.show()  # Mostrar la imagen
