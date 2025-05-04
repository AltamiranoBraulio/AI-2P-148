import re  # Usamos expresiones regulares para la detección de patrones en las frases

# Definimos un conjunto de reglas de gramática causal
# Estas reglas definen cómo se forma una relación causal en nuestras frases

# Una relación causal básica en la gramática será de tipo "Si X, entonces Y"
reglas_causales = [
    r"Si\s([a-zA-Z\s]+),\sentonces\s([a-zA-Z\s]+)",  # Regla para "Si X, entonces Y"
    r"([a-zA-Z\s]+),\spor\slotanto\s([a-zA-Z\s]+)"    # Regla para "X, por lo tanto Y"
]

# La función principal que analiza una lista de frases en busca de relaciones causales
def analizar_causalidad(frases):
    # Iteramos sobre cada frase que tenemos
    for frase in frases:
        # Tratamos de encontrar una relación causal según nuestras reglas
        for regla in reglas_causales:
            # Usamos la función `re.search` para buscar la expresión regular en la frase
            match = re.search(regla, frase)
            if match:  # Si encontramos un patrón causal
                # Imprimimos el patrón causal encontrado
                print(f"Relación causal encontrada: {frase}")
                print(f"Causa: {match.group(1)}")
                print(f"Consecuencia: {match.group(2)}\n")

# Lista de frases para analizar
frases = [
    "Si llueve, entonces me mojo.",
    "El sol brilla, por lo tanto hace calor.",
    "Si estudio mucho, entonces aprobaré el examen.",
    "Me caí, por lo tanto me lastimé."
]

# Llamamos a la función de análisis
analizar_causalidad(frases)

# Explicación:
# - La función `re.search` trata de encontrar un patrón que coincida con las reglas definidas.
# - Si una frase tiene una coincidencia, la función extrae la causa y la consecuencia y las imprime.
# - Estamos buscando frases que tengan una relación de "causa-efecto" utilizando dos tipos de estructuras comunes en causalidad.
