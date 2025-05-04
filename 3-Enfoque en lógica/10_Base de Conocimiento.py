# Definimos los hechos y las reglas en la base de conocimiento
hechos = {
    "nubes": False,  # No hay nubes (se asume que el cielo está despejado)
    "viento": False,  # No hay viento (el clima está tranquilo)
    "lluvia": False  # No está lloviendo (el suelo está seco)
}

# Definimos las reglas para la base de conocimiento
# Regla: Si hay nubes y viento, es probable que llueva.
reglas = [
    ("nubes", "viento", "lluvia"),  # Esto significa: si hay nubes Y hay viento, entonces llueve
]

# Función para aplicar las reglas de inferencia
def aplicar_reglas(hechos, reglas):
    nuevos_hechos = set()  # Creamos un conjunto vacío donde guardaremos nuevos hechos deducidos
    
    # Comprobamos todas las reglas una por una
    for regla in reglas:
        condiciones = regla[0:2]  # Tomamos las primeras dos partes de la regla como condiciones ("nubes" y "viento")
        conclusion = regla[2]  # La tercera parte de la regla es la conclusión ("lluvia")
        
        # Verificamos si TODAS las condiciones son verdaderas en los hechos actuales
        if all(hechos[condicion] for condicion in condiciones if condicion):
            # Si la conclusión todavía no es verdadera, la marcamos como verdadera
            if not hechos.get(conclusion, False):  # .get devuelve False si no existe la conclusión
                hechos[conclusion] = True  # Ahora decimos que este nuevo hecho es verdadero
                nuevos_hechos.add(conclusion)  # Guardamos la conclusión nueva en el conjunto de nuevos hechos
    
    return nuevos_hechos  # Devolvemos todos los nuevos hechos que se dedujeron

# Función para decidir si llevar paraguas, según los hechos actuales
def decidir_paraguas(hechos):
    if hechos["lluvia"]:  # Si en los hechos dice que está lloviendo
        return "Lleva paraguas"  # Recomendamos llevar paraguas
    else:  # Si no está lloviendo
        return "No es necesario llevar paraguas"  # Decimos que no hace falta

# Aplicamos las reglas de inferencia para actualizar los hechos
nuevos_hechos = aplicar_reglas(hechos, reglas)

# Tomamos una decisión sobre si debemos llevar paraguas o no
decisión = decidir_paraguas(hechos)

# Mostrar en pantalla todos los hechos después de aplicar las reglas
print("Hechos después de la inferencia:")
for hecho, valor in hechos.items():  # Recorremos cada hecho y su valor (True o False)
    print(f"{hecho}: {valor}")  # Mostramos el hecho y su estado

# Mostrar la decisión final (llevar paraguas o no)
print("\nDecisión:", decisión)
