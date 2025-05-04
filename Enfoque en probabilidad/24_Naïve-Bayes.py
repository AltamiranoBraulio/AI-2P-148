# -------------------------------------------
# 🌈 Clasificador de Mensajes Positivos o Negativos usando Naïve Bayes
# -------------------------------------------

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# -------------------------------------------
# 📝 Datos de entrenamiento: Mensajes y etiquetas
mensajes = [
    "Me encanta este producto",  # Positivo (1)
    "Es un excelente servicio",  # Positivo (1)
    "Muy mala experiencia",      # Negativo (0)
    "No me gustó para nada",     # Negativo (0)
    "Fantástico y rápido",       # Positivo (1)
    "Horrible, nunca volveré",   # Negativo (0)
]

# Etiquetas (1 = positivo, 0 = negativo)
etiquetas = [1, 1, 0, 0, 1, 0]

# -------------------------------------------
# 🧰 Convertir texto a números (Bolsa de Palabras)
vectorizador = CountVectorizer()

# Transforma los mensajes en una matriz de frecuencia de palabras
X = vectorizador.fit_transform(mensajes)

# -------------------------------------------
# 🔮 Crear el modelo Naïve Bayes
modelo = MultinomialNB()

# Entrenarlo con nuestros datos
modelo.fit(X, etiquetas)

# -------------------------------------------
# ✨ Nueva predicción
nuevo_mensaje = ["Me encantó el servicio, fue fantástico"]

# Convertirlo a números usando el mismo vectorizador
X_nuevo = vectorizador.transform(nuevo_mensaje)

# Predecir
prediccion = modelo.predict(X_nuevo)

# Mostrar resultado
print("🔎 Mensaje:", nuevo_mensaje[0])
print("✅ Clasificación:", "Positivo 😊" if prediccion[0] == 1 else "Negativo 😞")
