import random
import re
from collections import defaultdict

# Corpus de ejemplo
corpus = """
Me gusta programar en Python.
Python es un lenguaje muy versátil.
Me encanta aprender nuevos lenguajes de programación.
"""

# Preprocesamiento: eliminar puntuación y poner todo en minúsculas
corpus = re.sub(r'[^\w\s]', '', corpus.lower())

# Tokenización: dividir el corpus en palabras
words = corpus.split()

# Crear un diccionario de bigramas
bigrams = defaultdict(list)

for i in range(len(words) - 1):
    bigrams[words[i]].append(words[i + 1])

# Función para generar una secuencia de texto utilizando los bigramas
def generate_sentence(start_word, length=10):
    current_word = start_word
    sentence = [current_word]
    
    for _ in range(length - 1):
        next_word = random.choice(bigrams[current_word]) if current_word in bigrams else '.'
        sentence.append(next_word)
        current_word = next_word
        if current_word == '.':
            break
    
    return ' '.join(sentence)

# Probar la generación de texto
start_word = "me"
generated_sentence = generate_sentence(start_word, length=10)
print(f"Frase generada: {generated_sentence}")
