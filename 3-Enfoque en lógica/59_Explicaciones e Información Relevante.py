# Importamos pandas para manejar datos en forma de tabla
import pandas as pd

# Importamos numpy para cálculos numéricos
import numpy as np

# Importamos un Árbol de Decisión como modelo explicativo
from sklearn.tree import DecisionTreeClassifier

# Importamos una función para visualizar la importancia de las características
from sklearn.tree import export_text

# Creamos un conjunto de datos simple para clasificar frutas
# Cada fruta tiene: Color (0=verde, 1=rojo), Tamaño (cm), Peso (g)
data = {
    'Color': [0, 1, 0, 1, 0],  # 0=verde, 1=rojo
    'Tamaño': [5, 6, 5, 7, 4],  # Tamaño en cm
    'Peso': [100, 150, 90, 200, 80],  # Peso en gramos
}

# Creamos las etiquetas de cada fruta (0=Manzana, 1=Sandía)
labels = [0, 1, 0, 1, 0]  # Etiquetas: Manzana o Sandía

# Convertimos los datos en un DataFrame para manipularlos como tabla
df = pd.DataFrame(data)

# Creamos el modelo de Árbol de Decisión
model = DecisionTreeClassifier()

# Entrenamos el modelo usando los datos y las etiquetas
model.fit(df, labels)

# Ahora vamos a hacer una predicción para una nueva fruta desconocida
# Nueva fruta: Color=rojo (1), Tamaño=6cm, Peso=160g
nueva_fruta = np.array([[1, 6, 160]])  # Definimos la nueva muestra

# Hacemos la predicción usando el modelo entrenado
prediccion = model.predict(nueva_fruta)

# Mostramos la predicción (0=Manzana, 1=Sandía)
print("Predicción para la nueva fruta (0=Manzana, 1=Sandía):", prediccion[0])

# 🔥 Ahora viene lo importante: explicar la decisión del modelo
# Usamos export_text para imprimir el árbol de decisión como texto explicativo
explicacion = export_text(model, feature_names=list(df.columns))

# Mostramos la explicación completa del árbol
print("\nExplicación del modelo (Árbol de Decisión):\n")
print(explicacion)

# 🎯 Extra: Mostramos la relevancia (importancia) de cada atributo
importancias = model.feature_importances_

# Recorremos cada característica para mostrar su relevancia numérica
print("\nInformación Relevante (Importancia de cada atributo):")
for nombre, importancia in zip(df.columns, importancias):
    print(f"- {nombre}: {importancia:.2f}")  # Mostramos con 2 decimales
