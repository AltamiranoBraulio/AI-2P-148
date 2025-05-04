"""
SISTEMA DE PLANIFICACIÓN HTN (HIERARCHICAL TASK NETWORK)
Autor: DeepSeek Chat
Enfoque: Redes Jerárquicas de Tareas para planificación avanzada

Este sistema implementa un planificador HTN que:
1. Descompone tareas abstractas en subtareas concretas
2. Maneja métodos de descomposición jerárquica
3. Selecciona operadores primitivos ejecutables
"""

from typing import List, Dict, Set, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum, auto
import random

# ==================== ESTRUCTURAS BÁSICAS ====================

class TipoTarea(Enum):
    """Tipos de tareas en la red jerárquica"""
    PRIMITIVA = auto()  # Tarea ejecutable directamente
    ABSTRACT = auto()   # Tarea que requiere descomposición

@dataclass
class Tarea:
    """Representa una tarea con nombre y tipo"""
    nombre: str
    tipo: TipoTarea

    def __str__(self):
        return self.nombre

@dataclass
class Metodo:
    """
    Método de descomposición para tareas abstractas:
    - nombre: Identificador del método
    - tarea: Tarea abstracta que descompone
    - precond: Condiciones requeridas para aplicar el método
    - subtareas: Secuencia de subtareas generadas
    """
    nombre: str
    tarea: Tarea
    precond: Set[str]
    subtareas: List[Tarea]

@dataclass
class Operador:
    """
    Operador primitivo (acción ejecutable):
    - nombre: Identificador del operador
    - precond: Condiciones requeridas
    - efectos_pos: Efectos positivos (añaden)
    - efectos_neg: Efectos negativos (eliminan)
    """
    nombre: str
    precond: Set[str]
    efectos_pos: Set[str]
    efectos_neg: Set[str]

# ==================== DOMINIO HTN ====================

class DominioHTN:
    """Contiene toda la definición del dominio HTN"""
    def __init__(self):
        self.tareas: Dict[str, Tarea] = {}          # Todas las tareas por nombre
        self.metodos: List[Metodo] = []             # Métodos de descomposición
        self.operadores: Dict[str, Operador] = {}   # Operadores primitivos
    
    def agregar_tarea(self, nombre: str, tipo: TipoTarea) -> Tarea:
        """Registra una nueva tarea en el dominio"""
        tarea = Tarea(nombre, tipo)
        self.tareas[nombre] = tarea
        return tarea
    
    def agregar_metodo(self, nombre: str, tarea: Tarea, precond: Set[str], subtareas: List[Tarea]) -> Metodo:
        """Añade un método de descomposición para una tarea abstracta"""
        metodo = Metodo(nombre, tarea, precond, subtareas)
        self.metodos.append(metodo)
        return metodo
    
    def agregar_operador(self, nombre: str, precond: Set[str], efectos_pos: Set[str], efectos_neg: Set[str]) -> Operador:
        """Registra un nuevo operador primitivo"""
        operador = Operador(nombre, precond, efectos_pos, efectos_neg)
        self.operadores[nombre] = operador
        return operador
    
    def obtener_metodos_para_tarea(self, tarea: Tarea) -> List[Metodo]:
        """Devuelve todos los métodos aplicables a una tarea abstracta"""
        return [m for m in self.metodos if m.tarea.nombre == tarea.nombre]

# ==================== PLANIFICADOR HTN ====================

class PlanificadorHTN:
    """Implementa el algoritmo de planificación HTN"""
    
    def __init__(self, dominio: DominioHTN):
        self.dominio = dominio
    
    def planificar(self, tarea_raiz: Tarea, estado: Set[str], max_profundidad=10) -> Optional[List[str]]:
        """
        Genera un plan ejecutable descomponiendo la tarea raiz
        
        Args:
            tarea_raiz: Tarea inicial a planificar
            estado: Estado inicial del mundo
            max_profundidad: Límite para evitar recursión infinita
            
        Returns:
            Lista de nombres de operadores o None si no se encuentra plan
        """
        return self._descomponer_tarea(tarea_raiz, estado, [], max_profundidad)
    
    def _descomponer_tarea(self, tarea: Tarea, estado: Set[str], plan_parcial: List[str], profundidad: int) -> Optional[List[str]]:
        """
        Función recursiva para descomponer tareas
        
        Args:
            tarea: Tarea actual a descomponer
            estado: Estado actual del mundo
            plan_parcial: Plan acumulado hasta ahora
            profundidad: Nivel actual de recursión
            
        Returns:
            Plan completo o None si falla la descomposición
        """
        # Caso base: evitar recursión infinita
        if profundidad <= 0:
            return None
        
        # Caso 1: Tarea primitiva (operador)
        if tarea.tipo == TipoTarea.PRIMITIVA:
            operador = self.dominio.operadores.get(tarea.nombre)
            if operador and operador.precond.issubset(estado):
                # Aplicar efectos del operador
                nuevo_estado = estado.copy()
                nuevo_estado.difference_update(operador.efectos_neg)
                nuevo_estado.update(operador.efectos_pos)
                
                # Añadir al plan y continuar
                nuevo_plan = plan_parcial.copy()
                nuevo_plan.append(operador.nombre)
                return nuevo_plan
            return None
        
        # Caso 2: Tarea abstracta (descomponer)
        else:
            # Obtener métodos aplicables (que cumplen precondiciones)
            metodos = [m for m in self.dominio.obtener_metodos_para_tarea(tarea) 
                      if m.precond.issubset(estado)]
            
            # Probar métodos en orden aleatorio (búsqueda no determinista)
            for metodo in random.sample(metodos, len(metodos)):
                plan_actual = plan_parcial.copy()
                estado_actual = estado.copy()
                exito = True
                
                # Intentar descomponer cada subtarea
                for subtarea in metodo.subtareas:
                    resultado = self._descomponer_tarea(
                        subtarea, estado_actual, plan_actual, profundidad - 1)
                    
                    if resultado is None:
                        exito = False
                        break
                    
                    plan_actual = resultado
                    # Actualizar estado según las acciones ya planificadas
                    for accion in plan_actual[len(plan_parcial):]:
                        op = self.dominio.operadores[accion]
                        estado_actual.difference_update(op.efectos_neg)
                        estado_actual.update(op.efectos_pos)
                
                if exito:
                    return plan_actual
        
        return None  # No se pudo descomponer

# ==================== EJEMPLO: DOMINIO DE CONSTRUCCIÓN ====================

def configurar_dominio_construccion() -> DominioHTN:
    """Configura un dominio HTN para construcción de casas"""
    dominio = DominioHTN()
    
    # Definir tareas
    construir_casa = dominio.agregar_tarea("construir_casa", TipoTarea.ABSTRACT)
    cimentacion = dominio.agregar_tarea("hacer_cimentacion", TipoTarea.PRIMITIVA)
    estructura = dominio.agregar_tarea("construir_estructura", TipoTarea.PRIMITIVA)
    techo = dominio.agregar_tarea("colocar_techo", TipoTarea.PRIMITIVA)
    instalaciones = dominio.agregar_tarea("instalar_instalaciones", TipoTarea.PRIMITIVA)
    acabados = dominio.agregar_tarea("aplicar_acabados", TipoTarea.PRIMITIVA)
    
    # Método 1: Construcción estándar
    dominio.agregar_metodo(
        "metodo_estandar", construir_casa,
        {"terreno_preparado"},
        [cimentacion, estructura, techo, instalaciones, acabados]
    )
    
    # Método 2: Construcción rápida (techo antes de instalaciones)
    dominio.agregar_metodo(
        "metodo_rapido", construir_casa,
        {"terreno_preparado", "permiso_rapido"},
        [cimentacion, estructura, techo, instalaciones, acabados]
    )
    
    # Operadores primitivos
    dominio.agregar_operador(
        "hacer_cimentacion",
        {"terreno_preparado"},
        {"cimentacion_hecha"},
        {"terreno_preparado"}
    )
    
    dominio.agregar_operador(
        "construir_estructura",
        {"cimentacion_hecha"},
        {"estructura_hecha"},
        {"cimentacion_hecha"}
    )
    
    dominio.agregar_operador(
        "colocar_techo",
        {"estructura_hecha"},
        {"techo_colocado"},
        set()
    )
    
    dominio.agregar_operador(
        "instalar_instalaciones",
        {"estructura_hecha"},
        {"instalaciones_instaladas"},
        set()
    )
    
    dominio.agregar_operador(
        "aplicar_acabados",
        {"techo_colocado", "instalaciones_instaladas"},
        {"casa_terminada"},
        set()
    )
    
    return dominio

# ==================== EJECUCIÓN PRINCIPAL ====================

def main():
    print("=== PLANIFICADOR HTN - CONSTRUCCIÓN DE CASA ===")
    
    # 1. Configurar dominio y problema
    dominio = configurar_dominio_construccion()
    estado_inicial = {"terreno_preparado", "permiso_rapido"}
    tarea_raiz = dominio.tareas["construir_casa"]
    
    # 2. Crear y ejecutar planificador
    planificador = PlanificadorHTN(dominio)
    plan = planificador.planificar(tarea_raiz, estado_inicial)
    
    # 3. Mostrar resultados
    if plan:
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
    else:
        print("\nNo se pudo encontrar un plan válido")

if __name__ == "__main__":
    main()