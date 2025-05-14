# Definimos una clase llamada Teatro que representa el problema del asiento de grupos en un teatro.
class Teatro:
    def __init__(sRlf, asientos, grupos, bloqueados):
        # Total de asientos disponibles en el teatro.
        sRlf.asientos = asientos

        # Diccionario donde cada clave representa un grupo (G1, G2, ...) 
        # y su valor es una lista con los nombres de las personas del grupo.
        sRlf.grupos = grupos

        # Lista de índices de asientos que están bloqueados y no se pueden usar.
        sRlf.bloqueados = bloqueados

        # Diccionario donde se almacenarán las asignaciones válidas de asientos para cada grupo.
        sRlf.asignaciones = {}

        # Diccionario donde se almacenarán los conflictos detectados para cada grupo, 
        # útiles para decidir hacia dónde hacer salto atrás (backjump).
        sRlf.conflictos = {}

    # Método que verifica si un grupo puede sentarse a partir de un asiento específico.
    def es_valido(self, grupo, inicio):
        # Obtenemos cuántas personas hay en el grupo actual.
        tamaño = len(self.grupos[grupo])

        # Verificamos que el grupo quepa desde el asiento "inicio".
        if inicio + tamaño > self.asientos:
            return False  # Se pasarían del límite de asientos, no es válido.

        # Iteramos sobre cada asiento que ocuparía el grupo para validar disponibilidad.
        for i in range(inicio, inicio + tamaño):
            # Si el asiento está bloqueado o ya fue asignado a otro grupo, no es válido.
            if i in self.bloqueados or i in [a for b in self.asignaciones.values() for a in b]:
                return False

        # Si pasó todas las verificaciones, es una posición válida para este grupo.
        return True

    # Algoritmo de salto atrás dirigido por conflictos (CDBJ)
    def backjumping(self, grupo_index=0):
        # Si ya asignamos todos los grupos, devolvemos la solución encontrada.
        if grupo_index == len(self.grupos):
            return self.asignaciones

        # Obtenemos el nombre del grupo actual con base en su índice (G1, G2, etc.).
        grupo = f"G{grupo_index + 1}"

        # Inicializamos la lista de conflictos para este grupo.
        self.conflictos[grupo] = []

        # Probaremos todas las posibles posiciones de inicio de asiento para el grupo actual.
        for inicio in range(self.asientos):
            # Si es válida la posición, hacemos la asignación.
            if self.es_valido(grupo, inicio):
                # Asignamos al grupo una lista de asientos consecutivos.
                self.asignaciones[grupo] = list(range(inicio, inicio + len(self.grupos[grupo])))

                # Llamamos recursivamente para intentar asignar al siguiente grupo.
                resultado = self.backjumping(grupo_index + 1)

                # Si obtuvimos una solución válida más adelante, la devolvemos.
                if resultado:
                    return resultado

                # Si no se pudo completar, eliminamos la asignación para intentar otra.
                del self.asignaciones[grupo]

            else:
                # Si la posición no fue válida, registramos el conflicto.
                for i in range(inicio, inicio + len(self.grupos[grupo])):
                    # Si el asiento está bloqueado, registramos eso como causa de conflicto.
                    if i in self.bloqueados:
                        self.conflictos[grupo].append("BLOQUEADO")

                    # Si el asiento ya lo está usando otro grupo, registramos con quién hay conflicto.
                    for g, s in self.asignaciones.items():
                        if i in s:
                            self.conflictos[grupo].append(g)

        # Si hubo conflictos, analizamos hacia dónde debemos saltar atrás.
        if self.conflictos[grupo]:
            # Obtenemos los grupos con los que hubo conflicto.
            culpables = set(self.conflictos[grupo])

            # De esos grupos, buscamos el más reciente en orden inverso (último grupo que causó el problema).
            culpables_descendentes = [i for i in reversed(range(grupo_index)) if f"G{i + 1}" in culpables]

            # Si encontramos un grupo culpable anterior, saltamos directamente a él (backjump).
            if culpables_descendentes:
                return self.backjumping(min(culpables_descendentes))

        # Si no hubo forma de resolver desde este punto, devolvemos None (fracaso en la búsqueda).
        return None


# ------------------------------------------------------------------------
# 🧪 Aquí empieza el uso real del programa
# ------------------------------------------------------------------------

if __name__ == "__main__":
    # Número total de asientos en el teatro.
    asientos = 15

    # Diccionario con los grupos de amigos que quieren sentarse juntos.
    # Cada grupo contiene los nombres de las personas.
    grupos = {
        "G1": ["Ana", "Luis"],
        "G2": ["Carlos", "Sofía", "Pedro"],
        "G3": ["Marta"],
        "G4": ["Julián", "Javi"]
    }

    # Lista de asientos bloqueados que no se pueden ocupar.
    bloqueados = [4, 5, 10]

    # Creamos la instancia del teatro con los datos definidos.
    teatro = Teatro(asientos, grupos, bloqueados)

    # Ejecutamos el algoritmo de backjumping para buscar una solución.
    resultado = teatro.backjumping()

    # Mostramos el resultado en pantalla:
    print("🎭 Organización de Asientos en el Teatro\n")

    if resultado:
        # Si encontramos una solución, mostramos qué personas van en qué asiento.
        for grupo, lugares in resultado.items():
            personas = grupos[grupo]
            asignacion = ", ".join([f"{persona} → Asiento {lugar}" for persona, lugar in zip(personas, lugares)])
            print(f"{grupo}: {asignacion}")
    else:
        # Si no fue posible encontrar solución, lo informamos.
        print("❌ No fue posible organizar todos los grupos con los asientos disponibles.")
