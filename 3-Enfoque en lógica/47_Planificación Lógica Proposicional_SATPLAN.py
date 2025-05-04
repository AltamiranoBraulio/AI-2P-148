"""
SISTEMA DE PLANIFICACIÓN SATPLAN
Autor: DeepSeek Chat
Enfoque: Planificación mediante satisfacción booleana (SAT)

Este sistema convierte problemas de planificación en fórmulas proposicionales
y utiliza un solucionador SAT para encontrar planes válidos.
"""

from typing import List, Dict, Set, Tuple, Optional
import itertools
from pysat.solvers import Glucose3  # Solucionador SAT eficiente

# ==================== REPRESENTACIÓN DEL PROBLEMA ====================

class Accion:
    """
    Representa una acción en el dominio de planificación con:
    - nombre: Identificador único
    - precondiciones: Condiciones necesarias para ejecutar
    - efectos_pos: Condiciones que se hacen verdaderas
    - efectos_neg: Condiciones que se hacen falsas
    """
    def __init__(self, nombre: str, precondiciones: Set[str], efectos_pos: Set[str], efectos_neg: Set[str]):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.efectos_pos = efectos_pos
        self.efectos_neg = efectos_neg

    def __repr__(self):
        return self.nombre

class ProblemaPlanificacion:
    """
    Representa un problema completo de planificación con:
    - acciones: Lista de acciones disponibles
    - estado_inicial: Condiciones verdaderas al inicio
    - objetivos: Condiciones que deben ser verdaderas al final
    """
    def __init__(self, acciones: List[Accion], estado_inicial: Set[str], objetivos: Set[str]):
        self.acciones = acciones
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos

# ==================== CODIFICACIÓN SAT ====================

class CodificadorSAT:
    """
    Codifica problemas de planificación en fórmulas proposicionales
    usando esquema de codificación lineal para SATPLAN
    """
    
    def __init__(self, problema: ProblemaPlanificacion):
        self.problema = problema
        self.variables = {}  # Diccionario de variables proposicionales
        self.contador_var = 1  # Contador para asignar IDs únicos a variables
        
    def _obtener_var(self, nombre: str, tiempo: int) -> int:
        """
        Obtiene o crea una variable proposicional para (nombre, tiempo)
        
        Args:
            nombre: Nombre de la proposición/acción
            tiempo: Paso temporal (nivel)
            
        Returns:
            ID numérico de la variable en el solucionador SAT
        """
        clave = (nombre, tiempo)
        if clave not in self.variables:
            self.variables[clave] = self.contador_var
            self.contador_var += 1
        return self.variables[clave]
    
    def codificar_problema(self, longitud_plan: int) -> List[List[int]]:
        """
        Codifica el problema de planificación en una fórmula SAT
        para un plan de longitud específica
        
        Args:
            longitud_plan: Número de pasos de acción en el plan
            
        Returns:
            Lista de cláusulas en formato CNF (Conjunctive Normal Form)
        """
        clausulas = []
        
        # 1. Codificar estado inicial (tiempo 0)
        for prop in self.problema.estado_inicial:
            var = self._obtener_var(prop, 0)
            clausulas.append([var])  # Las proposiciones iniciales son verdaderas
        
        # 2. Codificar objetivos (tiempo final)
        for prop in self.problema.objetivos:
            var = self._obtener_var(prop, longitud_plan)
            clausulas.append([var])  # Los objetivos deben ser verdaderas al final
        
        # 3. Codificar restricciones para cada paso de tiempo
        for t in range(longitud_plan):
            # 3.1. Restricciones de acciones
            for accion in self.problema.acciones:
                # Variable para "acción A ocurre en tiempo t"
                var_accion = self._obtener_var(f"a_{accion.nombre}", t)
                
                # Precondiciones deben ser verdaderas en t para ejecutar acción
                for pre in accion.precondiciones:
                    var_pre = self._obtener_var(pre, t)
                    clausulas.append([-var_accion, var_pre])  # a → pre
                
                # Efectos positivos se hacen verdaderos en t+1
                for efecto in accion.efectos_pos:
                    var_efecto = self._obtener_var(efecto, t+1)
                    clausulas.append([-var_accion, var_efecto])  # a → efecto_pos
                
                # Efectos negativos se hacen falsos en t+1
                for efecto in accion.efectos_neg:
                    var_efecto = self._obtener_var(efecto, t+1)
                    clausulas.append([-var_accion, -var_efecto])  # a → ¬efecto_neg
            
            # 3.2. Restricción de persistencia (frame axioms)
            for prop in self._obtener_todas_proposiciones():
                var_prop_t = self._obtener_var(prop, t)
                var_prop_t1 = self._obtener_var(prop, t+1)
                
                # Acciones que podrían añadir/eliminar esta proposición
                acciones_afectan = [
                    a for a in self.problema.acciones 
                    if prop in a.efectos_pos or prop in a.efectos_neg
                ]
                
                # Si la proposición cambia, alguna acción relevante debe ocurrir
                if acciones_afectan:
                    # ¬prop_t ∧ prop_t+1 → ∨{a | a añade prop}
                    añaden = [a for a in acciones_afectan if prop in a.efectos_pos]
                    if añaden:
                        clausula = [var_prop_t, -var_prop_t1]
                        for a in añaden:
                            clausula.append(self._obtener_var(f"a_{a.nombre}", t))
                        clausulas.append(clausula)
                    
                    # prop_t ∧ ¬prop_t+1 → ∨{a | a elimina prop}
                    eliminan = [a for a in acciones_afectan if prop in a.efectos_neg]
                    if eliminan:
                        clausula = [-var_prop_t, var_prop_t1]
                        for a in eliminan:
                            clausula.append(self._obtener_var(f"a_{a.nombre}", t))
                        clausulas.append(clausula)
            
            # 3.3. Restricción de conflicto: máximo una acción por paso
            vars_acciones = [self._obtener_var(f"a_{a.nombre}", t) for a in self.problema.acciones]
            for a1, a2 in itertools.combinations(vars_acciones, 2):
                clausulas.append([-a1, -a2])  # ¬a1 ∨ ¬a2 (no pueden ser ambas verdaderas)
        
        return clausulas
    
    def _obtener_todas_proposiciones(self) -> Set[str]:
        """Recolecta todas las proposiciones mencionadas en el problema"""
        props = set()
        props.update(self.problema.estado_inicial)
        props.update(self.problema.objetivos)
        for a in self.problema.acciones:
            props.update(a.precondiciones)
            props.update(a.efectos_pos)
            props.update(a.efectos_neg)
        return props
    
    def decodificar_plan(self, modelo: List[int], longitud_plan: int) -> List[Accion]:
        """
        Convierte un modelo SAT en una secuencia de acciones
        
        Args:
            modelo: Asignación de variables del solucionador SAT
            longitud_plan: Longitud del plan a extraer
            
        Returns:
            Lista ordenada de acciones que forman el plan
        """
        plan = []
        modelo_positivo = {abs(v): v > 0 for v in modelo}
        
        # Mapeo inverso de variables
        vars_inversas = {v: k for k, v in self.variables.items()}
        
        for t in range(longitud_plan):
            for a in self.problema.acciones:
                var_key = (f"a_{a.nombre}", t)
                if var_key in self.variables:
                    var_id = self.variables[var_key]
                    if modelo_positivo.get(var_id, False):
                        plan.append(a)
                        break  # Asumimos una acción por paso temporal
        return plan

# ==================== ALGORITMO SATPLAN ====================

class SATPlan:
    """
    Implementa el algoritmo SATPLAN que:
    1. Prueba con diferentes longitudes de plan
    2. Codifica el problema en SAT
    3. Usa un solucionador SAT para encontrar planes
    """
    
    def __init__(self, problema: ProblemaPlanificacion):
        self.problema = problema
        self.codificador = CodificadorSAT(problema)
    
    def encontrar_plan(self, max_longitud=10) -> Optional[List[Accion]]:
        """
        Busca un plan válido probando con diferentes longitudes
        
        Args:
            max_longitud: Máxima longitud de plan a probar
            
        Returns:
            Secuencia de acciones que resuelve el problema o None
        """
        for longitud in range(1, max_longitud + 1):
            print(f"Probando con longitud de plan: {longitud}")
            
            # 1. Codificar el problema
            clausulas = self.codificador.codificar_problema(longitud)
            
            # 2. Resolver con SAT
            with Glucose3(bootstrap_with=clausulas) as solver:
                if solver.solve():
                    # 3. Decodificar el modelo
                    modelo = solver.get_model()
                    plan = self.codificador.decodificar_plan(modelo, longitud)
                    return plan
        return None

# ==================== EJEMPLO: DOMINIO DEL TRANSPORTE ====================

def crear_problema_transporte() -> ProblemaPlanificacion:
    """Configura un problema de transporte de paquetes"""
    
    # Definir acciones
    acciones = [
        Accion(
            nombre="cargar(P,C)",
            precondiciones={"en(P,C)", "libre(C)"},
            efectos_pos={"cargado(P,C)"},
            efectos_neg={"en(P,C)", "libre(C)"}
        ),
        Accion(
            nombre="descargar(P,C)",
            precondiciones={"cargado(P,C)", "en(C,L)"},
            efectos_pos={"en(P,L)", "libre(C)"},
            efectos_neg={"cargado(P,C)"}
        ),
        Accion(
            nombre="mover(C,L1,L2)",
            precondiciones={"en(C,L1)", "conectado(L1,L2)"},
            efectos_pos={"en(C,L2)"},
            efectos_neg={"en(C,L1)"}
        )
    ]
    
    # Estado inicial
    estado_inicial = {
        "en(P1,A)", "en(C,A)", "libre(C)",
        "conectado(A,B)", "conectado(B,A)"
    }
    
    # Objetivo
    objetivos = {"en(P1,B)"}
    
    return ProblemaPlanificacion(acciones, estado_inicial, objetivos)

# ==================== VISUALIZACIÓN ====================

def mostrar_plan(plan: List[Accion]):
    """Muestra el plan encontrado de forma legible"""
    if plan:
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
    else:
        print("\nNo se encontró un plan válido")

# ==================== EJECUCIÓN PRINCIPAL ====================

def main():
    print("=== SISTEMA SATPLAN - PROBLEMA DE TRANSPORTE ===")
    
    # 1. Configurar el problema
    problema = crear_problema_transporte()
    print("Estado inicial:", problema.estado_inicial)
    print("Objetivo:", problema.objetivos)
    
    # 2. Ejecutar SATPLAN
    satplan = SATPlan(problema)
    plan = satplan.encontrar_plan()
    
    # 3. Mostrar resultados
    mostrar_plan(plan)

if __name__ == "__main__":
    main()