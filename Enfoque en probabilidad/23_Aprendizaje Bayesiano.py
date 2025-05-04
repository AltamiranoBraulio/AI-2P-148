# Importamos la librería NumPy, que es básica en Python para trabajar con matrices y vectores numéricos
import numpy as np

# Importamos GaussianNB, que es el clasificador de Naive Bayes para datos que siguen una distribución normal (gaussiana)
from sklearn.naive_bayes import GaussianNB

# -----------------------------
# 📝 Datos de entrenamiento: cada fila representa un animal con dos características:
# [Peso (en kilogramos), Altura (en centímetros)]

# Creamos un arreglo (matriz) con los datos de ejemplo
X = np.array([
    [4, 30],   # Primer animal: Peso 4kg, Altura 30cm (es un gato)
    [5, 25],   # Segundo animal: Peso 5kg, Altura 25cm (también gato)
    [30, 60],  # Tercer animal: Peso 30kg, Altura 60cm (es un perro)
    [25, 55],  # Cuarto animal: Peso 25kg, Altura 55cm (otro perro)
])

# Etiquetas que indican la clase de cada animal
# 0 significa "Gato" y 1 significa "Perro"
y = np.array([0, 0, 1, 1])  # Los dos primeros son gatos (0), los dos últimos son perros (1)

# -----------------------------
# 🔮 Creamos el modelo Bayesiano
# GaussianNB es un clasificador que usa el Teorema de Bayes bajo la suposición de que los datos siguen una distribución Gaussiana
modelo = GaussianNB()

# Entrenamos (ajustamos) el modelo usando los datos de entrada (X) y sus respectivas etiquetas (y)
# Aquí el modelo aprende las "reglas" que le permitirán clasificar nuevos datos
modelo.fit(X, y)

# -----------------------------
# 🐾 Ahora vamos a predecir la clase de un nuevo animal
# Definimos un nuevo ejemplo con peso 6kg y altura 28cm
# La pregunta es: ¿será un gato (0) o un perro (1)?
nuevo = np.array([[6, 28]])  # Nota: el doble corchete [[]] es porque scikit-learn espera una matriz, no un vector

# Usamos el modelo entrenado para predecir la clase de este nuevo ejemplo
prediccion = modelo.predict(nuevo)  # Esto devuelve un array con la predicción (por ejemplo, [0] o [1])

# Mostramos el resultado en pantalla
# Si la predicción es 1, imprimimos "Perro 🐶", si es 0, imprimimos "Gato 🐱"
print("Predicción:", "Perro 🐶" if prediccion[0] == 1 else "Gato 🐱")
