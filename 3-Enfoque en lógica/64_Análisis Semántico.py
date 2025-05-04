# Primero, importamos la librería TextBlob para el análisis semántico del texto
from textblob import TextBlob  # TextBlob facilita el análisis de texto en términos de polaridad y subjetividad

# Definimos un texto de ejemplo para analizar
texto = """
La inteligencia artificial es una de las tecnologías más fascinantes que está cambiando el mundo.
A pesar de sus desafíos, el potencial de la IA es increíble y puede traer enormes beneficios a la humanidad.
"""

# Creamos un objeto TextBlob con el texto proporcionado
# TextBlob permite realizar varios análisis, entre ellos la polaridad y subjetividad
blob = TextBlob(texto)

# Vamos a imprimir el texto original para tenerlo de referencia
print(f"Texto original:\n{texto}\n")

# Ahora analizamos la **polaridad** del texto (sentimiento)
# La polaridad puede estar entre -1 (negativo) y 1 (positivo), donde:
# -1 significa un sentimiento negativo, 1 es un sentimiento positivo, y 0 es neutral
polaridad = blob.sentiment.polarity
print(f"Polaridad del texto: {polaridad}")

# Ahora, determinamos el sentimiento en términos simples:
if polaridad > 0:
    print("Sentimiento: Positivo")
elif polaridad < 0:
    print("Sentimiento: Negativo")
else:
    print("Sentimiento: Neutral")

# También podemos analizar la **subjetividad**, que mide qué tan subjetivo es el texto
# Un valor de 1 significa que el texto es completamente subjetivo, y 0 significa completamente objetivo
subjetividad = blob.sentiment.subjectivity
print(f"Subjetividad del texto: {subjetividad}")

# Si la subjetividad es mayor a 0.5, el texto se considera subjetivo (opiniones, emociones, etc.)
# Si es menor a 0.5, se considera objetivo (hechos, información verificable)
if subjetividad > 0.5:
    print("El texto tiene un alto grado de subjetividad (opinión, emoción).")
else:
    print("El texto es más objetivo (información, hechos).")

# Ahora vamos a hacer un análisis sobre algunas palabras importantes en el texto
# Utilizamos el análisis semántico para obtener las palabras claves o "sustantivos"
sustantivos = blob.noun_phrases
print(f"Sustantivos clave en el texto: {sustantivos}")

# Por último, podemos realizar una simple corrección ortográfica si el texto contiene errores
# Usamos TextBlob para verificar la ortografía y sugerir correcciones
texto_incorrecto = "La inteligencia artifisial es increible."
texto_corregido = TextBlob(texto_incorrecto).correct()
print(f"Texto corregido: {texto_corregido}")

# Para ver la corrección de forma más clara, imprimimos las diferencias
print(f"Texto original con errores: {texto_incorrecto}")
print(f"Texto después de corrección: {texto_corregido}")
