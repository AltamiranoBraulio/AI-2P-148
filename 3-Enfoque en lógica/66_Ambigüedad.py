import nltk
from nltk.corpus import wordnet as wn

# Descargamos los recursos de NLTK si no se tienen previamente
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Frase ambigua
frase = "El banco está cerca del río"

# Tokenizamos la frase (dividimos la frase en palabras)
tokens = nltk.word_tokenize(frase)

# Etiquetamos las palabras con sus categorías gramaticales (part of speech tagging)
etiquetas = nltk.pos_tag(tokens)

# Función para obtener los significados posibles de una palabra ambigua
def obtener_significados(palabra):
    # Usamos WordNet para obtener los sinónimos y significados de la palabra
    sinonimos = wn.synsets(palabra)
    
    # Si no hay sinónimos, devolvemos una lista vacía
    if not sinonimos:
        return ["Sin significados disponibles."]
    
    # Extraemos los nombres de los primeros 5 significados
    significados = [synset.name() for synset in sinonimos[:5]]
    return significados

# Analizar las palabras ambiguas en la frase
for palabra, etiqueta in etiquetas:
    # Solo analizamos sustantivos, ya que en este ejemplo la ambigüedad suele estar en sustantivos
    if etiqueta in ['NN', 'NNS', 'NNP', 'NNPS']:
        # Obtenemos los significados de la palabra ambigua
        significados = obtener_significados(palabra.lower())  # Convertimos a minúsculas para uniformidad
        print(f"Palabra: {palabra}")
        print(f"Posibles significados: {significados}")
        print("")

# Explicación del código:
# 1. Primero, tokenizamos la frase usando nltk.word_tokenize para dividirla en palabras.
# 2. Luego, etiquetamos gramaticalmente cada palabra usando nltk.pos_tag. Esto nos da información sobre si la palabra es un sustantivo, verbo, adjetivo, etc.
# 3. Luego, buscamos palabras ambiguas (sustantivos en este caso) y usamos WordNet para obtener los significados posibles de cada palabra.
# 4. Finalmente, mostramos los significados y explicamos la ambigüedad de cada palabra.
