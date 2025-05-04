#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SISTEMA DE VIGILANCIA CON DRONES AUTÓNOMOS
-----------------------------------------
Tema Principal: Vigilancia de Ejecución y Replanificación
Descripción:
    - Un drone debe patrullar una zona con waypoints predefinidos.
    - Durante la ejecución, pueden surgir obstáculos o fallos (batería baja, clima adverso).
    - El sistema monitorea el estado en tiempo real y replanifica si es necesario.
"""

import random
import time
from typing import List, Dict, Tuple, Optional

# =============================================================================
# CLASES BASE PARA MODELAR EL ENTORNO Y EL DRON
# =============================================================================

class Entorno:
    """Representa el entorno de vigilancia con ubicaciones y obstáculos."""
    
    def __init__(self, waypoints: List[str]):
        self.waypoints = waypoints          # Lista de ubicaciones a patrullar (ej: ["A", "B", "C"])
        self.obstaculos = set()             # Conjunto de waypoints bloqueados (ej: {"B"})
        self.clima = "bueno"                # Estado del clima ("bueno", "lluvia", "viento")
    
    def actualizar_obstaculos(self):
        """Simula cambios dinámicos: 20% de probabilidad de obstáculo aleatorio."""
        if random.random() < 0.2 and self.waypoints:
            obstaculo = random.choice(self.waypoints)
            self.obstaculos.add(obstaculo)
            print(f"⚠️ ¡Nuevo obstáculo en waypoint {obstaculo}!")
    
    def actualizar_clima(self):
        """Simula cambios climáticos aleatorios."""
        clima_posible = ["bueno", "lluvia", "viento"]
        self.clima = random.choice(clima_posible)
        print(f"🌤️ Clima actualizado: {self.clima}")

class Drone:
    """Modela el drone autónomo con estados internos."""
    
    def __init__(self, ubicacion: str, bateria: int = 100):
        self.ubicacion = ubicacion          # Ubicación actual del drone
        self.bateria = bateria              # Nivel de batería (0-100)
        self.estado = "listo"               # Estados: "listo", "en_movimiento", "fallo"
    
    def consumir_bateria(self, cantidad: int):
        """Reduce la batería y verifica si es crítica."""
        self.bateria = max(0, self.bateria - cantidad)
        if self.bateria < 20:
            print(f"🔋 ¡Batería crítica ({self.bateria}%)!")
            self.estado = "fallo"
    
    def mover(self, destino: str, entorno: Entorno) -> bool:
        """
        Intenta moverse a un waypoint.
        - Verifica obstáculos, clima y batería.
        - Retorna True si el movimiento fue exitoso.
        """
        if self.estado == "fallo":
            return False
        
        if destino in entorno.obstaculos:
            print(f"🚧 ¡Obstáculo detectado en {destino}!")
            return False
        
        if entorno.clima != "bueno":
            print(f"🌧️ ¡Clima adverso ({entorno.clima})! Movimiento más lento.")
            self.consumir_bateria(15)
        else:
            self.consumir_bateria(10)
        
        time.sleep(1)  # Simula tiempo de movimiento
        self.ubicacion = destino
        print(f"✈️ Drone movido a {destino}. Batería: {self.bateria}%")
        return True

# =============================================================================
# MÓDULO DE VIGILANCIA Y REPLANIFICACIÓN
# =============================================================================

class SistemaVigilancia:
    """Coordina la ejecución, monitoreo y replanificación del drone."""
    
    def __init__(self, drone: Drone, entorno: Entorno):
        self.drone = drone
        self.entorno = entorno
        self.plan_actual = []               # Secuencia de waypoints pendientes
    
    def generar_plan_inicial(self) -> List[str]:
        """Genera un plan inicial de patrulla (orden de waypoints)."""
        return self.entorno.waypoints.copy()
    
    def monitorizar(self) -> bool:
        """
        Verifica el estado del drone y entorno durante la ejecución.
        - Retorna False si hay que replanificar.
        """
        # Chequear batería crítica
        if self.drone.estado == "fallo":
            print("🆘 ¡Fallo detectado! Requiere replanificación.")
            return False
        
        # Chequear clima adverso (replanificar si es lluvia)
        if self.entorno.clima == "lluvia":
            print("☔ ¡Lluvia intensa! Replanificando...")
            return False
        
        # Chequear obstáculos en el próximo waypoint
        if self.plan_actual and self.plan_actual[0] in self.entorno.obstaculos:
            print(f"🔄 Waypoint {self.plan_actual[0]} bloqueado. Replanificando...")
            return False
        
        return True
    
    def replanificar(self) -> List[str]:
        """
        Genera un nuevo plan evitando obstáculos y optimizando batería.
        - Prioriza waypoints cercanos y evita climas adversos.
        """
        # Filtrar waypoints accesibles (no obstruidos)
        waypoints_disponibles = [
            wp for wp in self.entorno.waypoints
            if wp not in self.entorno.obstaculos
        ]
        
        # Si hay lluvia, reducir la ruta a la mitad
        if self.entorno.clima == "lluvia":
            waypoints_disponibles = waypoints_disponibles[:len(waypoints_disponibles)//2]
            print("🔁 Plan acortado por clima adverso.")
        
        # Ordenar por proximidad (simplificado)
        nuevo_plan = sorted(
            waypoints_disponibles,
            key=lambda x: abs(ord(x) - ord(self.drone.ubicacion))  # Distancia ASCII (ej: "A" -> "B")
        )
        
        print(f"📝 Nuevo plan generado: {nuevo_plan}")
        return nuevo_plan
    
    def ejecutar_mision(self):
        """Bucle principal de ejecución con vigilancia continua."""
        self.plan_actual = self.generar_plan_inicial()
        print(f"🚀 Iniciando misión. Plan inicial: {self.plan_actual}")
        
        while self.plan_actual and self.drone.bateria > 0:
            # 1. Monitorear estado actual
            if not self.monitorizar():
                self.plan_actual = self.replanificar()
                if not self.plan_actual:
                    print("❌ No hay waypoints disponibles. Misión abortada.")
                    break
            
            # 2. Ejecutar siguiente acción del plan
            destino = self.plan_actual.pop(0)
            if not self.drone.mover(destino, self.entorno):
                print(f"❌ Fallo al mover a {destino}. Reintentando...")
                self.plan_actual.insert(0, destino)  # Reintentar
            
            # 3. Simular cambios dinámicos en el entorno
            self.entorno.actualizar_obstaculos()
            self.entorno.actualizar_clima()
            time.sleep(1.5)
        
        print("🏁 Misión finalizada.")

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Configuración inicial
    entorno = Entorno(waypoints=["A", "B", "C", "D", "E"])
    drone = Drone(ubicacion="Base", bateria=100)
    sistema = SistemaVigilancia(drone, entorno)
    
    # Iniciar misión
    sistema.ejecutar_mision()