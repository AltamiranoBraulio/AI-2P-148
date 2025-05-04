"""
SISTEMA DE PLANIFICACIÓN DE ORDEN PARCIAL (POP)
Autor: DeepSeek Chat
Enfoque: Planificación con acciones parcialmente ordenadas para gestión de proyectos

Este sistema implementa un planificador de orden parcial (Partial Order Planning)
que permite establecer relaciones de precedencia flexibles entre acciones,
manteniendo consistencia y resolviendo conflictos potenciales.
"""

# Importación de módulos necesarios
from typing import List, Dict, Set, Tuple, Optional  # Para anotaciones de tipo
from collections import defaultdict  # Para crear diccionarios con valores por defecto
import graphviz  # Para generar visualizaciones de grafos
import random  # Para selección aleatoria en la resolución de amenazas

# ==================== REPRESENTACIÓN DEL PROBLEMA ====================

class Accion:
    """
    Representa una acción en el plan con:
    - nombre: Identificador único de la acción
    - precondiciones: Condiciones que deben ser verdaderas ANTES de ejecutar la acción
    - efectos: Condiciones que se hacen verdaderas DESPUÉS de ejecutar la acción
    - duracion: Tiempo que toma ejecutar la acción (para planificación temporal)
    """
    def __init__(self, nombre: str, 
                 precondiciones: Set[str], 
                 efectos: Set[str], 
                 duracion: int = 1):
        # Inicialización de los atributos de la acción
        self.nombre = nombre  # Nombre identificador de la acción
        self.precondiciones = precondiciones  # Condiciones requeridas para ejecutar
        self.efectos = efectos  # Condiciones que se hacen verdaderas al ejecutar
        self.duracion = duracion  # Duración temporal de la acción (opcional)

    def __repr__(self):
        """Representación string de la acción para debugging"""
        return f"Acción({self.nombre})"  # Ejemplo: "Acción(Cimentación)"


class PlanParcial:
    """
    Representa un plan parcialmente ordenado con:
    - acciones: Todas las acciones incluidas en el plan
    - ordenes: Relaciones de precedencia entre acciones (A debe ejecutarse antes que B)
    - enlaces: Conexiones causales entre acciones (qué acción satisface cada precondición)
    """
    def __init__(self):
        # Inicialización de las estructuras de datos del plan
        self.acciones = set()  # Usamos un set para evitar duplicados
        self.ordenes = set()   # Conjunto de tuplas (A, B) donde A < B
        self.enlaces = dict()  # Diccionario de (proveedor, consumidor) -> precondición

    def agregar_accion(self, accion: Accion):
        """Añade una nueva acción al plan"""
        self.acciones.add(accion)  # Añade al conjunto de acciones

    def agregar_orden(self, accion_anterior: Accion, accion_posterior: Accion):
        """
        Establece que una acción debe ejecutarse antes que otra
        Args:
            accion_anterior: La acción que debe ejecutarse primero
            accion_posterior: La acción que debe ejecutarse después
        """
        self.ordenes.add((accion_anterior, accion_posterior))  # Añade relación de orden

    def agregar_enlace(self, precondicion: str, accion_proveedora: Accion, accion_consumidora: Accion):
        """
        Establece un enlace causal entre acciones:
        - accion_proveedora satisface una precondición de accion_consumidora
        
        Args:
            precondicion: La condición que se está satisfaciendo
            accion_proveedora: La acción que provee la condición
            accion_consumidora: La acción que requiere la condición
        """
        # Validación de que el enlace es correcto
        if precondicion not in accion_proveedora.efectos:
            raise ValueError(f"La acción {accion_proveedora} no provee {precondicion}")
        if precondicion not in accion_consumidora.precondiciones:
            raise ValueError(f"La acción {accion_consumidora} no requiere {precondicion}")
        
        # Registrar el enlace y la relación de orden correspondiente
        self.enlaces[(accion_proveedora, accion_consumidora)] = precondicion
        self.agregar_orden(accion_proveedora, accion_consumidora)  # La proveedora debe ejecutarse antes

    def es_consistente(self) -> bool:
        """
        Verifica si el plan es consistente (no tiene ciclos en las relaciones de orden)
        
        Returns:
            True si el plan es consistente, False si contiene ciclos
        """
        # Construimos un grafo de precedencia
        grafo = defaultdict(list)
        for a1, a2 in self.ordenes:
            grafo[a1].append(a2)  # a1 -> a2
        
        # Detección de ciclos usando DFS (Depth-First Search)
        visitados = set()  # Nodos ya visitados
        en_recursion = set()  # Nodos en el camino actual (para detectar ciclos)

        def tiene_ciclo(accion):
            """Función auxiliar recursiva para detectar ciclos"""
            visitados.add(accion)
            en_recursion.add(accion)
            
            # Explorar todos los vecinos
            for vecino in grafo[accion]:
                if vecino not in visitados:
                    if tiene_ciclo(vecino):  # Llamada recursiva
                        return True
                elif vecino in en_recursion:  # Encontramos un ciclo
                    return True
            
            en_recursion.remove(accion)
            return False

        # Aplicar la detección de ciclos a todas las acciones no visitadas
        for accion in self.acciones:
            if accion not in visitados:
                if tiene_ciclo(accion):
                    return False  # Plan inconsistente
        return True  # Plan consistente

    def visualizar(self):
        """
        Genera una visualización gráfica del plan usando Graphviz
        Crea un archivo 'plan_parcial.png' con la representación visual
        """
        # Crear un nuevo grafo dirigido
        dot = graphviz.Digraph(comment='Plan Parcialmente Ordenado')
        
        # Añadir nodos para cada acción
        for accion in self.acciones:
            # Cada nodo muestra el nombre y duración de la acción
            dot.node(accion.nombre, 
                    label=f"{accion.nombre}\nD={accion.duracion}")
        
        # Añadir arcos para relaciones de orden (negros)
        for a1, a2 in self.ordenes:
            dot.edge(a1.nombre, a2.nombre, color="black")
        
        # Añadir arcos para enlaces causales (azules punteados)
        for (a1, a2), precond in self.enlaces.items():
            dot.edge(a1.nombre, a2.nombre, 
                    label=precond,  # Mostrar la precondición
                    color="blue", 
                    fontcolor="blue",
                    style="dashed")
        
        # Generar y mostrar el archivo de imagen
        dot.render('plan_parcial', view=True, format='png')

# ==================== ALGORITMO DE PLANIFICACIÓN POP ====================

class PlanificadorPOP:
    """
    Implementa el algoritmo de planificación de orden parcial (POP) con:
    - Selección de amenazas: Resolución de conflictos en el plan
    - Criterio de terminación: Todas las precondiciones están satisfechas
    
    El algoritmo sigue estos pasos principales:
    1. Inicializar con acciones de inicio y fin
    2. Seleccionar precondiciones no satisfechas
    3. Añadir acciones que satisfagan precondiciones
    4. Resolver amenazas a los enlaces causales
    5. Repetir hasta que todas las precondiciones estén satisfechas
    """
    def __init__(self, acciones_disponibles: List[Accion]):
        # Lista de todas las acciones disponibles en el dominio
        self.acciones = acciones_disponibles

    def planificar(self, 
                   estado_inicial: Set[str], 
                   objetivos: Set[str], 
                   max_iter=1000) -> Optional[PlanParcial]:
        """
        Genera un plan parcialmente ordenado que alcanza los objetivos
        
        Args:
            estado_inicial: Condiciones verdaderas al inicio
            objetivos: Condiciones que deben ser verdaderas al final
            max_iter: Límite de iteraciones para evitar bucles infinitos
            
        Returns:
            Plan parcialmente ordenado válido o None si no se encuentra solución
        """
        # 1. Crear acciones especiales de inicio y fin
        accion_inicio = Accion("Inicio", set(), estado_inicial)  # Acción inicial (sin precondiciones)
        accion_fin = Accion("Fin", objetivos, set())  # Acción final (sin efectos)
        
        # 2. Inicializar el plan con estas acciones básicas
        plan = PlanParcial()
        plan.agregar_accion(accion_inicio)
        plan.agregar_accion(accion_fin)
        plan.agregar_orden(accion_inicio, accion_fin)  # Inicio debe ejecutarse antes que Fin
        
        # 3. Establecer que el inicio satisface las precondiciones del fin
        for precond in objetivos:
            plan.agregar_enlace(precond, accion_inicio, accion_fin)
        
        # 4. Bucle principal de planificación
        iteracion = 0
        while iteracion < max_iter:
            iteracion += 1
            
            # 4.1 Seleccionar una precondición no satisfecha
            accion_consumidora, precond = self._elegir_precondicion_no_satisfecha(plan)
            if accion_consumidora is None:
                return plan  # ¡Plan completo! Todas las precondiciones están satisfechas
            
            # 4.2 Intentar usar una acción existente que satisfaga la precondición
            accion_proveedora = self._elegir_accion_que_satisface(plan, precond)
            
            if accion_proveedora is None:
                # 4.3 Si no existe, añadir una nueva acción que satisfaga la precondición
                accion_proveedora = self._elegir_accion_disponible(precond)
                if accion_proveedora is None:
                    return None  # No hay acción disponible que satisfaga la precondición
                
                # Añadir la nueva acción al plan con órdenes básicos
                plan.agregar_accion(accion_proveedora)
                plan.agregar_orden(accion_inicio, accion_proveedora)  # Inicio < NuevaAcción
                plan.agregar_orden(accion_proveedora, accion_fin)  # NuevaAcción < Fin
            
            # 4.4 Establecer el enlace causal
            plan.agregar_enlace(precond, accion_proveedora, accion_consumidora)
            
            # 4.5 Resolver amenazas potenciales al nuevo enlace
            if not self._resolver_amenazas(plan):
                return None  # No se pudieron resolver las amenazas
            
        return None  # Se excedió el límite de iteraciones sin encontrar solución

    def _elegir_precondicion_no_satisfecha(self, plan: PlanParcial) -> Tuple[Optional[Accion], Optional[str]]:
        """
        Encuentra una precondición no satisfecha en el plan.
        
        Returns:
            Tupla con (acción_consumidora, precondición) o (None, None) si todas están satisfechas
        """
        for accion in plan.acciones:
            for precond in accion.precondiciones:
                satisfecha = False
                # Verificar si hay algún enlace que satisfaga esta precondición
                for (a1, a2), p in plan.enlaces.items():
                    if a2 == accion and p == precond:
                        satisfecha = True
                        break
                if not satisfecha:
                    return (accion, precond)
        return (None, None)  # Todas las precondiciones están satisfechas

    def _elegir_accion_que_satisface(self, plan: PlanParcial, precond: str) -> Optional[Accion]:
        """
        Busca una acción existente en el plan que pueda satisfacer la precondición
        sin introducir ciclos en las relaciones de orden.
        """
        candidatos = []
        for accion in plan.acciones:
            if precond in accion.efectos:
                # Verificar que añadir accion < accion_consumidora no cree ciclos
                es_valida = True
                for a1, a2 in plan.ordenes:
                    if a2 == accion:
                        # Simular añadir el nuevo orden
                        temp_orden = set(plan.ordenes)
                        temp_orden.add((accion, accion_consumidora))
                        
                        # Verificar ciclos en el grafo temporal
                        grafo = defaultdict(list)
                        for a, b in temp_orden:
                            grafo[a].append(b)
                        
                        # BFS para detectar ciclos
                        visitados = set()
                        cola = [accion_consumidora]
                        while cola:
                            actual = cola.pop(0)
                            if actual == accion:  # Ciclo detectado
                                es_valida = False
                                break
                            visitados.add(actual)
                            for vecino in grafo.get(actual, []):
                                if vecino not in visitados:
                                    cola.append(vecino)
                        
                        if not es_valida:
                            break
                
                if es_valida:
                    candidatos.append(accion)
        
        # Seleccionar aleatoriamente entre los candidatos válidos
        return random.choice(candidatos) if candidatos else None

    def _elegir_accion_disponible(self, precond: str) -> Optional[Accion]:
        """Selecciona una acción del dominio que pueda satisfacer la precondición"""
        candidatos = [a for a in self.acciones if precond in a.efectos]
        return random.choice(candidatos) if candidatos else None

    def _resolver_amenazas(self, plan: PlanParcial) -> bool:
        """
        Resuelve amenazas en el plan (acciones que podrían interferir con enlaces causales)
        mediante promoción (hacer que la amenazante vaya después) o democión (que vaya antes).
        
        Returns:
            True si se resolvieron todas las amenazas, False si no fue posible
        """
        amenazas = self._detectar_amenazas(plan)
        
        for amenaza in amenazas:
            accion_amenazante, (a1, a2), precond = amenaza
            
            # Elegir aleatoriamente entre promoción o democión
            if random.choice([True, False]):
                # Promoción: hacer que la amenazante vaya DESPUÉS de a2
                plan.agregar_orden(a2, accion_amenazante)
            else:
                # Democión: hacer que la amenazante vaya ANTES de a1
                plan.agregar_orden(accion_amenazante, a1)
            
            # Verificar si el plan sigue siendo consistente
            if not plan.es_consistente():
                return False  # La resolución de amenazas hizo el plan inconsistente
        
        return True  # Todas las amenazas resueltas con éxito

    def _detectar_amenazas(self, plan: PlanParcial) -> List[Tuple[Accion, Tuple[Accion, Accion], str]]:
        """
        Detecta acciones que amenazan enlaces causales existentes.
        Una amenaza ocurre cuando una acción podría invalidar un enlace causal.
        
        Returns:
            Lista de tuplas (acción_amenazante, (proveedor, consumidor), precondición)
        """
        amenazas = []
        
        # Para cada enlace causal en el plan
        for (a1, a2), precond in plan.enlaces.items():
            # Buscar acciones que puedan amenazar este enlace
            for accion in plan.acciones:
                if accion != a1 and accion != a2:  # No es ni proveedor ni consumidor
                    if precond in accion.efectos:  # La acción podría invalidar la precondición
                        # Verificar si no hay orden que prevenga la amenaza
                        if (a1, accion) not in plan.ordenes and (accion, a2) not in plan.ordenes:
                            amenazas.append((accion, (a1, a2), precond))
        
        return amenazas

# ==================== EJEMPLO: PLANIFICACIÓN DE CONSTRUCCIÓN ====================

def configurar_ejemplo_construccion():
    """
    Configura un ejemplo de planificación para construcción de una casa.
    Define las acciones disponibles en este dominio.
    
    Returns:
        Lista de acciones del dominio de construcción
    """
    acciones = [
        # Acción: Cimentación (requiere terreno preparado, produce cimentación hecha)
        Accion("Cimentación", 
               precondiciones={"terreno_preparado"}, 
               efectos={"cimentacion_hecha"}, 
               duracion=5),
        
        # Acción: Estructura (requiere cimentación, produce estructura)
        Accion("Estructura", 
               precondiciones={"cimentacion_hecha"}, 
               efectos={"estructura_hecha"}, 
               duracion=10),
        
        # Acción: Techado (requiere estructura, produce techo)
        Accion("Techado", 
               precondiciones={"estructura_hecha"}, 
               efectos={"techado_hecho"}, 
               duracion=7),
        
        # Acción: Instalaciones (requiere estructura, produce instalaciones)
        Accion("Instalaciones", 
               precondiciones={"estructura_hecha"}, 
               efectos={"instalaciones_hechas"}, 
               duracion=8),
        
        # Acción: Acabados (requiere techo e instalaciones, produce casa terminada)
        Accion("Acabados", 
               precondiciones={"techado_hecho", "instalaciones_hechas"}, 
               efectos={"casa_terminada"}, 
               duracion=12),
        
        # Acción: Preparar terreno (no requiere nada, produce terreno preparado)
        Accion("PrepararTerreno", 
               precondiciones=set(), 
               efectos={"terreno_preparado"}, 
               duracion=3)
    ]
    return acciones

def main():
    """
    Función principal que ejecuta el ejemplo de construcción de casa.
    """
    print("=== SISTEMA DE PLANIFICACIÓN DE ORDEN PARCIAL ===")
    print("Ejemplo: Construcción de una casa\n")
    
    # 1. Configurar el problema
    acciones = configurar_ejemplo_construccion()  # Obtener acciones del dominio
    estado_inicial = set()  # Estado inicial vacío (PrepararTerreno generará las condiciones iniciales)
    objetivos = {"casa_terminada"}  # Meta a alcanzar
    
    # 2. Crear y ejecutar planificador
    planificador = PlanificadorPOP(acciones)
    plan = planificador.planificar(estado_inicial, objetivos)
    
    # 3. Mostrar resultados
    if plan:
        print("¡Plan encontrado con éxito!")
        
        # 3.1 Mostrar acciones del plan
        print("\nAcciones en el plan:")
        for accion in plan.acciones:
            print(f"- {accion.nombre} (Duración: {accion.duracion} días)")
        
        # 3.2 Mostrar relaciones de orden
        print("\nÓrdenes parciales:")
        for a1, a2 in plan.ordenes:
            print(f"{a1.nombre} -> {a2.nombre}")
        
        # 3.3 Mostrar enlaces causales
        print("\nEnlaces causales:")
        for (a1, a2), precond in plan.enlaces.items():
            print(f"{a1.nombre} provee '{precond}' para {a2.nombre}")
        
        # 3.4 Generar visualización gráfica
        print("\nGenerando visualización del plan...")
        plan.visualizar()
    else:
        print("No se pudo encontrar un plan válido")

if __name__ == "__main__":
    # Ejecutar el programa principal si se ejecuta este script directamente
    main()