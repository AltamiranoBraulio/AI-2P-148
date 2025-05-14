class PlanificacionHorarios:
    # El constructor de la clase inicializa los atributos necesarios para la planificación
    def __init__(self, clases, profesores, aulas):
        # Inicializa las listas de clases, profesores y aulas
        self.clases = clases  # Lista de nombres de las clases a planificar
        self.profesores = profesores  # Lista de nombres de los profesores
        self.aulas = aulas  # Lista de nombres de las aulas disponibles
        
        # Inicializa el diccionario de asignaciones vacío para clases y aulas
        self.asignaciones = {
            "clases": {},  # Asignaciones de clases a profesores
            "aulas": {}    # Asignaciones de clases a aulas
        }
        
        # Inicializa los dominios para clases, profesores y aulas
        # Los dominios contienen una lista de posibles profesores y aulas que se pueden asignar a cada clase
        self.dominios = {
            "clases": {clase: list(range(len(self.profesores))) for clase in clases},  # Para cada clase, hay una lista de posibles índices de profesores
            "aulas": {clase: list(range(len(self.aulas))) for clase in clases}  # Para cada clase, hay una lista de posibles índices de aulas
        }

    # Función que verifica las restricciones de asignación de profesores y aulas
    def verificar_restricciones(self):
        """Verifica que ninguna clase tenga conflicto de profesor o aula"""
        # Verificar que no haya profesores asignados a más de una clase al mismo tiempo
        for clase1, prof1 in self.asignaciones["clases"].items():
            for clase2, prof2 in self.asignaciones["clases"].items():
                if clase1 != clase2 and prof1 == prof2:  # Si el mismo profesor está asignado a dos clases distintas
                    return False  # Conflicto de profesor, retorna False

        # Verificar que las aulas no se solapen
        for clase1, aula1 in self.asignaciones["aulas"].items():
            for clase2, aula2 in self.asignaciones["aulas"].items():
                if clase1 != clase2 and aula1 == aula2:  # Si el mismo aula está asignada a dos clases distintas
                    return False  # Conflicto de aula, retorna False

        return True  # Si no hay conflictos, retorna True

    # Función que propaga las restricciones, eliminando valores no válidos de los dominios
    def propagacion(self, clase):
        """Elimina valores no válidos de los dominios de las clases"""
        # Si ya se ha asignado un profesor o aula a la clase, propagamos las restricciones
        profesor_asignado = self.asignaciones["clases"].get(clase)  # Obtiene el profesor asignado a la clase
        aula_asignada = self.asignaciones["aulas"].get(clase)  # Obtiene el aula asignada a la clase

        if profesor_asignado is not None:  # Si un profesor ya está asignado
            for otra_clase in self.clases:  # Recorre todas las clases
                if otra_clase != clase:  # Si la clase no es la actual
                    if profesor_asignado in self.dominios["clases"][otra_clase]:  # Si el profesor está en el dominio de otra clase
                        self.dominios["clases"][otra_clase].remove(profesor_asignado)  # Elimina ese profesor de los posibles dominios de esa clase

        if aula_asignada is not None:  # Si un aula ya está asignada
            for otra_clase in self.clases:  # Recorre todas las clases
                if otra_clase != clase:  # Si la clase no es la actual
                    if aula_asignada in self.dominios["aulas"][otra_clase]:  # Si el aula está en el dominio de otra clase
                        self.dominios["aulas"][otra_clase].remove(aula_asignada)  # Elimina esa aula de los posibles dominios de esa clase

    # Función principal de backtracking que intenta asignar las clases a los profesores y aulas
    def backtracking(self):
        """Algoritmo de Backtracking con Propagación de Restricciones"""
        # Si ya se han asignado todas las clases
        if len(self.asignaciones["clases"]) == len(self.clases):
            if self.verificar_restricciones():  # Verificar si las restricciones se cumplen
                return self.asignaciones  # Si se cumple, retorna las asignaciones
            return None  # Si no se cumplen las restricciones, retorna None

        # Selecciona la siguiente clase para asignar (se elige la clase que no se ha asignado aún)
        clase = len(self.asignaciones["clases"])

        # Prueba cada posible profesor y aula para la clase
        for profesor in self.dominios["clases"][self.clases[clase]]:  # Recorre los posibles profesores para la clase
            for aula in self.dominios["aulas"][self.clases[clase]]:  # Recorre los posibles aulas para la clase
                # Asigna el profesor y el aula a la clase
                self.asignaciones["clases"][self.clases[clase]] = profesor
                self.asignaciones["aulas"][self.clases[clase]] = aula

                # Propaga las restricciones para actualizar los dominios
                self.propagacion(self.clases[clase])

                # Llamada recursiva para intentar asignar las siguientes clases
                resultado = self.backtracking()
                if resultado:  # Si se encuentra una solución
                    return resultado  # Retorna el resultado

                # Si no se encuentra solución, deshace la asignación
                del self.asignaciones["clases"][self.clases[clase]]
                del self.asignaciones["aulas"][self.clases[clase]]

        return None  # Si no se encuentra ninguna solución, retorna None

# ---------------- EJECUCIÓN ----------------

if __name__ == "__main__":
    # Se definen los datos de entrada: clases, profesores y aulas
    clases = ["Matemáticas", "Física", "Química"]
    profesores = ["Profesor A", "Profesor B", "Profesor C"]
    aulas = ["Aula 1", "Aula 2", "Aula 3"]

    # Crear un objeto de la clase PlanificacionHorarios con los datos de entrada
    planificador = PlanificacionHorarios(clases, profesores, aulas)

    # Intenta encontrar una asignación válida de clases, profesores y aulas
    asignaciones = planificador.backtracking()

    # Si se encuentra una asignación válida, se muestra por pantalla
    if asignaciones:
        print("✅ Solución encontrada: ")
        for clase in asignaciones["clases"]:
            print(f"{clase}: Profesor - {asignaciones['clases'][clase]}, Aula - {asignaciones['aulas'][clase]}")
    else:
        print("❌ No se pudo encontrar una solución.")  # Si no se encuentra solución, se muestra este mensaje
