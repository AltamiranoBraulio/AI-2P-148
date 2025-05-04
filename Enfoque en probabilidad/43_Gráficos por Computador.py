# 📚 Importamos librerías esenciales para este gráfico computacional

import numpy as np  # NumPy nos permite manejar cálculos matemáticos con arreglos de datos (arrays), ideal para operaciones vectoriales
import matplotlib.pyplot as plt  # Matplotlib es una librería para graficar, aquí usamos su módulo pyplot para gráficos
from mpl_toolkits.mplot3d import Axes3D  # Esta herramienta dentro de matplotlib nos permite crear gráficos en 3D

# ----------------------------------------------------
# 🌐 Creamos los datos matemáticos que representan una esfera en 3D

# Creamos un rango de valores para el ángulo "theta" (ángulo vertical)
# Este va desde 0 hasta π (180 grados), cubriendo del polo sur al polo norte de la esfera
theta = np.linspace(0, np.pi, 100)  # Creamos 100 divisiones para mayor resolución

# Creamos un rango de valores para el ángulo "phi" (ángulo horizontal)
# Este va desde 0 hasta 2π (360 grados), girando completamente alrededor de la esfera
phi = np.linspace(0, 2 * np.pi, 100)  # También 100 divisiones para que quede bien suave

# np.meshgrid toma esos valores de theta y phi y genera una cuadrícula (malla) de coordenadas
# Esto es necesario para poder calcular cada punto (x, y, z) de la superficie de la esfera
theta, phi = np.meshgrid(theta, phi)  # Ahora tenemos una matriz 2D de ángulos

# Aquí usamos las fórmulas matemáticas para convertir coordenadas esféricas a cartesianas:
# x = sin(theta) * cos(phi)
# y = sin(theta) * sin(phi)
# z = cos(theta)
# Estas fórmulas colocan cada punto en su posición 3D correcta sobre la esfera
x = np.sin(theta) * np.cos(phi)  # Coordenadas X de cada punto de la esfera
y = np.sin(theta) * np.sin(phi)  # Coordenadas Y de cada punto
z = np.cos(theta)               # Coordenadas Z (altura)

# ----------------------------------------------------
# 💡 Simulamos la iluminación sobre la esfera para que se perciba volumen y profundidad

# Definimos la dirección de la luz como un vector 3D
# En este caso, la luz viene de la esquina superior derecha (0.5, 0.5, 1)
light_dir = np.array([0.5, 0.5, 1])

# Normalizamos el vector de luz para que tenga longitud 1 (esto es importante en matemáticas vectoriales)
# Así evitamos que la intensidad sea afectada por el tamaño del vector
light_dir = light_dir / np.linalg.norm(light_dir)  # np.linalg.norm calcula la magnitud del vector

# Ahora queremos calcular cuánta luz recibe cada punto de la esfera
# Para eso, usamos el "producto punto" entre la normal del punto (x, y, z) y la dirección de la luz
# Este producto punto nos da un valor: 
# - Alto si el punto está mirando hacia la luz (brillante)
# - Bajo o cero si el punto está en sombra

# Primero, apilamos los valores x, y, z en un array que represente las normales (vectores que apuntan hacia afuera)
# axis=-1 significa que ponemos x, y, z en la última dimensión para que cada punto tenga sus 3 coordenadas
normals = np.stack((x, y, z), axis=-1)  # Ahora tenemos un array donde cada punto tiene su vector normal

# Hacemos el producto punto entre cada normal y la dirección de la luz
# Esto nos da la "intensidad" de luz para cada punto (escalar entre 0 y 1)
intensity = np.dot(normals, light_dir)  # np.dot hace el cálculo en todos los puntos de la esfera

# Aseguramos que las intensidades no sean negativas
# Si un punto está totalmente en sombra (producto punto negativo), lo ponemos a 0
intensity = np.clip(intensity, 0, 1)  # np.clip limita los valores entre 0 y 1

# ----------------------------------------------------
# 🎨 Finalmente, graficamos la esfera con sus colores simulando luz y sombra

# Creamos una figura para el gráfico 3D
# figsize define el tamaño en pulgadas (ancho x alto)
fig = plt.figure(figsize=(8, 8))

# Agregamos un sistema de ejes 3D a la figura
# 111 significa 1 fila, 1 columna, posición 1 (es decir, un solo gráfico)
ax = fig.add_subplot(111, projection='3d')  # proyección en 3D

# Usamos ax.plot_surface para graficar la superficie de la esfera
# Pasamos las coordenadas x, y, z para que dibuje cada punto en el espacio 3D
# facecolors define el color de cada punto basado en su intensidad de luz
# cmap='viridis' es un mapa de color bonito que va de azul oscuro a verde y amarillo
ax.plot_surface(
    x, y, z, 
    facecolors=plt.cm.viridis(intensity),  # Mapeamos la intensidad de luz al color
    rstride=1, cstride=1,  # Pasos entre filas y columnas (más bajo = más suave)
    antialiased=True,  # Suaviza los bordes para que se vea mejor
    linewidth=0  # No dibuja líneas negras entre cada punto, solo color
)

# Quitamos los ejes para que el gráfico se vea limpio (sin números ni líneas)
ax.set_axis_off()

# Agregamos un título arriba del gráfico
plt.title('🪐 Esfera con Luz y Sombra (Percepción Gráfica)', fontsize=16)

# Mostramos el gráfico en pantalla
plt.show()
