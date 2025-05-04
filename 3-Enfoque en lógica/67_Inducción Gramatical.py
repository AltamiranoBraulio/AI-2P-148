# Importamos las bibliotecas necesarias
import random  # Para crear ejemplos aleatorios
import re  # Para usar expresiones regulares al crear reglas

# Definimos un conjunto de ejemplos (frases)
# Estos ejemplos son secuencias de palabras que representan patrones que el sistema intentará aprender
examples = [
    "el perro corre",
    "la gata duerme",
    "el gato juega",
    "el perro duerme",
    "la vaca corre",
    "el caballo come"
]

# La función para generar una regla de la gramática a partir de un ejemplo dado
def generate_rule(example):
    """
    Esta función recibe una cadena de texto (un ejemplo de la gramática),
    y genera una regla simple basada en la estructura de la cadena.
    """
    # Descomponemos la cadena en palabras usando espacios como delimitadores
    words = example.split(" ")
    
    # Definimos un patrón para la regla, por ejemplo:
    # Asumimos que la primera palabra es el artículo, la segunda es el sustantivo, 
    # y la tercera es el verbo. Vamos a generar la regla:
    
    # Ejemplo de forma de la regla: "Artículo + Sustantivo + Verbo"
    rule = f"({words[0]}) + ({words[1]}) + ({words[2]})"
    
    # Devolvemos la regla generada
    return rule

# Ahora definimos la función para hacer inducción gramatical
def inductive_learning(examples):
    """
    Esta función toma una lista de ejemplos, y genera reglas gramaticales 
    inductivas para aprender patrones comunes en los ejemplos dados.
    """
    rules = []  # Lista que almacenará las reglas generadas
    
    # Recorremos todos los ejemplos y generamos reglas para cada uno
    for example in examples:
        rule = generate_rule(example)  # Generamos una regla para cada ejemplo
        rules.append(rule)  # Agregamos la regla a la lista
    
    # Devolvemos todas las reglas generadas
    return rules

# Ejecutamos la inducción gramatical sobre los ejemplos
learned_rules = inductive_learning(examples)

# Mostramos las reglas aprendidas
print("Reglas gramaticales aprendidas:")
for rule in learned_rules:
    print(rule)

# Ahora generamos una nueva frase usando una de las reglas aprendidas de forma aleatoria
def generate_sentence(rule):
    """
    Esta función genera una nueva oración utilizando una regla gramatical
    basada en las partes que definimos previamente (Artículo, Sustantivo, Verbo).
    """
    # Definimos las posibles palabras para cada categoría
    articles = ["el", "la"]
    nouns = ["perro", "gato", "vaca", "caballo", "gata"]
    verbs = ["corre", "juega", "duerme", "come"]
    
    # Partimos la regla para extraer la estructura (Artículo + Sustantivo + Verbo)
    # Suponemos que la estructura tiene el formato: "(Artículo) + (Sustantivo) + (Verbo)"
    structure = rule.split(" + ")
    
    # Generamos una nueva frase basada en la estructura de la regla
    sentence = ""
    
    for part in structure:
        if "Artículo" in part:
            sentence += random.choice(articles) + " "
        elif "Sustantivo" in part:
            sentence += random.choice(nouns) + " "
        elif "Verbo" in part:
            sentence += random.choice(verbs) + " "
    
    # Devolvemos la frase generada
    return sentence.strip()

# Generamos y mostramos una nueva oración aleatoria basada en las reglas aprendidas
print("\nGenerando una nueva oración basada en las reglas aprendidas:")
new_sentence = generate_sentence(random.choice(learned_rules))
print(new_sentence)
