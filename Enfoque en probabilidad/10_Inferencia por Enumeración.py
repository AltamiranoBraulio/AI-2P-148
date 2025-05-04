import itertools

# Definir las probabilidades condicionales para cada variable
# Probabilidades para la lluvia (Llueve)
prob_lluvia = {'Sí': 0.3, 'No': 0.7}

# Probabilidades de tráfico dadas las condiciones de lluvia
prob_trafico_dado_lluvia = {
    'Sí': {'Sí': 0.8, 'No': 0.2},  # Si llueve
    'No': {'Sí': 0.5, 'No': 0.5}   # Si no llueve
}

# Probabilidades de accidente dadas el tráfico y la lluvia
prob_accidente = {
    ('Sí', 'Sí'): 0.9,  # Lluvia y tráfico
    ('Sí', 'No'): 0.1,  # Lluvia y sin tráfico
    ('No', 'Sí'): 0.5,  # No lluvia y tráfico
    ('No', 'No'): 0.05  # No lluvia y sin tráfico
}

# Función para calcular la probabilidad de un accidente dado que hay tráfico y lluvia
def inferir_accidente(evidencia):
    """
    Realiza la inferencia por enumeración en una red bayesiana simple.

    evidencia: un diccionario con las observaciones dadas (en este caso, Tráfico y Llueve)
    """
    # Todos los estados posibles para las variables Lluvia y Tráfico
    estados_lluvia = ['Sí', 'No']
    estados_trafico = ['Sí', 'No']

    # Generamos todas las combinaciones posibles de Lluvia y Tráfico
    combinaciones = list(itertools.product(estados_lluvia, estados_trafico))
    
    probabilidad_total = 0
    
    for combinacion in combinaciones:
        lluvias, trafico = combinacion
        
        # Calcular la probabilidad total para cada combinación
        # Calcular la probabilidad de la lluvia
        prob_lluvia_ = prob_lluvia[lluvias]
        
        # Calcular la probabilidad del tráfico dado la lluvia
        prob_trafico_ = prob_trafico_dado_lluvia[lluvias][trafico]
        
        # Calcular la probabilidad del accidente dado lluvia y tráfico
        prob_accidente_ = prob_accidente[(lluvias, trafico)]
        
        # Multiplicamos las probabilidades
        prob_comb = prob_lluvia_ * prob_trafico_ * prob_accidente_
        
        # Sumar al total
        probabilidad_total += prob_comb
    
    return probabilidad_total

# Caso de inferencia: ¿Cuál es la probabilidad de un accidente dado que hay tráfico y lluvia?
evidencia = {'Tráfico': 'Sí', 'Llueve': 'Sí'}
probabilidad_accidente = inferir_accidente(evidencia)

# Mostrar el resultado
print(f"\nProbabilidad de que ocurra un accidente dado que hay tráfico y lluvia: {probabilidad_accidente:.4f}")
