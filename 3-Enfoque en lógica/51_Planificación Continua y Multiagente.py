#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SISTEMA DE RESCATE MULTIAGENTE CON PLANIFICACIÓN CONTINUA - VERSIÓN CORREGIDA
------------------------------------------------------------------------------
Correcciones implementadas:
1. Solucionado error en asignación/remoción de víctimas
2. Mejorada la sincronización entre tareas pendientes y asignaciones
3. Añadida verificación de existencia antes de remover elementos
4. Mejorado el manejo de errores
"""

import random
import time
from typing import List, Dict, Tuple, Optional
from enum import Enum, auto

# =============================================================================
# ENUMERACIONES Y ESTRUCTURAS BASE
# =============================================================================

class TipoAgente(Enum):
    """Tipos de agentes disponibles en el sistema."""
    DRON = auto()      # Agente aéreo para exploración rápida
    ROBOT = auto()     # Agente terrestre para transporte
    CENTRAL = auto()   # Unidad de coordinación central

class EstadoAgente(Enum):
    """Estados posibles de un agente."""
    DISPONIBLE = auto()
    ASIGNADO = auto()
    EN_RUTA = auto()
    EJECUTANDO = auto()
    FALLO = auto()

class Victima:
    """Representa una víctima en el entorno."""
    def __init__(self, id: int, ubicacion: Tuple[int, int], gravedad: int):
        self.id = id
        self.ubicacion = ubicacion  # Coordenadas (x, y)
        self.gravedad = gravedad   # Nivel de urgencia (1-5)
        self.rescatada = False

    def __str__(self):
        return f"Víctima {self.id} en {self.ubicacion} (Gravedad: {self.gravedad})"

# =============================================================================
# CLASES PARA AGENTES Y PLANIFICACIÓN (CORREGIDAS)
# =============================================================================

class Agente:
    """Clase base para todos los agentes."""
    def __init__(self, id: int, tipo: TipoAgente, ubicacion: Tuple[int, int]):
        self.id = id
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.estado = EstadoAgente.DISPONIBLE
        self.bateria = 100
        self.tarea_actual = None
    
    def actualizar_estado(self, nuevo_estado: EstadoAgente):
        """Cambia el estado del agente y notifica."""
        self.estado = nuevo_estado
        print(f"Agente {self.id} -> {nuevo_estado.name}")

    def consumir_recursos(self, cantidad: int):
        """Reduce la batería y verifica fallos."""
        self.bateria = max(0, self.bateria - cantidad)
        if self.bateria < 15:
            self.actualizar_estado(EstadoAgente.FALLO)
            print(f"⚠️ Agente {self.id} con batería crítica!")

class Dron(Agente):
    """Agente aéreo para exploración y mapeo."""
    def __init__(self, id: int, ubicacion: Tuple[int, int]):
        super().__init__(id, TipoAgente.DRON, ubicacion)
        self.velocidad = 3
    
    def explorar(self, entorno: 'Entorno') -> List[Victima]:
        """Descubre víctimas en un radio de 5 unidades."""
        self.actualizar_estado(EstadoAgente.EJECUTANDO)
        self.consumir_recursos(10)
        
        victimas_descubiertas = [
            v for v in entorno.victimas 
            if not v.rescatada 
            and self._distancia(v.ubicacion) <= 5
        ]
        
        print(f"🛩️ Dron {self.id} encontró {len(victimas_descubiertas)} víctimas.")
        return victimas_descubiertas
    
    def _distancia(self, ubicacion: Tuple[int, int]) -> float:
        """Calcula distancia euclidiana a otra ubicación."""
        return ((self.ubicacion[0] - ubicacion[0])**2 + 
                (self.ubicacion[1] - ubicacion[1])**2)**0.5

class Robot(Agente):
    """Agente terrestre para transporte de víctimas."""
    def __init__(self, id: int, ubicacion: Tuple[int, int]):
        super().__init__(id, TipoAgente.ROBOT, ubicacion)
        self.capacidad = 2
    
    def rescatar(self, victima: Victima, entorno: 'Entorno') -> bool:
        """Intenta rescatar a una víctima."""
        if self.estado == EstadoAgente.FALLO:
            return False
        
        self.actualizar_estado(EstadoAgente.EN_RUTA)
        print(f"🤖 Robot {self.id} en ruta a víctima {victima.id}...")
        
        tiempo_movimiento = self._distancia(victima.ubicacion) * 0.5
        time.sleep(tiempo_movimiento)
        
        self.ubicacion = victima.ubicacion
        self.consumir_recursos(15)
        
        if random.random() < 0.9:
            victima.rescatada = True
            self.actualizar_estado(EstadoAgente.EJECUTANDO)
            print(f"🎉 Víctima {victima.id} rescatada!")
            return True
        else:
            print(f"❌ Fallo en rescate de víctima {victima.id}.")
            return False

# =============================================================================
# SISTEMA DE PLANIFICACIÓN CENTRALIZADA (CORREGIDO)
# =============================================================================

class Coordinador:
    """Coordina la asignación de tareas y replanificación."""
    def __init__(self, agentes: List[Agente], entorno: 'Entorno'):
        self.agentes = agentes
        self.entorno = entorno
        self.tareas_pendientes = []  # Lista de víctimas por rescatar
    
    def asignar_tareas(self):
        """Asigna tareas a agentes con verificación de existencia."""
        for agente in self.agentes:
            if agente.estado != EstadoAgente.DISPONIBLE:
                continue
            
            if isinstance(agente, Dron) and random.random() < 0.7:
                agente.tarea_actual = "Explorar"
                agente.actualizar_estado(EstadoAgente.ASIGNADO)
            
            elif isinstance(agente, Robot) and self.tareas_pendientes:
                victima = self._seleccionar_victima()
                if victima is not None:  # Verificación añadida
                    agente.tarea_actual = f"Rescatar V-{victima.id}"
                    agente.actualizar_estado(EstadoAgente.ASIGNADO)
                    try:
                        self.tareas_pendientes.remove(victima)
                    except ValueError:
                        print(f"⚠️ Víctima {victima.id} no estaba en tareas pendientes")
    
    def _seleccionar_victima(self) -> Optional[Victima]:
        """Selecciona víctima con mayor gravedad solo entre pendientes."""
        if not self.tareas_pendientes:
            return None
        
        return max(self.tareas_pendientes, key=lambda x: x.gravedad)
    
    def actualizar_plan(self, nuevas_victimas: List[Victima]):
        """Añade nuevas víctimas evitando duplicados."""
        for v in nuevas_victimas:
            if v not in self.tareas_pendientes and not v.rescatada:
                self.tareas_pendientes.append(v)
        print(f"📊 Replanificación: {len(self.tareas_pendientes)} tareas pendientes.")
    
    def monitorear_agentes(self):
        """Verifica estados y recupera agentes fallidos."""
        for agente in self.agentes:
            if agente.estado == EstadoAgente.FALLO and agente.bateria > 5:
                agente.actualizar_estado(EstadoAgente.DISPONIBLE)
                print(f"♻️ Agente {agente.id} recuperado.")

class Entorno:
    """Representa el entorno dinámico con víctimas."""
    def __init__(self, dimensiones: Tuple[int, int]):
        self.dimensiones = dimensiones
        self.victimas = self._generar_victimas(10)
    
    def _generar_victimas(self, cantidad: int) -> List[Victima]:
        """Genera víctimas en ubicaciones aleatorias."""
        return [
            Victima(
                id=i,
                ubicacion=(
                    random.randint(0, self.dimensiones[0]),
                    random.randint(0, self.dimensiones[1])
                ),
                gravedad=random.randint(1, 5)
            )
            for i in range(cantidad)
        ]
    
    def agregar_victimas(self, cantidad: int) -> List[Victima]:
        """Simula descubrimiento de nuevas víctimas."""
        nuevas = self._generar_victimas(cantidad)
        self.victimas.extend(nuevas)
        print(f"⚠️ ¡Se agregaron {cantidad} nuevas víctimas!")
        return nuevas

# =============================================================================
# SIMULACIÓN PRINCIPAL (ACTUALIZADA)
# =============================================================================

def simular_mision():
    """Ejecuta la simulación completa con manejo de errores."""
    entorno = Entorno((50, 50))
    agentes = [
        Dron(1, (0, 0)),
        Dron(2, (0, 0)),
        Robot(3, (0, 0)),
        Robot(4, (0, 0))
    ]
    coordinador = Coordinador(agentes, entorno)
    
    print("🚀 INICIANDO MISIÓN DE RESCATE MULTIAGENTE (VERSIÓN CORREGIDA)")
    print(f"Agentes: {len(agentes)} | Víctimas iniciales: {len(entorno.victimas)}")
    
    try:
        for paso in range(1, 11):
            print(f"\n=== PASO {paso} ===")
            
            # Exploración con drones
            for agente in agentes:
                if isinstance(agente, Dron) and agente.estado == EstadoAgente.ASIGNADO:
                    victimas_descubiertas = agente.explorar(entorno)
                    coordinador.actualizar_plan(victimas_descubiertas)
            
            # Rescate con robots
            for agente in agentes:
                if isinstance(agente, Robot) and agente.estado == EstadoAgente.ASIGNADO:
                    agente.ejecutar_tarea(entorno)
            
            # Dinámicas del entorno
            if random.random() < 0.2:
                nuevas = entorno.agregar_victimas(random.randint(1, 3))
                coordinador.actualizar_plan(nuevas)
            
            # Gestión continua
            coordinador.asignar_tareas()
            coordinador.monitorear_agentes()
            
            time.sleep(1)
        
        # Resultados finales
        rescatadas = sum(1 for v in entorno.victimas if v.rescatada)
        print(f"\n🏁 MISIÓN TERMINADA | Víctimas rescatadas: {rescatadas}/{len(entorno.victimas)}")
    
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        print("Deteniendo simulación...")

if __name__ == "__main__":
    simular_mision()