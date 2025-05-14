# Función que determina si dos superpoderes tienen un conflicto entre sí
def tiene_conflicto(poder1, poder2):
    """
    Verifica si dos poderes son conflictivos según una lista predefinida de conflictos.
    """
    conflictos = {
        "Manipulación Elemental (Fuego)": ["Manipulación Elemental (Hielo)", "Manipulación Elemental (Agua)"],
        "Manipulación Elemental (Hielo)": ["Manipulación Elemental (Fuego)"],
        "Manipulación Elemental (Agua)": ["Manipulación Elemental (Fuego)"],
    }
    # Devuelve True si el segundo poder está en la lista de conflictos del primero
    return poder2 in conflictos.get(poder1, [])

# Función principal que aplica la técnica de Forward Checking para asignar superpoderes
def forward_checking_superpoderes(invitados, dominios, restricciones, asignacion):
    """
    Asigna superpoderes únicos a los invitados usando Comprobación Hacia Delante,
    respetando restricciones de unicidad y conflictos definidos.
    """

    # Caso base: si ya hay tantos poderes asignados como invitados, se encontró solución
    if len(asignacion) == len(invitados):
        return asignacion

    # Seleccionar el siguiente invitado a asignar poder (por orden en la lista)
    invitado_actual = invitados[len(asignacion)]

    # Se recorre una copia del dominio del invitado actual para evitar modificar el original durante la iteración
    for poder in list(dominios[invitado_actual]):

        # Asignar provisionalmente este poder al invitado actual
        asignacion[invitado_actual] = poder

        # Crear una copia del dominio para los invitados no asignados (se usará para seguir evaluando)
        dominios_futuros = {inv: set(dom) for inv, dom in dominios.items()}

        consistente = True  # Esta variable verifica si la asignación actual permite seguir avanzando

        # Revisar los siguientes invitados no asignados
        for siguiente_invitado in invitados[len(asignacion) + 1:]:
            dominio_reducido = set()  # Aquí se guardarán los poderes válidos para ese siguiente invitado

            # Verificar cada poder del dominio original de ese invitado
            for poder_futuro in dominios[siguiente_invitado]:
                cumple_restricciones = True

                # Comparar el poder futuro con los ya asignados para verificar unicidad y conflictos
                for inv_asignado, poder_asignado in asignacion.items():

                    # Restricción de unicidad: no puede haber poderes repetidos
                    if poder_futuro == poder_asignado:
                        cumple_restricciones = False
                        break

                    # Restricción de conflicto entre Ana y Beto
                    if (invitado_actual == "Ana" and inv_asignado == "Beto" and tiene_conflicto(poder, poder_asignado)) or \
                       (invitado_actual == "Beto" and inv_asignado == "Ana" and tiene_conflicto(poder, poder_asignado)):

                        cumple_restricciones = False
                        break

                    # Restricción de combinación específica: Carlos no puede tener Telequinesis si Diana tiene Vuelo
                    if (invitado_actual == "Carlos" and inv_asignado == "Diana" and poder == "Telequinesis" and poder_asignado == "Vuelo") or \
                       (invitado_actual == "Diana" and inv_asignado == "Carlos" and poder == "Vuelo" and poder_asignado == "Telequinesis"):

                        cumple_restricciones = False
                        break

                # Si el poder futuro no viola restricciones, se agrega al dominio reducido
                if cumple_restricciones:
                    dominio_reducido.add(poder_futuro)

            # Si el dominio del siguiente invitado queda vacío, esta asignación no sirve
            if not dominio_reducido:
                consistente = False
                break

            # Actualizamos el dominio futuro con los valores reducidos válidos
            dominios_futuros[siguiente_invitado] = dominio_reducido

        # Si es consistente, se continúa de forma recursiva
        if consistente:
            resultado = forward_checking_superpoderes(invitados, dominios_futuros, restricciones, asignacion)
            if resultado:  # Si se obtuvo una solución válida, se retorna
                return resultado

        # Si no fue posible completar con esta asignación, se hace backtrack (deshacer)
        del asignacion[invitado_actual]

    # Si ningún poder resultó en solución válida, se retorna None
    return None

# Lista de invitados a los que se les asignarán superpoderes
invitados = ["Ana", "Beto", "Carlos", "Diana"]

# Dominios iniciales: cada invitado puede recibir cualquiera de estos superpoderes
dominios_iniciales = {
    "Ana": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", 
            "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Beto": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", 
             "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Carlos": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", 
               "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Diana": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", 
              "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
}

# Restricciones adicionales (aparte de la unicidad de poderes):
restricciones = [
    ("Ana", "Beto", lambda a, b: not tiene_conflicto(a, b)),  # Ana y Beto no deben tener poderes en conflicto
    ("Carlos", "Diana", lambda c, d: not (c == "Telequinesis" and d == "Vuelo")),  # Carlos y Diana no deben tener esta combinación
]

# Se ejecuta el algoritmo de forward checking
solucion = forward_checking_superpoderes(invitados, dominios_iniciales, restricciones, {})

# Mostrar el resultado
if solucion:
    print("¡Asignación de superpoderes exitosa!")
    for invitado, poder in solucion.items():
        print(f"{invitado}: {poder}")
else:
    print("No se encontró una asignación de superpoderes que cumpla con todas las restricciones.")
