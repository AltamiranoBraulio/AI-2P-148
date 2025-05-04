# 📚 Importamos librerías necesarias
from collections import defaultdict  # defaultdict nos permite crear diccionarios con valores por defecto
import random  # random lo usaremos para elegir traducciones aleatorias (cuando hay varias opciones)

# 🔤 Nuestro pequeño corpus paralelo (frases en inglés y sus equivalentes en español)
# Cada par es una frase en inglés y su traducción en español
parallel_corpus = [
    ("hello", "hola"),
    ("good morning", "buenos días"),
    ("how are you", "cómo estás"),
    ("thank you", "gracias"),
    ("good night", "buenas noches"),
    ("see you", "nos vemos"),
    ("i love you", "te amo"),
]

# 📊 Creamos un diccionario especial para almacenar las posibles traducciones
# defaultdict con listas: si una palabra no existe aún, se crea una lista vacía automáticamente
translation_table = defaultdict(list)

# 🔄 Llenamos la tabla de traducciones usando los pares del corpus
for en, es in parallel_corpus:  # Recorremos cada par (en: inglés, es: español)
    translation_table[en].append(es)  # Añadimos la traducción española a la lista de opciones del inglés

# 🔎 Definimos una función para traducir frases usando nuestro "modelo estadístico"
def translate(sentence):
    # 👇 Paso 1: Convertimos toda la frase a minúsculas y la separamos en palabras
    words = sentence.lower().split()  # .lower() hace minúsculas, .split() separa por espacios
    translated = []  # Lista vacía donde guardaremos las traducciones

    # 🔄 Paso 2: Recorremos palabra por palabra
    for word in words:
        # 🔍 Verificamos si la palabra está en nuestra tabla de traducciones
        if word in translation_table:
            # ✅ Si la palabra existe en el diccionario, escogemos aleatoriamente una traducción
            translated.append(random.choice(translation_table[word]))  # random.choice elige una opción al azar
        else:
            # ❓ Si la palabra no existe, la marcamos como desconocida poniéndola entre corchetes
            translated.append(f"[{word}]")

    # 📝 Paso 3: Unimos todas las palabras traducidas en una sola cadena separada por espacios
    return " ".join(translated)

# 🚀 Probamos nuestro sistema con algunas frases conocidas y desconocidas
print("🔤 Traducciones Automáticas:")  # Título que indica que se mostrarán traducciones
print("hello  ➡️", translate("hello"))  # Traduce "hello"
print("good night  ➡️", translate("good night"))  # Traduce "good night"
print("i love you  ➡️", translate("i love you"))  # Traduce "i love you"
print("thank you  ➡️", translate("thank you"))  # Traduce "thank you"
print("bye  ➡️", translate("bye"))  # Traduce "bye" (palabra que no está en nuestro corpus)
