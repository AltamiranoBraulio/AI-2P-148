def tiene_conflicto(poder1, poder2):
    """Verifica si dos poderes son conflictivos."""
    conflictos = {
        "Manipulación Elemental (Fuego)": ["Manipulación Elemental (Hielo)"],
        "Manipulación Elemental (Hielo)": ["Manipulación Elemental (Fuego)"],
        "Manipulación Elemental (Agua)": ["Manipulación Elemental (Fuego)"],
        "Manipulación Elemental (Fuego)": ["Manipulación Elemental (Agua)"],
    }
    return poder2 in conflictos.get(poder1, [])

def forward_checking_superpoderes(invitados, dominios, restricciones, asignacion):
    """
    Aplica Comprobación Hacia Delante para asignar superpoderes únicos a invitados.
    """
    if len(asignacion) == len(invitados):
        return asignacion  # Solución encontrada

    invitado_actual = invitados[len(asignacion)]
    for poder in list(dominios[invitado_actual]):  # Iterar sobre una copia para permitir modificaciones
        asignacion[invitado_actual] = poder
        dominios_futuros = {inv: set(dom) for inv, dom in dominios.items()}  # Copia de los dominios

        consistente = True
        for siguiente_invitado in invitados[len(asignacion) + 1:]:
            dominio_reducido = set()
            for poder_futuro in dominios[siguiente_invitado]:
                cumple_restricciones = True
                # Verificar restricciones con la asignación actual
                for inv_asignado, poder_asignado in asignacion.items():
                    if poder_futuro == poder_asignado:  # Verificar unicidad
                        cumple_restricciones = False
                        break
                    if (invitado_actual == "Ana" and inv_asignado == "Beto" and tiene_conflicto(poder, poder_asignado)) or \
                       (invitado_actual == "Beto" and inv_asignado == "Ana" and tiene_conflicto(poder, poder_asignado)) or \
                       (invitado_actual == "Carlos" and inv_asignado == "Diana" and poder == "Telequinesis" and poder_asignado == "Vuelo") or \
                       (invitado_actual == "Diana" and inv_asignado == "Carlos" and poder == "Vuelo" and poder_asignado == "Telequinesis"):
                        cumple_restricciones = False
                        break
                if cumple_restricciones:
                    dominio_reducido.add(poder_futuro)

            if not dominio_reducido:
                consistente = False
                break
            dominios_futuros[siguiente_invitado] = dominio_reducido

        if consistente:
            resultado = forward_checking_superpoderes(invitados, dominios_futuros, restricciones, asignacion)
            if resultado:
                return resultado

        del asignacion[invitado_actual]  # Backtrack si la asignación no lleva a solución

    return None

# Definición del problema
invitados = ["Ana", "Beto", "Carlos", "Diana"]
dominios_iniciales = {
    "Ana": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Beto": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Carlos": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
    "Diana": {"Fuerza Sobrehumana", "Telequinesis", "Vuelo", "Control del Tiempo", "Invisibilidad", "Manipulación Elemental (Fuego)", "Manipulación Elemental (Agua)", "Manipulación Elemental (Hielo)"},
}
restricciones = [
    ("Ana", "Beto", lambda a, b: not tiene_conflicto(a, b)),
    ("Carlos", "Diana", lambda c, d: not (c == "Telequinesis" and d == "Vuelo")),
]

# Ejecutar la búsqueda con Comprobación Hacia Delante
solucion = forward_checking_superpoderes(invitados, dominios_iniciales, restricciones, {})

if solucion:
    print("¡Asignación de superpoderes exitosa!")
    for invitado, poder in solucion.items():
        print(f"{invitado}: {poder}")
else:
    print("No se encontró una asignación de superpoderes que cumpla con todas las restricciones.")