from collections import defaultdict, deque  # Importamos estructuras útiles: diccionario con valores por defecto y cola doble

# Clase que representa una Acción en el dominio de planificación
class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name  # Nombre descriptivo de la acción (ejemplo: 'mover a cocina')
        self.preconditions = set(preconditions)  # Conjunto de precondiciones lógicas necesarias
        self.effects = set(effects)  # Conjunto de efectos lógicos que produce la acción

# Clase que representa el Grafo de Planificación (GraphPlan)
class GraphPlan:
    def __init__(self, initial_state, actions, goal):
        self.initial_state = set(initial_state)  # Estado inicial como conjunto de hechos
        self.actions = actions  # Lista de todas las acciones disponibles
        self.goal = set(goal)  # Estado meta como conjunto de hechos deseados

    # Método principal para ejecutar la planificación
    def plan(self):
        levels = []  # Lista donde guardaremos cada nivel del grafo (estados y acciones)
        current_level = self.initial_state  # Iniciamos con el estado inicial
        levels.append(current_level)  # Agregamos el nivel 0 al grafo

        # Bucle infinito hasta encontrar plan o determinar que no es posible
        while True:
            next_level = set(current_level)  # Inicializamos el siguiente nivel copiando el actual

            # Para cada acción disponible...
            for action in self.actions:
                # Si todas las precondiciones están en el nivel actual...
                if action.preconditions.issubset(current_level):
                    # Agregamos todos los efectos de la acción al siguiente nivel
                    next_level.update(action.effects)

            # Si no hay cambios, significa que no podemos expandir más
            if next_level == current_level:
                print("No hay plan posible. Meta inalcanzable.")
                return None  # Terminamos retornando None

            # Agregamos el nuevo nivel al grafo
            levels.append(next_level)

            # Si todos los objetivos están presentes en este nivel...
            if self.goal.issubset(next_level):
                print("Plan encontrado en nivel:", len(levels)-1)
                return self.extract_plan(levels)  # Llamamos para extraer el plan

            # Continuamos avanzando al siguiente nivel
            current_level = next_level

    # Método para extraer un plan simple desde los niveles generados
    def extract_plan(self, levels):
        plan = []  # Lista donde guardaremos el plan encontrado
        goals = self.goal.copy()  # Copiamos los objetivos a cumplir

        # Recorremos los niveles de forma inversa (de meta a inicial)
        for level in reversed(levels[:-1]):  # Saltamos el último nivel porque es la meta ya alcanzada
            for action in self.actions:
                # Si la acción es aplicable en este nivel...
                if action.preconditions.issubset(level):
                    # Y alguno de sus efectos contribuye a los objetivos actuales
                    if not goals.isdisjoint(action.effects):
                        # Agregamos esta acción al plan
                        plan.append(action.name)
                        # Actualizamos los objetivos: ahora son las precondiciones de esta acción
                        goals.update(action.preconditions)
                        goals.difference_update(action.effects)
        
        return list(reversed(plan))  # Retornamos el plan en orden correcto (de inicio a meta)

# ---------------------------- EJEMPLO CREATIVO: Robot que prepara cena ---------------------------- #

# Definimos las acciones disponibles para el robot
actions = [
    Action('mover a cocina', ['en sala'], ['en cocina', '¬en sala']),
    Action('mover a sala', ['en cocina'], ['en sala', '¬en cocina']),
    Action('limpiar mesa', ['en sala', 'mesa sucia'], ['mesa limpia', '¬mesa sucia']),
    Action('cocinar cena', ['en cocina', 'mesa limpia'], ['cena lista']),
]

# Definimos el estado inicial
initial_state = [
    'en sala',  # Robot está en la sala
    'mesa sucia'  # La mesa está sucia
]

# Definimos la meta deseada
goal = [
    'cena lista'  # Queremos que la cena esté lista
]

# Creamos una instancia de nuestro planificador
planner = GraphPlan(initial_state, actions, goal)

# Ejecutamos la planificación y obtenemos el plan
plan_result = planner.plan()

# Imprimimos el plan paso a paso si existe
if plan_result:
    print("\nPlan encontrado:")
    for step, action in enumerate(plan_result, 1):
        print(f"Paso {step}: {action}")
