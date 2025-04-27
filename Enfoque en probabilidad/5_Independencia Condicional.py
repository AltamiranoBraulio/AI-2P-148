import random

# --- Probabilidades a priori y condicionadas ---
# Probabilidades de inicio de cada clima (a priori)
probabilidad_inicial = {
    "Soleado": 0.5,
    "Nublado": 0.3,
    "Lluvia": 0.2
}

# Probabilidades condicionadas basadas en el clima del día anterior
# Ejemplo: Si el clima fue "Soleado", la probabilidad de que sea "Soleado" de nuevo es del 0.6, etc.
probabilidad_condicional = {
    "Soleado": {"Soleado": 0.6, "Nublado": 0.3, "Lluvia": 0.1},
    "Nublado": {"Soleado": 0.2, "Nublado": 0.5, "Lluvia": 0.3},
    "Lluvia": {"Soleado": 0.1, "Nublado": 0.3, "Lluvia": 0.6}
}

# Función para simular el clima de un día dado el clima anterior
def clima_dia_anterior(clima_anterior):
    # Elegimos el clima del día siguiente basado en el clima anterior
    probabilidad = probabilidad_condicional[clima_anterior]
    
    # Generamos un número aleatorio entre 0 y 1
    r = random.random()
    
    # Determinamos el clima del siguiente día basado en las probabilidades
    suma_prob = 0
    for clima, prob in probabilidad.items():
        suma_prob += prob
        if r < suma_prob:
            return clima

# --- Simulación del clima por varios días ---
def simular_clima(dias):
    # Empezamos con un clima inicial elegido aleatoriamente
    clima_actual = random.choices(list(probabilidad_inicial.keys()), list(probabilidad_inicial.values()))[0]
    print(f"Clima del primer día: {clima_actual}")
    
    for dia in range(2, dias + 1):
        # Simulamos el clima del siguiente día
        clima_siguiente = clima_dia_anterior(clima_actual)
        print(f"Día {dia}: {clima_siguiente}")
        clima_actual = clima_siguiente

# --- Ejecución de la simulación para 10 días ---
simular_clima(10)
