#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MEJOR HIPÓTESIS ACTUAL (MHA) - SISTEMA ADAPTATIVO
=================================================
Tema Principal: Algoritmo de Mejor Hipótesis Actual (MHA)
Características:
- Aprendizaje incremental de hipótesis
- Evaluación en tiempo real de hipótesis candidatas
- Visualización interactiva del espacio de hipótesis
- Mecanismo de poda de hipótesis poco prometedoras
- Integración con modelos de sklearn
- Dataset de ejemplo para diagnóstico médico
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import random
import time

# =============================================================================
# CLASE HIPÓTESIS - REPRESENTA UNA HIPÓTESIS CANDIDATA
# =============================================================================

class Hipotesis:
    """
    Representa una hipótesis en el espacio de búsqueda.
    
    Atributos:
    - reglas: Lista de condiciones que definen la hipótesis
    - precision: Precisión actual de la hipótesis
    - cobertura: Porcentaje de muestras que cubre
    - complejidad: Número de condiciones en la hipótesis
    - ultima_actualizacion: Iteración cuando fue actualizada
    - historial: Registro de desempeño a lo largo del tiempo
    """
    
    def __init__(self, reglas: List[Tuple[str, str, float]]):
        """
        Inicializa una nueva hipótesis.
        
        Args:
            reglas: Lista de tuplas (característica, operador, valor)
                   Ejemplo: [("fiebre", ">", 37.5), ("tos", "==", True)]
        """
        self.reglas = reglas
        self.precision = 0.0
        self.cobertura = 0.0
        self.complejidad = len(reglas)
        self.ultima_actualizacion = 0
        self.historial = {
            'precision': [],
            'cobertura': [],
            'complejidad': []
        }
    
    def evaluar(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Evalúa la hipótesis en un conjunto de datos.
        
        Args:
            X: Datos de entrada (n_samples, n_features)
            y: Etiquetas verdaderas (n_samples,)
            
        Returns:
            Tuple (precision, cobertura)
        """
        mascara = self._aplicar_reglas(X)
        muestras_cubiertas = np.sum(mascara)
        
        if muestras_cubiertas == 0:
            return (0.0, 0.0)
        
        precision = np.mean(y[mascara] == 1)  # Asumimos clase positiva=1
        cobertura = muestras_cubiertas / len(X)
        
        return (precision, cobertura)
    
    def _aplicar_reglas(self, X: np.ndarray) -> np.ndarray:
        """
        Aplica las reglas a los datos de entrada.
        
        Args:
            X: Datos de entrada (n_samples, n_features)
            
        Returns:
            Máscara booleana indicando muestras que cumplen todas las reglas
        """
        mascara = np.ones(X.shape[0], dtype=bool)
        
        for caracteristica, operador, valor in self.reglas:
            if operador == ">":
                mascara &= (X[:, caracteristica] > valor)
            elif operador == "<":
                mascara &= (X[:, caracteristica] < valor)
            elif operador == "==":
                mascara &= (X[:, caracteristica] == valor)
            elif operador == "!=":
                mascara &= (X[:, caracteristica] != valor)
        
        return mascara
    
    def actualizar_desempeno(self, precision: float, cobertura: float, iteracion: int):
        """
        Actualiza las métricas de desempeño de la hipótesis.
        """
        self.precision = precision
        self.cobertura = cobertura
        self.ultima_actualizacion = iteracion
        self.historial['precision'].append(precision)
        self.historial['cobertura'].append(cobertura)
        self.historial['complejidad'].append(self.complejidad)
    
    def __str__(self):
        reglas_str = " AND ".join([f"{f} {op} {v}" for f, op, v in self.reglas])
        return f"Hipótesis: {reglas_str} | Prec: {self.precision:.2f}, Cob: {self.cobertura:.2f}"

# =============================================================================
# CLASE MEJOR HIPÓTESIS ACTUAL (MHA) - ALGORITMO PRINCIPAL
# =============================================================================

class MejorHipotesisActual(BaseEstimator, ClassifierMixin):
    """
    Implementación del algoritmo de Mejor Hipótesis Actual.
    
    Atributos:
    - hipotesis_actual: La mejor hipótesis encontrada hasta el momento
    - hipotesis_candidatas: Lista de hipótesis bajo evaluación
    - historial: Registro de la hipótesis actual a lo largo del tiempo
    - parametros: Diccionario de parámetros del algoritmo
    """
    
    def __init__(self, max_hipotesis: int = 50, prob_mutacion: float = 0.1, 
                 prob_cruce: float = 0.3, generaciones: int = 100):
        """
        Inicializa el algoritmo MHA.
        
        Args:
            max_hipotesis: Número máximo de hipótesis a mantener
            prob_mutacion: Probabilidad de mutar una hipótesis
            prob_cruce: Probabilidad de cruzar dos hipótesis
            generaciones: Número de iteraciones para ejecutar
        """
        self.max_hipotesis = max_hipotesis
        self.prob_mutacion = prob_mutacion
        self.prob_cruce = prob_cruce
        self.generaciones = generaciones
        self.hipotesis_actual = None
        self.hipotesis_candidatas = []
        self.historial = []
        self.mejor_por_generacion = []
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Entrena el algoritmo MHA con los datos proporcionados.
        
        Args:
            X: Datos de entrenamiento (n_samples, n_features)
            y: Etiquetas de clase (n_samples,)
        """
        # 1. Inicialización: crear hipótesis aleatorias simples
        self._inicializar_hipotesis(X, y)
        
        # 2. Bucle de optimización
        for generacion in range(self.generaciones):
            # 2.1 Evaluar todas las hipótesis candidatas
            self._evaluar_hipotesis(X, y, generacion)
            
            # 2.2 Seleccionar la mejor hipótesis actual
            self._seleccionar_mejor_hipotesis()
            
            # 2.3 Registrar progreso
            self._registrar_progreso(generacion)
            
            # 2.4 Generar nuevas hipótesis mediante operadores genéticos
            self._generar_nuevas_hipotesis(X, generacion)
            
            # 2.5 Podar hipótesis poco prometedoras
            self._podar_hipotesis()
    
    def _inicializar_hipotesis(self, X: np.ndarray, y: np.ndarray):
        """
        Genera hipótesis iniciales aleatorias.
        """
        n_caracteristicas = X.shape[1]
        
        for _ in range(self.max_hipotesis):
            # Crear hipótesis con 1-3 reglas aleatorias
            num_reglas = random.randint(1, 3)
            reglas = []
            
            for _ in range(num_reglas):
                caracteristica = random.randint(0, n_caracteristicas - 1)
                operador = random.choice([">", "<", "==", "!="])
                valor = self._generar_valor_aleatorio(X, caracteristica)
                reglas.append((caracteristica, operador, valor))
            
            self.hipotesis_candidatas.append(Hipotesis(reglas))
    
    def _generar_valor_aleatorio(self, X: np.ndarray, caracteristica: int) -> float:
        """
        Genera un valor aleatorio dentro del rango de la característica.
        """
        valores = X[:, caracteristica]
        if isinstance(valores[0], (np.floating, float)):
            return np.random.uniform(np.min(valores), np.max(valores))
        else:
            return random.choice(np.unique(valores))
    
    def _evaluar_hipotesis(self, X: np.ndarray, y: np.ndarray, generacion: int):
        """
        Evalúa todas las hipótesis candidatas.
        """
        for hipotesis in self.hipotesis_candidatas:
            precision, cobertura = hipotesis.evaluar(X, y)
            hipotesis.actualizar_desempeno(precision, cobertura, generacion)
    
    def _seleccionar_mejor_hipotesis(self):
        """
        Selecciona la mejor hipótesis basada en precisión y cobertura.
        """
        # Función de evaluación: combinación de precisión y cobertura
        def evaluacion(h: Hipotesis) -> float:
            return h.precision * h.cobertura
        
        mejor_hipotesis = max(self.hipotesis_candidatas, key=evaluacion)
        
        if self.hipotesis_actual is None or evaluacion(mejor_hipotesis) > evaluacion(self.hipotesis_actual):
            self.hipotesis_actual = mejor_hipotesis
    
    def _registrar_progreso(self, generacion: int):
        """
        Registra el progreso del algoritmo.
        """
        if self.hipotesis_actual:
            self.mejor_por_generacion.append({
                'generacion': generacion,
                'precision': self.hipotesis_actual.precision,
                'cobertura': self.hipotesis_actual.cobertura,
                'complejidad': self.hipotesis_actual.complejidad
            })
    
    def _generar_nuevas_hipotesis(self, X: np.ndarray, generacion: int):
        """
        Genera nuevas hipótesis mediante mutación y cruce.
        """
        nuevas_hipotesis = []
        n_caracteristicas = X.shape[1]
        
        # Operador de mutación
        for hipotesis in self.hipotesis_candidatas:
            if random.random() < self.prob_mutacion:
                reglas = hipotesis.reglas.copy()
                
                # Seleccionar una regla aleatoria para mutar
                idx = random.randint(0, len(reglas) - 1)
                caracteristica, op, valor = reglas[idx]
                
                # Mutar el operador o el valor
                if random.random() < 0.5:
                    nuevo_op = random.choice([">", "<", "==", "!="])
                    reglas[idx] = (caracteristica, nuevo_op, valor)
                else:
                    nuevo_valor = self._generar_valor_aleatorio(X, caracteristica)
                    reglas[idx] = (caracteristica, op, nuevo_valor)
                
                nuevas_hipotesis.append(Hipotesis(reglas))
        
        # Operador de cruce
        if len(self.hipotesis_candidatas) >= 2:
            for _ in range(int(self.prob_cruce * self.max_hipotesis)):
                padre, madre = random.sample(self.hipotesis_candidatas, 2)
                
                # Cruzar las reglas de ambas hipótesis
                min_reglas = min(len(padre.reglas), len(madre.reglas))
                punto_cruce = random.randint(1, min_reglas - 1) if min_reglas > 1 else 1
                
                reglas_nuevas = padre.reglas[:punto_cruce] + madre.reglas[punto_cruce:]
                nuevas_hipotesis.append(Hipotesis(reglas_nuevas))
        
        # Añadir nuevas hipótesis al conjunto
        self.hipotesis_candidatas.extend(nuevas_hipotesis)
    
    def _podar_hipotesis(self):
        """
        Elimina hipótesis poco prometedoras para mantener el límite.
        """
        # Ordenar por evaluación (precisión * cobertura)
        self.hipotesis_candidatas.sort(
            key=lambda h: h.precision * h.cobertura, 
            reverse=True
        )
        
        # Mantener solo las mejores
        self.hipotesis_candidatas = self.hipotesis_candidatas[:self.max_hipotesis]
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Realiza predicciones usando la mejor hipótesis actual.
        """
        if self.hipotesis_actual is None:
            raise ValueError("El modelo no ha sido entrenado aún.")
        
        mascara = self.hipotesis_actual._aplicar_reglas(X)
        predicciones = np.zeros(X.shape[0])
        predicciones[mascara] = 1  # Asumimos clase positiva=1
        
        return predicciones
    
    def visualizar_progreso(self):
        """
        Visualiza el progreso del algoritmo a lo largo de las generaciones.
        """
        if not self.mejor_por_generacion:
            print("No hay datos de progreso para visualizar.")
            return
        
        generaciones = [x['generacion'] for x in self.mejor_por_generacion]
        precisiones = [x['precision'] for x in self.mejor_por_generacion]
        coberturas = [x['cobertura'] for x in self.mejor_por_generacion]
        complejidades = [x['complejidad'] for x in self.mejor_por_generacion]
        
        plt.figure(figsize=(12, 8))
        
        # Gráfico de precisión y cobertura
        plt.subplot(2, 1, 1)
        plt.plot(generaciones, precisiones, label='Precisión', marker='o')
        plt.plot(generaciones, coberturas, label='Cobertura', marker='s')
        plt.xlabel('Generación')
        plt.ylabel('Métrica')
        plt.title('Evolución de Precisión y Cobertura')
        plt.legend()
        plt.grid(True)
        
        # Gráfico de complejidad
        plt.subplot(2, 1, 2)
        plt.plot(generaciones, complejidades, label='Complejidad', marker='^', color='green')
        plt.xlabel('Generación')
        plt.ylabel('Número de Reglas')
        plt.title('Evolución de la Complejidad de la Hipótesis')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

# =============================================================================
# EJEMPLO PRÁCTICO: DIAGNÓSTICO MÉDICO
# =============================================================================

if __name__ == "__main__":
    # Crear dataset de ejemplo para diagnóstico médico
    # Características: [0: Temperatura, 1: Tos, 2: Dolor cabeza, 3: Dolor muscular]
    # Clase: 1 (enfermo), 0 (sano)
    X, y = make_classification(
        n_samples=500,
        n_features=4,
        n_informative=3,
        n_redundant=1,
        n_classes=2,
        random_state=42
    )
    
    # Ajustar rangos para simular datos médicos
    X[:, 0] = np.round(X[:, 0] * 5 + 36, 1)  # Temperatura (36-41°C)
    X[:, 1:] = np.where(X[:, 1:] > 0, 1, 0)  # Síntomas binarios
    
    nombres_caracteristicas = ["Temperatura", "Tos", "Dolor cabeza", "Dolor muscular"]
    nombres_clases = ["Sano", "Enfermo"]
    
    # Dividir en entrenamiento y prueba
    X_ent, X_prueba, y_ent, y_prueba = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Crear y entrenar el modelo MHA
    print("🚀 Entrenando Mejor Hipótesis Actual...")
    mha = MejorHipotesisActual(
        max_hipotesis=30,
        prob_mutacion=0.2,
        prob_cruce=0.4,
        generaciones=50
    )
    
    inicio = time.time()
    mha.fit(X_ent, y_ent)
    fin = time.time()
    
    print(f"\n⏱️ Tiempo de entrenamiento: {fin - inicio:.2f} segundos")
    
    # Evaluar el modelo
    y_pred = mha.predict(X_prueba)
    precision = accuracy_score(y_prueba, y_pred)
    
    print("\n📊 Resultados de evaluación:")
    print(f"- Precisión en prueba: {precision:.2%}")
    print(f"- Mejor hipótesis encontrada:")
    print(mha.hipotesis_actual)
    
    # Visualizar progreso
    print("\n📈 Visualizando progreso del entrenamiento...")
    mha.visualizar_progreso()
    
    # Mostrar ejemplo de predicción
    print("\n🔮 Ejemplo de predicción:")
    muestra = X_prueba[0]
    print(f"Datos de muestra: {dict(zip(nombres_caracteristicas, muestra))}")
    print(f"Clase real: {nombres_clases[y_prueba[0]]}")
    print(f"Predicción: {nombres_clases[y_pred[0]]}")