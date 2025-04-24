class PlanificacionHorarios:
    def __init__(self, clases, profesores, aulas):
        self.clases = clases
        self.profesores = profesores
        self.aulas = aulas
        self.asignaciones = {
            "clases": {},  # Inicializa la clave 'clases' como un diccionario vacío
            "aulas": {}    # Inicializa la clave 'aulas' como un diccionario vacío
        }
        self.dominios = {
            "clases": {clase: list(range(len(self.profesores))) for clase in clases},
            "aulas": {clase: list(range(len(self.aulas))) for clase in clases}
        }

    def verificar_restricciones(self):
        """Verifica que ninguna clase tenga conflicto de profesor o aula"""
        # Comprobar que no haya profesores asignados a más de una clase al mismo tiempo
        for clase1, prof1 in self.asignaciones["clases"].items():
            for clase2, prof2 in self.asignaciones["clases"].items():
                if clase1 != clase2 and prof1 == prof2:
                    return False  # Conflicto de profesor

        # Comprobar que las aulas no se solapen
        for clase1, aula1 in self.asignaciones["aulas"].items():
            for clase2, aula2 in self.asignaciones["aulas"].items():
                if clase1 != clase2 and aula1 == aula2:
                    return False  # Conflicto de aula

        return True

    def propagacion(self, clase):
        """Elimina valores no válidos de los dominios de las clases"""
        # Propagación de restricciones: si un profesor o aula ya está asignado, se elimina de los dominios
        profesor_asignado = self.asignaciones["clases"].get(clase)
        aula_asignada = self.asignaciones["aulas"].get(clase)

        if profesor_asignado is not None:
            for otra_clase in self.clases:
                if otra_clase != clase:
                    if profesor_asignado in self.dominios["clases"][otra_clase]:
                        self.dominios["clases"][otra_clase].remove(profesor_asignado)

        if aula_asignada is not None:
            for otra_clase in self.clases:
                if otra_clase != clase:
                    if aula_asignada in self.dominios["aulas"][otra_clase]:
                        self.dominios["aulas"][otra_clase].remove(aula_asignada)

    def backtracking(self):
        """Algoritmo de Backtracking con Propagación de Restricciones"""
        if len(self.asignaciones["clases"]) == len(self.clases):
            if self.verificar_restricciones():
                return self.asignaciones
            return None  # Si no cumple las restricciones

        # Seleccionar una clase para asignar
        clase = len(self.asignaciones["clases"])

        for profesor in self.dominios["clases"][self.clases[clase]]:
            for aula in self.dominios["aulas"][self.clases[clase]]:
                # Asignar profesor y aula a la clase
                self.asignaciones["clases"][self.clases[clase]] = profesor
                self.asignaciones["aulas"][self.clases[clase]] = aula

                # Propagar las restricciones
                self.propagacion(self.clases[clase])

                # Llamar recursivamente
                resultado = self.backtracking()
                if resultado:
                    return resultado

                # Si no funciona, deshacer la asignación
                del self.asignaciones["clases"][self.clases[clase]]
                del self.asignaciones["aulas"][self.clases[clase]]

        return None  # No se encontró una solución

# ---------------- EJECUCIÓN ----------------

if __name__ == "__main__":
    clases = ["Matemáticas", "Física", "Química"]
    profesores = ["Profesor A", "Profesor B", "Profesor C"]
    aulas = ["Aula 1", "Aula 2", "Aula 3"]

    # Crear el objeto de planificación
    planificador = PlanificacionHorarios(clases, profesores, aulas)

    # Intentar encontrar una asignación válida
    asignaciones = planificador.backtracking()

    if asignaciones:
        print("✅ Solución encontrada: ")
        for clase in asignaciones["clases"]:
            print(f"{clase}: Profesor - {asignaciones['clases'][clase]}, Aula - {asignaciones['aulas'][clase]}")
    else:
        print("❌ No se pudo encontrar una solución.")
