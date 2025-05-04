"""
SISTEMA DE PLANIFICACIÓN CON ALGORITMOS STRIPS Y ADL
Autor: DeepSeek Chat
Enfoque: Representación de acciones, estados y metas para planificación automatizada
"""

from typing import List, Dict, Set, Tuple

# ==================== REPRESENTACIÓN STRIPS ====================
class STRIPSAction:
    """
    Representa una acción en STRIPS con:
    - Precondiciones: condiciones que deben ser verdaderas para ejecutar la acción
    - Efectos: condiciones que se hacen verdaderas después de ejecutar la acción
    - Efectos negativos: condiciones que se hacen falsas después de ejecutar la acción
    """
    def __init__(self, name: str, preconditions: Set[str], 
                 effects: Set[str], negative_effects: Set[str] = None):
        self.name = name  # Nombre de la acción
        self.preconditions = preconditions  # Condiciones requeridas
        self.effects = effects  # Condiciones que se hacen verdaderas
        self.negative_effects = negative_effects if negative_effects else set()  # Condiciones que se hacen falsas

    def __repr__(self):
        return f"Acción {self.name}"

class STRIPSPlanner:
    """
    Planificador STRIPS que encuentra una secuencia de acciones para alcanzar una meta
    desde un estado inicial.
    """
    def __init__(self, actions: List[STRIPSAction]):
        self.actions = actions  # Lista de acciones disponibles

    def plan(self, initial_state: Set[str], goal: Set[str]) -> List[str]:
        """
        Genera un plan para alcanzar la meta desde el estado inicial.
        
        Args:
            initial_state: Conjunto de proposiciones verdaderas al inicio
            goal: Conjunto de proposiciones que deben ser verdaderas al final
            
        Returns:
            Lista de nombres de acciones que forman el plan
        """
        current_state = set(initial_state)  # Copiamos el estado inicial
        plan = []  # Aquí almacenaremos las acciones del plan
        
        # Mientras no se hayan alcanzado todas las metas
        while not goal.issubset(current_state):
            # Buscamos una acción aplicable que acerque a la meta
            action_applied = False
            
            for action in self.actions:
                # Verificamos si la acción es aplicable (precondiciones cumplidas)
                if action.preconditions.issubset(current_state):
                    # Verificamos si la acción contribuye a alguna meta no alcanzada
                    useful_effects = goal.difference(current_state).intersection(action.effects)
                    if useful_effects or not action_applied:
                        # Aplicamos la acción
                        current_state.update(action.effects)  # Añadimos efectos positivos
                        current_state.difference_update(action.negative_effects)  # Eliminamos efectos negativos
                        plan.append(action.name)  # Añadimos al plan
                        action_applied = True
                        break
            
            if not action_applied:
                raise ValueError("No se puede encontrar un plan para alcanzar la meta")
        
        return plan

# ==================== REPRESENTACIÓN ADL ====================
class ADLAction:
    """
    Representa una acción en ADL (Action Description Language) que permite:
    - Precondiciones más complejas (con cuantificadores y condiciones compuestas)
    - Efectos condicionales
    """
    def __init__(self, name: str, 
                 preconditions: List[str],  # Lista de condiciones en formato string
                 effects: List[Tuple[str, List[str]]]):  # Lista de (efecto, condiciones)
        self.name = name
        self.preconditions = preconditions
        self.effects = effects  # Efectos condicionales

    def is_applicable(self, state: Set[str]) -> bool:
        """
        Verifica si la acción es aplicable en el estado actual.
        ADL permite precondiciones más complejas que STRIPS.
        """
        # Evaluamos cada precondición (simplificado para este ejemplo)
        for cond in self.preconditions:
            if cond.startswith("not ") and cond[4:] in state:
                return False
            elif not cond.startswith("not ") and cond not in state:
                return False
        return True

    def apply(self, state: Set[str]) -> Set[str]:
        """
        Aplica la acción al estado actual, considerando efectos condicionales.
        """
        new_state = set(state)
        for effect, conditions in self.effects:
            # Verificamos si se cumplen las condiciones para este efecto
            all_conditions_met = True
            for cond in conditions:
                if cond.startswith("not ") and cond[4:] in new_state:
                    all_conditions_met = False
                    break
                elif not cond.startswith("not ") and cond not in new_state:
                    all_conditions_met = False
                    break
            
            if all_conditions_met:
                if effect.startswith("not "):
                    new_state.discard(effect[4:])  # Eliminamos si es negativo
                else:
                    new_state.add(effect)  # Añadimos si es positivo
        
        return new_state

class ADLPlanner:
    """
    Planificador ADL que maneja acciones con precondiciones y efectos más complejos.
    """
    def __init__(self, actions: List[ADLAction]):
        self.actions = actions

    def plan(self, initial_state: Set[str], goal: Set[str], max_depth=20) -> List[str]:
        """
        Planificación con búsqueda hacia adelante con backtracking.
        """
        def recurse(state: Set[str], current_plan: List[str], depth: int) -> List[str]:
            if depth > max_depth:
                return None  # Límite de profundidad alcanzado
            
            if goal.issubset(state):
                return current_plan  # Meta alcanzada
            
            for action in self.actions:
                if action.is_applicable(state):
                    new_state = action.apply(state)
                    result = recurse(new_state, current_plan + [action.name], depth + 1)
                    if result is not None:
                        return result
            
            return None  # No se encontró plan

        return recurse(set(initial_state), [], 0)

# ==================== EJEMPLO: DOMINIO DEL MUNDO DE LOS BLOQUES ====================
def setup_blocks_world():
    """Configura el dominio del mundo de los bloques para STRIPS y ADL"""
    
    # Acciones STRIPS
    strips_actions = [
        STRIPSAction(
            name="mover_A_a_B",
            preconditions={"libre_A", "sobre_A_mesa", "libre_B"},
            effects={"sobre_A_B", "libre_A_mesa"},
            negative_effects={"sobre_A_mesa", "libre_B"}
        ),
        STRIPSAction(
            name="mover_A_a_mesa",
            preconditions={"libre_A", "sobre_A_B"},
            effects={"sobre_A_mesa", "libre_B"},
            negative_effects={"sobre_A_B"}
        )
    ]
    
    # Acciones ADL (más expresivas)
    adl_actions = [
        ADLAction(
            name="mover_X_a_Y",
            preconditions=["libre_X", "sobre_X_Z", "libre_Y", "X != Y"],
            effects=[
                ("sobre_X_Y", []),
                ("libre_Z", []),
                ("not sobre_X_Z", []),
                ("not libre_Y", [])
            ]
        ),
        ADLAction(
            name="mover_X_a_mesa",
            preconditions=["libre_X", "sobre_X_Y"],
            effects=[
                ("sobre_X_mesa", []),
                ("libre_Y", []),
                ("not sobre_X_Y", [])
            ]
        )
    ]
    
    return strips_actions, adl_actions

# ==================== INTERFAZ DE USUARIO ====================
def main():
    print("=== SISTEMA DE PLANIFICACIÓN CON STRIPS Y ADL ===")
    print("Dominio: Mundo de los bloques\n")
    
    # Configurar acciones
    strips_actions, adl_actions = setup_blocks_world()
    
    # Estado inicial y meta
    initial_state = {"sobre_A_mesa", "sobre_B_mesa", "libre_A", "libre_B", "libre_C"}
    goal_state = {"sobre_A_B", "sobre_B_C"}
    
    # Planificación con STRIPS
    print("\nPlanificación con STRIPS:")
    strips_planner = STRIPSPlanner(strips_actions)
    try:
        plan = strips_planner.plan(initial_state, goal_state)
        print("Plan encontrado:", " -> ".join(plan))
    except ValueError as e:
        print("Error:", e)
    
    # Planificación con ADL
    print("\nPlanificación con ADL:")
    adl_planner = ADLPlanner(adl_actions)
    plan = adl_planner.plan(initial_state, goal_state)
    if plan:
        print("Plan encontrado:", " -> ".join(plan))
    else:
        print("No se pudo encontrar un plan")

if __name__ == "__main__":
    main()