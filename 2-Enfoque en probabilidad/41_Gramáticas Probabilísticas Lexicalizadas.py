import random

# 📚 Definimos las reglas gramaticales lexicalizadas con las probabilidades correspondientes
# Cada regla ahora tiene una palabra (terminal) específica en el lado derecho
lexicalized_rules = [
    ("S", ["NP", "VP"], 1.0),  # S → NP VP con probabilidad 1.0
    ("NP", ["Det", "N"], 0.5),  # NP → Det N con probabilidad 0.5
    ("NP", ["Det", "Adj", "N"], 0.5),  # NP → Det Adj N con probabilidad 0.5
    ("VP", ["V", "NP"], 1.0),  # VP → V NP con probabilidad 1.0
    ("Det", ["el"], 0.4),  # Det → "el" con probabilidad 0.4
    ("Det", ["la"], 0.6),  # Det → "la" con probabilidad 0.6
    ("N", ["perro"], 0.5),  # N → "perro" con probabilidad 0.5
    ("N", ["gata"], 0.5),  # N → "gata" con probabilidad 0.5
    ("V", ["ladra"], 0.5),  # V → "ladra" con probabilidad 0.5
    ("V", ["duerme"], 0.5),  # V → "duerme" con probabilidad 0.5
    ("Adj", ["gris"], 1.0)  # Adj → "gris" con probabilidad 1.0
]

# 🧠 Función para elegir una regla aleatoria de acuerdo con su probabilidad
def choose_rule(non_terminal):
    # Filtramos las reglas que corresponden al símbolo no terminal
    applicable_rules = [rule for rule in lexicalized_rules if rule[0] == non_terminal]
    
    # Calculamos la probabilidad total de todas las reglas aplicables
    total_probability = sum(rule[2] for rule in applicable_rules)
    
    # Generamos un número aleatorio entre 0 y la probabilidad total
    random_choice = random.uniform(0, total_probability)
    
    # Suma acumulativa de las probabilidades
    running_sum = 0
    
    # Iteramos sobre las reglas y seleccionamos una basada en la probabilidad acumulada
    for rule in applicable_rules:
        running_sum += rule[2]
        if running_sum >= random_choice:
            return rule
    
    # Si no se encuentra ninguna regla, devolvemos la última regla por defecto
    return applicable_rules[-1]

# 🧩 Función recursiva para generar una cadena a partir de un símbolo no terminal
def generate_string(symbol):
    # Si el símbolo es un terminal (es decir, una palabra), lo devolvemos tal cual
    if symbol.islower():  # Si el símbolo es minúscula, es un terminal
        return symbol
    
    # Si el símbolo es un no terminal, elegimos una regla para expandirlo
    rule = choose_rule(symbol)
    
    # Extraemos el lado derecho de la regla elegida
    right_side = rule[1]
    
    # Aplicamos recursivamente la generación de cadenas a cada símbolo del lado derecho
    return ' '.join(generate_string(sym) for sym in right_side)

# 🚀 Generamos una oración empezando con el símbolo inicial "S"
print(generate_string("S"))
