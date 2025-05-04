# 📚 Importamos el módulo random para generar números aleatorios
import random

# 🎲 Definimos las reglas de nuestra Gramática Probabilística Independiente del Contexto (PCFG)
# Cada regla es una tupla de la forma (Lado izquierdo, Lado derecho, probabilidad)
rules = [
    ("S", ["NP", "VP"], 1.0),  # Regla 1: S → NP VP con probabilidad 1.0
    ("NP", ["Det", "N"], 0.5),  # Regla 2: NP → Det N con probabilidad 0.5
    ("NP", ["Det", "Adj", "N"], 0.5),  # Regla 3: NP → Det Adj N con probabilidad 0.5
    ("VP", ["V", "NP"], 1.0),  # Regla 4: VP → V NP con probabilidad 1.0
    ("Det", ["el"], 0.5),  # Regla 5: Det → "el" con probabilidad 0.5
    ("Det", ["la"], 0.5),  # Regla 6: Det → "la" con probabilidad 0.5
    ("N", ["perro"], 0.5),  # Regla 7: N → "perro" con probabilidad 0.5
    ("N", ["gata"], 0.5),  # Regla 8: N → "gata" con probabilidad 0.5
    ("V", ["ladra"], 0.5),  # Regla 9: V → "ladra" con probabilidad 0.5
    ("V", ["duerme"], 0.5),  # Regla 10: V → "duerme" con probabilidad 0.5
    ("Adj", ["gris"], 1.0)  # Regla 11: Adj → "gris" con probabilidad 1.0
]

# 🧠 Función que selecciona aleatoriamente una regla para un símbolo no terminal
def choose_rule(non_terminal):
    # 🔎 Filtramos las reglas que aplican para el no terminal actual
    applicable_rules = [rule for rule in rules if rule[0] == non_terminal]
    
    # 🧮 Sumamos las probabilidades de las reglas que aplican
    total_probability = sum(rule[2] for rule in applicable_rules)
    
    # 🔀 Generamos un número aleatorio entre 0 y la probabilidad total
    random_choice = random.uniform(0, total_probability)
    
    # ⚡ Inicializamos la suma acumulada de probabilidades
    running_sum = 0
    
    # 🔁 Recorremos las reglas aplicables para encontrar cuál se selecciona
    for rule in applicable_rules:
        running_sum += rule[2]  # Sumamos la probabilidad de la regla actual
        
        # 🔍 Si el número aleatorio cae en el rango de esta regla, la seleccionamos
        if running_sum >= random_choice:
            return rule  # Devolvemos la regla seleccionada
    
    # 🔄 Si no se elige ninguna regla, devolvemos la última regla por defecto
    return applicable_rules[-1]

# 🧩 Función recursiva para generar una cadena a partir de un símbolo no terminal
def generate_string(symbol):
    # 🛑 Si el símbolo es un terminal (es decir, una palabra), lo devolvemos directamente
    if symbol.islower():  # Si el símbolo es una letra minúscula, es un terminal
        return symbol  # Devolvemos el símbolo tal cual
    
    else:
        # 🔄 Si el símbolo es un no terminal, aplicamos una regla para expandirlo
        rule = choose_rule(symbol)  # Elegimos una regla para expandir el no terminal
        
        # 📝 Extraemos el lado derecho de la regla elegida
        right_side = rule[1]  # El lado derecho de la regla es la lista de símbolos a expandir
        
        # 🔄 Aplicamos recursivamente la generación de cadenas a cada símbolo del lado derecho
        return ' '.join(generate_string(sym) for sym in right_side)  # Unimos las cadenas generadas para cada símbolo del lado derecho

# 🚀 Generamos una cadena empezando con el símbolo inicial "S"
print(generate_string("S"))  # Llamamos a la función para generar una cadena a partir del símbolo "S"
