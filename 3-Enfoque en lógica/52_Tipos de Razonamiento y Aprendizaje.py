#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AGENTE INTELIGENTE MULTIMODAL: RAZONAMIENTO Y APRENDIZAJE INTEGRADOS
====================================================================
Tema Principal: Tipos de Razonamiento y Aprendizaje
Subtemas Integrados:
1. Razonamiento Basado en Casos (CBR)
2. Aprendizaje por Refuerzo (Q-Learning)
3. Razonamiento Probabilístico (Red Bayesiana)
4. Aprendizaje Supervisado (Clasificador)

Descripción:
    - Agente virtual para diagnóstico médico de emergencias
    - Combina múltiples enfoques de razonamiento/aprendizaje
    - Sistema auto-actualizable con experiencia acumulada
"""

import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
import random
import math
from typing import Dict, List, Tuple, Any, Optional

# =============================================================================
# MÓDULO 1: RAZONAMIENTO BASADO EN CASOS (CBR)
# =============================================================================

class SistemaCBR:
    """Sistema de Razonamiento Basado en Casos para diagnóstico médico."""
    
    def __init__(self):
        self.casos = []  # Base de casos históricos
        self.similitudes = {}  # Cache de similitudes calculadas
        
    def agregar_caso(self, sintomas: Dict[str, Any], diagnostico: str, tratamiento: str):
        """Añade un nuevo caso a la base de conocimiento."""
        self.casos.append({
            'sintomas': sintomas,
            'diagnostico': diagnostico,
            'tratamiento': tratamiento,
            'utilidad': 1.0  # Peso inicial del caso
        })
    
    def _calcular_similitud(self, caso1: Dict, caso2: Dict) -> float:
        """Calcula similitud entre casos usando distancia coseno ponderada."""
        claves = set(caso1['sintomas'].keys()) | set(caso2['sintomas'].keys())
        dot_product = 0
        norm1 = 0
        norm2 = 0
        
        for clave in claves:
            val1 = caso1['sintomas'].get(clave, 0)
            val2 = caso2['sintomas'].get(clave, 0)
            peso = 1.0  # Podría ser ponderado por importancia del síntoma
            dot_product += peso * val1 * val2
            norm1 += peso * (val1 ** 2)
            norm2 += peso * (val2 ** 2)
            
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return (dot_product / (math.sqrt(norm1) * math.sqrt(norm2))) * caso2['utilidad']
    
    def recuperar_casos_similares(self, nuevo_caso: Dict, n: int = 3) -> List[Dict]:
        """Recupera los n casos más similares, considerando su utilidad histórica."""
        # Usar cache si está disponible
        caso_id = str(nuevo_caso)
        if caso_id in self.similitudes:
            return self.similitudes[caso_id]
            
        # Calcular similitudes con todos los casos
        similitudes = []
        for caso in self.casos:
            sim = self._calcular_similitud(nuevo_caso, caso)
            similitudes.append((sim, caso))
        
        # Ordenar por similitud y devolver los mejores
        similitudes.sort(reverse=True, key=lambda x: x[0])
        mejores = [caso for sim, caso in similitudes[:n]]
        
        # Almacenar en cache
        self.similitudes[caso_id] = mejores
        return mejores
    
    def adaptar_solucion(self, casos_similares: List[Dict]) -> Dict[str, Any]:
        """Combina soluciones de casos similares para generar nueva solución."""
        # Estrategia simple: voto mayoritario ponderado por similitud
        diagnosticos = defaultdict(float)
        tratamientos = defaultdict(float)
        
        for caso in casos_similares:
            diagnosticos[caso['diagnostico']] += caso['utilidad']
            tratamientos[caso['tratamiento']] += caso['utilidad']
        
        diagnostico = max(diagnosticos.items(), key=lambda x: x[1])[0]
        tratamiento = max(tratamientos.items(), key=lambda x: x[1])[0]
        
        return {
            'diagnostico': diagnostico,
            'tratamiento': tratamiento,
            'confianza': diagnosticos[diagnostico] / sum(diagnosticos.values())
        }
    
    def actualizar_utilidad(self, caso: Dict, exito: bool):
        """Ajusta la utilidad del caso basado en resultados."""
        factor = 1.1 if exito else 0.9  # Aumentar/disminuir utilidad
        caso['utilidad'] = max(0.1, min(2.0, caso['utilidad'] * factor))

# =============================================================================
# MÓDULO 2: APRENDIZAJE POR REFUERZO (Q-LEARNING)
# =============================================================================

class AgenteRefuerzo:
    """Sistema de Aprendizaje por Refuerzo para gestión de tratamientos."""
    
    def __init__(self, estados: List[str], acciones: List[str]):
        self.estados = estados
        self.acciones = acciones
        self.q_table = defaultdict(lambda: np.zeros(len(acciones)))
        self.alpha = 0.1  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento
        self.epsilon = 0.3  # Probabilidad de exploración
        
    def seleccionar_accion(self, estado: str) -> str:
        """Selecciona acción usando política ε-greedy."""
        if random.random() < self.epsilon:
            return random.choice(self.acciones)  # Exploración
        else:
            idx = np.argmax(self.q_table[estado])
            return self.acciones[idx]  # Explotación
    
    def actualizar_q(self, estado: str, accion: str, recompensa: float, nuevo_estado: str):
        """Actualiza la tabla Q usando la ecuación de Bellman."""
        accion_idx = self.acciones.index(accion)
        mejor_futuro = np.max(self.q_table[nuevo_estado])
        actual = self.q_table[estado][accion_idx]
        
        # Ecuación de Q-Learning
        self.q_table[estado][accion_idx] = actual + self.alpha * (
            recompensa + self.gamma * mejor_futuro - actual
        )

# =============================================================================
# MÓDULO 3: RAZONAMIENTO PROBABILÍSTICO (RED BAYESIANA)
# =============================================================================

class ModeloProbabilistico:
    """Modelo bayesiano para estimar probabilidades de diagnósticos."""
    
    def __init__(self):
        self.modelo = GaussianNB()
        self.encoder = LabelEncoder()
        self.entrenado = False
    
    def entrenar(self, datos: pd.DataFrame, objetivos: pd.Series):
        """Entrena el modelo con datos históricos."""
        datos_codificados = datos.apply(LabelEncoder().fit_transform)
        self.modelo.fit(datos_codificados, objetivos)
        self.entrenado = True
    
    def predecir_proba(self, sintomas: Dict[str, Any]) -> Dict[str, float]:
        """Predice probabilidades para cada diagnóstico posible."""
        if not self.entrenado:
            raise ValueError("Modelo no entrenado")
            
        # Convertir a formato de entrada
        entrada = pd.DataFrame([sintomas])
        entrada_cod = entrada.apply(LabelEncoder().fit_transform)
        
        probas = self.modelo.predict_proba(entrada_cod)[0]
        clases = self.modelo.classes_
        
        return {clase: proba for clase, proba in zip(clases, probas)}

# =============================================================================
# MÓDULO 4: SISTEMA INTEGRADO PRINCIPAL
# =============================================================================

class AgenteDiagnostico:
    """Agente inteligente que integra múltiples enfoques de razonamiento/aprendizaje."""
    
    def __init__(self):
        # Inicializar subsistemas
        self.cbr = SistemaCBR()
        self.rl = AgenteRefuerzo(
            estados=["leve", "moderado", "grave"],
            acciones=["observacion", "medicacion", "hospitalizacion"]
        )
        self.prob = ModeloProbabilistico()
        
        # Cargar conocimiento inicial
        self._cargar_casos_base()
    
    def _cargar_casos_base(self):
        """Carga casos de ejemplo para inicializar el sistema."""
        casos_iniciales = [
            ({"fiebre": 1, "dolor_cabeza": 1}, "gripe", "reposo"),
            ({"fiebre": 2, "dificultad_respirar": 1}, "neumonia", "antibioticos"),
            ({"dolor_pecho": 3, "nauseas": 1}, "infarto", "hospitalizacion")
        ]
        
        for sintomas, diag, trat in casos_iniciales:
            self.cbr.agregar_caso(sintomas, diag, trat)
    
    def diagnosticar(self, sintomas_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """Genera diagnóstico integrando múltiples enfoques."""
        # Paso 1: Razonamiento Basado en Casos
        similares = self.cbr.recuperar_casos_similares({"sintomas": sintomas_paciente})
        solucion_cbr = self.cbr.adaptar_solucion(similares)
        
        # Paso 2: Razonamiento Probabilístico
        try:
            probas = self.prob.predecir_proba(sintomas_paciente)
            diagnostico_prob = max(probas.items(), key=lambda x: x[1])[0]
            confianza_prob = probas[diagnostico_prob]
        except:
            diagnostico_prob = solucion_cbr["diagnostico"]
            confianza_prob = 0.5
        
        # Paso 3: Combinar resultados
        if confianza_prob > solucion_cbr["confianza"]:
            diagnostico_final = diagnostico_prob
            fuente = "modelo_probabilistico"
        else:
            diagnostico_final = solucion_cbr["diagnostico"]
            fuente = "casos_similares"
        
        # Paso 4: Aprendizaje por Refuerzo para tratamiento
        severidad = self._clasificar_severidad(sintomas_paciente)
        accion = self.rl.seleccionar_accion(severidad)
        
        return {
            "diagnostico": diagnostico_final,
            "tratamiento_recomendado": accion,
            "confianza": max(confianza_prob, solucion_cbr["confianza"]),
            "fuente": fuente,
            "casos_similares": [c["diagnostico"] for c in similares]
        }
    
    def _clasificar_severidad(self, sintomas: Dict[str, Any]) -> str:
        """Clasifica la severidad del caso para el módulo de RL."""
        score = sum(sintomas.values()) / len(sintomas) if sintomas else 0
        if score < 1.5:
            return "leve"
        elif score < 2.5:
            return "moderado"
        else:
            return "grave"
    
    def retroalimentar(self, sintomas: Dict, resultado: bool):
        """Actualiza los modelos con retroalimentación."""
        # Actualizar CBR
        caso = {"sintomas": sintomas}
        similares = self.cbr.recuperar_casos_similares(caso)
        for caso_similar in similares:
            self.cbr.actualizar_utilidad(caso_similar, resultado)
        
        # Actualizar RL (simplificado)
        severidad = self._clasificar_severidad(sintomas)
        accion = self.diagnosticar(sintomas)["tratamiento_recomendado"]
        recompensa = 1 if resultado else -1
        self.rl.actualizar_q(severidad, accion, recompensa, severidad)

# =============================================================================
# EJECUCIÓN PRINCIPAL Y DEMOSTRACIÓN
# =============================================================================

if __name__ == "__main__":
    # Inicializar agente
    print("⚕️ Inicializando Agente de Diagnóstico Inteligente...")
    agente = AgenteDiagnostico()
    
    # Simular datos de entrenamiento para el modelo probabilístico
    print("\n📊 Entrenando modelos con datos históricos...")
    datos_ejemplo = pd.DataFrame([
        {"fiebre": 1, "dolor_cabeza": 1, "dolor_garganta": 1},
        {"fiebre": 2, "tos": 1, "dificultad_respirar": 1},
        {"dolor_pecho": 3, "nauseas": 1, "sudoracion": 1}
    ])
    objetivos_ejemplo = pd.Series(["gripe", "neumonia", "infarto"])
    agente.prob.entrenar(datos_ejemplo, objetivos_ejemplo)
    
    # Caso de prueba 1
    print("\n🔍 Analizando nuevo caso...")
    sintomas = {"fiebre": 2, "dolor_cabeza": 1, "tos": 1}
    diagnostico = agente.diagnosticar(sintomas)
    
    print("\n📋 Resultados del Diagnóstico Integrado:")
    print(f"- Diagnóstico: {diagnostico['diagnostico']} (Confianza: {diagnostico['confianza']:.0%})")
    print(f"- Tratamiento recomendado: {diagnostico['tratamiento_recomendado']}")
    print(f"- Fuente principal: {diagnostico['fuente']}")
    print(f"- Casos similares usados: {', '.join(diagnostico['casos_similares'])}")
    
    # Retroalimentación (simulando acierto)
    print("\n🔄 Aprendiendo de la experiencia...")
    agente.retroalimentar(sintomas, True)
    print("Sistemas de conocimiento actualizados con retroalimentación positiva")