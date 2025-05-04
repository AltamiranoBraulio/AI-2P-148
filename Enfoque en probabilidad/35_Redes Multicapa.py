from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# -----------------------------
# 1. Cargar el dataset (imágenes de dígitos 0-9)
# -----------------------------
digits = load_digits()

# Mostrar una imagen de ejemplo
plt.gray()
plt.matshow(digits.images[0])
plt.show()

# -----------------------------
# 2. Preparar datos
# -----------------------------
# a) Características (imagenes aplanadas)
X = digits.data

# b) Etiquetas (números reales 0-9)
y = digits.target

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# -----------------------------
# 3. Crear el modelo MLP
# -----------------------------
# Red con 2 capas ocultas: 100 y 50 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(100, 50), 
                    activation='relu', 
                    solver='adam', 
                    max_iter=500)

# -----------------------------
# 4. Entrenar la red
# -----------------------------
mlp.fit(X_train, y_train)

# -----------------------------
# 5. Evaluar la red
# -----------------------------
predictions = mlp.predict(X_test)

# Mostrar métricas
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
