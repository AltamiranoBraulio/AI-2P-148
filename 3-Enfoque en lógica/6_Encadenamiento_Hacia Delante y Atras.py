# Definimos un conjunto de reglas de inferencia para el sistema experto.
reglas = [
    # Regla 1: Si las condiciones de "nubes" y "viento" son verdaderas, entonces deducimos "lluvia".
    # La regla es: si hay nubes y viento, entonces habrá lluvia.
    ("nubes", "viento", "lluvia"),  # La regla toma dos condiciones ("nubes" y "viento") y una conclusión ("lluvia").
    
    # Regla 2: Si la condición "sol" es verdadera, entonces deducimos "no_lluvia".
    # La regla es: si hay sol, no habrá lluvia.
    ("sol", "", "no_lluvia"),  # La regla toma una condición ("sol") y una conclusión ("no_lluvia"). Si no hay condiciones adicionales, el segundo argumento es una cadena vacía.
]

# Definimos los hechos iniciales disponibles en nuestro sistema.
# Los hechos representan lo que ya sabemos con certeza en el momento de la ejecución.
hechos = {
    "nubes": False,  # No hay nubes al inicio.
    "viento": False,  # No hay viento al inicio.
    "sol": True,  # Hay sol al inicio.
}

# Definimos la función para realizar el Encadenamiento Hacia Delante (Forward Chaining).
def encadenamiento_hacia_delante(hechos, reglas):
    # Inicializamos un conjunto para almacenar los hechos derivados de las reglas.
    nuevos_hechos = set()
    
    # Iteramos sobre todas las reglas para ver cuáles se pueden aplicar según los hechos actuales.
    for regla in reglas:
        # Extraemos las condiciones (primeros dos elementos de la regla).
        condiciones = regla[0:2]
        
        # Comprobamos si todas las condiciones de la regla son verdaderas con los hechos disponibles.
        # Usamos `all()` para asegurarnos de que todas las condiciones se cumplan.
        if all(hechos[condicion] for condicion in condiciones if condicion):
            # Si todas las condiciones se cumplen, entonces extraemos la conclusión (tercer elemento de la regla).
            conclusion = regla[2]
            
            # Verificamos si la conclusión aún no está presente en los hechos.
            if conclusion not in hechos:
                # Si la conclusión no está en los hechos, la añadimos como un nuevo hecho.
                hechos[conclusion] = True
                # Agregamos la nueva conclusión al conjunto de hechos derivados.
                nuevos_hechos.add(conclusion)
    
    # Devolvemos los nuevos hechos que se han derivado en este paso.
    return nuevos_hechos

# Definimos la función para realizar el Encadenamiento Hacia Atrás (Backward Chaining).
def encadenamiento_hacia_atras(hechos, reglas, meta):
    # Primero, comprobamos si la meta ya es un hecho conocido.
    if meta in hechos and hechos[meta]:
        # Si la meta es un hecho conocido, devolvemos `True` porque ya hemos alcanzado la meta.
        return True
    
    # Si la meta no es un hecho conocido, buscamos las reglas que podrían generar esa meta.
    for regla in reglas:
        # Extraemos las condiciones y la conclusión de la regla.
        condiciones = regla[0:2]
        conclusion = regla[2]
        
        # Si la conclusión de la regla es igual a nuestra meta, intentamos comprobar si las condiciones son verdaderas.
        if conclusion == meta:
            # Verificamos si todas las condiciones de la regla son verdaderas usando los hechos disponibles.
            if all(hechos[condicion] for condicion in condiciones if condicion):
                # Si las condiciones se cumplen, devolvemos `True` porque hemos alcanzado la meta.
                return True
            else:
                # Si las condiciones no se cumplen, intentamos verificar cada condición recursivamente.
                # Esto es un enfoque recursivo, buscando más hechos que puedan llevarnos a la meta.
                for condicion in condiciones:
                    if not hechos[condicion]:  # Si el hecho no existe, intentamos buscarlo.
                        if encadenamiento_hacia_atras(hechos, reglas, condicion):
                            return True
    # Si no podemos encontrar una cadena de hechos que lleve a la meta, devolvemos `False`.
    return False

# Ejecución del Encadenamiento Hacia Delante
print("Encadenamiento Hacia Delante:")
# Llamamos a la función de encadenamiento hacia adelante y almacenamos los nuevos hechos derivados.
nuevos_hechos = encadenamiento_hacia_delante(hechos, reglas)
# Imprimimos los hechos nuevos derivados durante el proceso.
print(f"Hechos derivados: {nuevos_hechos}")

# Ejecución del Encadenamiento Hacia Atrás
print("\nEncadenamiento Hacia Atrás:")
# Definimos la meta que queremos comprobar, en este caso, queremos saber si habrá "lluvia".
meta = "lluvia"
# Llamamos a la función de encadenamiento hacia atrás y verificamos si podemos llegar a la meta.
resultado = encadenamiento_hacia_atras(hechos, reglas, meta)
# Imprimimos el resultado indicando si es posible alcanzar la meta o no.
print(f"¿Es posible llegar a la meta '{meta}'? {'Sí' if resultado else 'No'}")
