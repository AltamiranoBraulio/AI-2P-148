# Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ---------------------------------------------
# 1. Cargar el conjunto de datos Iris
iris = datasets.load_iris()
X = iris.data[:, :2]  # Usamos solo las dos primeras características (Largo y Ancho del Sépalo)
y = iris.target  # Etiquetas de las tres especies de flores (0, 1, 2)

# ---------------------------------------------
# 2. Preprocesamiento de datos: Normalizamos las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Normalizamos las características

# ---------------------------------------------
# 3. Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# ---------------------------------------------
# 4. Crear el modelo SVM con núcleo RBF
svm_clf = SVC(kernel='rbf', C=1.0, gamma='scale')

# Entrenamos el modelo
svm_clf.fit(X_train, y_train)

# ---------------------------------------------
# 5. Evaluación del modelo
score = svm_clf.score(X_test, y_test)
print(f"Precisión del modelo SVM en datos de prueba: {score:.2f}")

# ---------------------------------------------
# 6. Predicción para un nuevo dato
nuevo_dato = np.array([[5.0, 3.5]])  # Largo del sépalo: 5.0 cm, Ancho del sépalo: 3.5 cm
nuevo_dato_scaled = scaler.transform(nuevo_dato)  # Normalizamos el nuevo dato
prediccion = svm_clf.predict(nuevo_dato_scaled)  # Predicción de la especie

# Mostrar el resultado de la predicción
especies = iris.target_names
print(f"El nuevo dato pertenece a la especie: {especies[prediccion][0]}")

# ---------------------------------------------
# 7. Visualización de la frontera de decisión
# Creamos una malla de puntos para graficar la frontera de decisión
x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

# Predicción sobre la malla para dibujar la frontera de decisión
Z = svm_clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Graficamos la frontera de decisión
plt.contourf(xx, yy, Z, alpha=0.8, cmap='coolwarm')

# Añadimos los puntos de entrenamiento
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=50, cmap='coolwarm', edgecolors='k')
plt.title("Frontera de decisión de SVM con núcleo RBF")
plt.xlabel("Largo del Sépalo (cm)")
plt.ylabel("Ancho del Sépalo (cm)")
plt.colorbar()
plt.show()
