#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PLANIFICACIÓN CONDICIONAL PARA ROBOT REPARTIDOR - VERSIÓN CORREGIDA
"""

import random
from typing import Dict, List, Tuple, Optional, Callable

# =============================================================================
# DEFINICIÓN DEL MODELO DEL MUNDO (ESTADOS Y ACCIONES)
# =============================================================================

class Estado:
    """Representa un estado del mundo con variables lógicas."""
    def __init__(self, bateria: int, paquete_entregado: bool, ubicacion: str, obstaculo: bool):
        self.bateria = bateria
        self.paquete_entregado = paquete_entregado
        self.ubicacion = ubicacion
        self.obstaculo = obstaculo

    def __str__(self):
        return f"Batería: {self.bateria}%, Ubicación: {self.ubicacion}, Paquete: {'Entregado' if self.paquete_entregado else 'No entregado'}, Obstáculo: {'Sí' if self.obstaculo else 'No'}"

# =============================================================================
# DEFINICIÓN DE ACCIONES CON EFECTOS PROBABILÍSTICOS
# =============================================================================

def mover(estado_actual: Estado, destino: str) -> Tuple[bool, Optional[Estado]]:
    """
    Acción MOVER: Intenta mover el robot a otra ubicación.
    - Precondición: Batería > 20% y no hay obstáculo.
    - Efectos probabilísticos:
        - 80%: Movimiento exitoso (gasta 10% batería).
        - 20%: Fallo (obstáculo aparece aleatoriamente).
    """
    if estado_actual.bateria <= 20:
        print("¡Batería insuficiente para moverse!")
        return False, None
    
    if estado_actual.obstaculo:
        print("¡Obstáculo detectado! No se puede mover.")
        return False, None
    
    if random.random() < 0.8:
        nuevo_estado = Estado(
            bateria=estado_actual.bateria - 10,
            paquete_entregado=estado_actual.paquete_entregado,
            ubicacion=destino,
            obstaculo=False
        )
        print(f"✅ Movimiento exitoso a {destino}. Batería ahora al {nuevo_estado.bateria}%.")
        return True, nuevo_estado
    else:
        print("❌ ¡Fallo inesperado! Apareció un obstáculo.")
        nuevo_estado = Estado(
            bateria=estado_actual.bateria - 5,
            paquete_entregado=estado_actual.paquete_entregado,
            ubicacion=estado_actual.ubicacion,
            obstaculo=True
        )
        return False, nuevo_estado

def entregar_paquete(estado_actual: Estado) -> Tuple[bool, Optional[Estado]]:
    """
    Acción ENTREGAR: Intenta entregar el paquete.
    - Precondición: Robot está en la ubicación objetivo y batería > 10%.
    """
    if estado_actual.ubicacion != "Oficina":
        print("¡No estás en la ubicación de entrega!")
        return False, None
    
    if random.random() < 0.9:
        nuevo_estado = Estado(
            bateria=estado_actual.bateria - 5,
            paquete_entregado=True,
            ubicacion=estado_actual.ubicacion,
            obstaculo=estado_actual.obstaculo
        )
        print("📦 ¡Paquete entregado con éxito!")
        return True, nuevo_estado
    else:
        print("❌ ¡Fallo en la entrega! Batería crítica.")
        return False, estado_actual

def esquivar_obstaculo(estado_actual: Estado) -> Tuple[bool, Optional[Estado]]:
    """
    Acción ESQUIVAR: Intenta remover un obstáculo.
    - Precondición: Obstáculo presente.
    """
    if not estado_actual.obstaculo:
        print("No hay obstáculos para esquivar.")
        return False, None
    
    nuevo_estado = Estado(
        bateria=estado_actual.bateria - 15,
        paquete_entregado=estado_actual.paquete_entregado,
        ubicacion=estado_actual.ubicacion,
        obstaculo=False
    )
    print("🔄 Obstáculo eliminado.")
    return True, nuevo_estado

# =============================================================================
# ALGORITMO DE PLANIFICACIÓN CONDICIONAL (BACKTRACKING)
# =============================================================================

def planificacion_condicional(estado: Estado, plan_actual: List[str], profundidad_max: int) -> Optional[List[str]]:
    """
    Función recursiva que genera un plan contingente.
    - estado: Estado actual del mundo.
    - plan_actual: Secuencia de acciones acumuladas.
    - profundidad_max: Límite para evitar recursión infinita.
    """
    if estado.paquete_entregado:
        return plan_actual
    
    if profundidad_max <= 0 or estado.bateria <= 0:
        return None
    
    # Definir posibles acciones y sus parámetros
    acciones = [
        (mover, {"destino": "Oficina"}),  # Siempre intentamos mover a "Oficina"
        (entregar_paquete, {}),
        (esquivar_obstaculo, {})
    ]
    
    for accion, kwargs in acciones:
        print(f"\n⚡ Intentando acción: {accion.__name__}")
        
        # Ejecutar acción con sus argumentos
        exito, nuevo_estado = accion(estado, **kwargs)
        
        if exito and nuevo_estado:
            nuevo_plan = plan_actual + [f"{accion.__name__}({', '.join(f'{k}={v}' for k, v in kwargs.items())})"]
            resultado = planificacion_condicional(nuevo_estado, nuevo_plan, profundidad_max - 1)
            if resultado:
                return resultado
        elif nuevo_estado:
            print("🔄 Generando contingencia...")
            nuevo_plan = plan_actual + [f"Fallo_{accion.__name__}"]
            resultado = planificacion_condicional(nuevo_estado, nuevo_plan, profundidad_max - 1)
            if resultado:
                return resultado
    
    return None

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    estado_inicial = Estado(
        bateria=100,
        paquete_entregado=False,
        ubicacion="Almacén",
        obstaculo=False
    )
    
    print("=== INICIO DEL PLANIFICADOR CONDICIONAL ===")
    print(f"Estado inicial: {estado_inicial}")
    
    plan_final = planificacion_condicional(estado_inicial, [], 10)
    
    if plan_final:
        print("\n🎉 ¡Plan contingente encontrado!")
        print(" -> ".join(plan_final))
    else:
        print("\n😵 No se pudo encontrar un plan válido.")