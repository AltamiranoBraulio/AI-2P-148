#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BOOSTING (ADABOOST) - IMPLEMENTACIÓN DIDÁCTICA COMPLETA
=======================================================
Tema Principal: Conjuntos de Hipótesis - Boosting
Características:
- Implementación manual del algoritmo AdaBoost
- Clasificación binaria con múltiples clasificadores débiles
- Visualización del proceso de boosting
- Cálculo de importancia de características
- Métricas de evaluación completas
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# =============================================================================
# CLASIFICADOR DÉBIL PERSONALIZADO (STUMP)
# =============================================================================

class Stump:
    """
    Clasificador débil (Decision Stump) para AdaBoost.
    
    Un Decision Stump es un árbol de decisión con solo un nivel de profundidad.
    
    Atributos:
    - caracteristica: Índice de la característica utilizada para la división
    - umbral: Valor de umbral para la división
    - polaridad: Dirección de la desigualdad (1 o -1)
    - alpha: Peso del clasificador en el ensemble
    - error: Error ponderado del clasificador
    """
    
    def __init__(self):
        self.caracteristica = None
        self.umbral = None
        self.polaridad = 1
        self.alpha = None
        self.error = None
    
    def predecir(self, X):
        """
        Realiza predicciones usando el clasificador débil.
        
        Args:
            X: Datos de entrada (n_samples, n_features)
            
        Returns:
            Predicciones (1 o -1) para cada muestra
        """
        n_muestras = X.shape[0]
        predicciones = np.ones(n_muestras)
        
        # Aplicar la regla de decisión según la polaridad
        if self.polaridad == 1:
            predicciones[X[:, self.caracteristica] < self.umbral] = -1
        else:
            predicciones[X[:, self.caracteristica] > self.umbral] = -1
            
        return predicciones

# =============================================================================
# IMPLEMENTACIÓN DE ADABOOST
# =============================================================================

class AdaBoost:
    """
    Implementación manual del algoritmo AdaBoost para clasificación binaria.
    
    AdaBoost (Adaptive Boosting) combina múltiples clasificadores débiles
    en un ensemble fuerte, ajustando los pesos de las muestras en cada iteración.
    
    Args:
        n_clasificadores: Número de clasificadores débiles a utilizar
    """
    
    def __init__(self, n_clasificadores=50):
        self.n_clasificadores = n_clasificadores
        self.clasificadores = []
        self.importancias_caracteristicas = None
    
    def entrenar(self, X, y):
        """
        Entrena el ensemble AdaBoost.
        
        Args:
            X: Datos de entrenamiento (n_samples, n_features)
            y: Etiquetas de clase (-1 o 1) (n_samples,)
        """
        n_muestras, n_caracteristicas = X.shape
        self.importancias_caracteristicas = np.zeros(n_caracteristicas)
        
        # Inicializar pesos uniformes
        pesos = np.full(n_muestras, 1/n_muestras)
        
        for _ in range(self.n_clasificadores):
            # Crear y entrenar un nuevo clasificador débil
            stump = Stump()
            min_error = float('inf')
            
            # Buscar la mejor característica y umbral
            for caracteristica in range(n_caracteristicas):
                valores_caracteristica = X[:, caracteristica]
                umbrales = np.unique(valores_caracteristica)
                
                for umbral in umbrales:
                    # Probar ambas polaridades
                    for polaridad in [1, -1]:
                        # Predicciones temporales
                        predicciones = np.ones(n_muestras)
                        if polaridad == 1:
                            predicciones[valores_caracteristica < umbral] = -1
                        else:
                            predicciones[valores_caracteristica > umbral] = -1
                        
                        # Calcular error ponderado
                        error = np.sum(pesos[y != predicciones])
                        
                        # Actualizar el mejor stump encontrado
                        if error < min_error:
                            min_error = error
                            stump.caracteristica = caracteristica
                            stump.umbral = umbral
                            stump.polaridad = polaridad
                            stump.error = error
            
            # Calcular alpha (peso del clasificador)
            stump.alpha = 0.5 * np.log((1 - min_error) / (min_error + 1e-10))
            
            # Actualizar pesos de las muestras
            predicciones = stump.predecir(X)
            pesos *= np.exp(-stump.alpha * y * predicciones)
            pesos /= np.sum(pesos)  # Normalizar pesos
            
            # Guardar clasificador y actualizar importancia de características
            self.clasificadores.append(stump)
            self.importancias_caracteristicas[stump.caracteristica] += stump.alpha
    
    def predecir(self, X):
        """
        Realiza predicciones usando el ensemble de clasificadores.
        
        Args:
            X: Datos a predecir (n_samples, n_features)
            
        Returns:
            Predicciones finales (1 o -1)
        """
        predicciones_ensemble = np.zeros(X.shape[0])
        
        # Sumar las predicciones ponderadas de todos los clasificadores
        for stump in self.clasificadores:
            predicciones = stump.predecir(X)
            predicciones_ensemble += stump.alpha * predicciones
        
        # Convertir a etiquetas binarias
        return np.sign(predicciones_ensemble)
    
    def visualizar_proceso(self, X, y, caracteristicas_nombres=None):
        """
        Visualiza el proceso de boosting iterativo.
        
        Args:
            X: Datos para visualización
            y: Etiquetas reales
            caracteristicas_nombres: Nombres de las características (opcional)
        """
        plt.figure(figsize=(12, 8))
        
        # Configurar subplots
        n_filas = int(np.ceil(self.n_clasificadores / 5))
        n_columnas = min(5, self.n_clasificadores)
        
        for i, stump in enumerate(self.clasificadores):
            plt.subplot(n_filas, n_columnas, i+1)
            
            # Crear gráfico de dispersión para las dos primeras características
            plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.6)
            
            # Dibujar la frontera de decisión del stump actual
            if stump.caracteristica == 0:
                plt.axvline(x=stump.umbral, color='black', linestyle='--')
            elif stump.caracteristica == 1:
                plt.axhline(y=stump.umbral, color='black', linestyle='--')
            
            # Configuraciones del gráfico
            plt.title(f"Iter {i+1}\nAlpha: {stump.alpha:.2f}")
            plt.xticks([])
            plt.yticks([])
            
            if caracteristicas_nombres is not None:
                plt.xlabel(caracteristicas_nombres[0] if stump.caracteristica == 0 else "")
                plt.ylabel(caracteristicas_nombres[1] if stump.caracteristica == 1 else "")
        
        plt.tight_layout()
        plt.show()

# =============================================================================
# EJEMPLO PRÁCTICO Y VISUALIZACIÓN
# =============================================================================

if __name__ == "__main__":
    # Generar datos de ejemplo no linealmente separables
    X, y = make_classification(
        n_samples=500, 
        n_features=5, 
        n_informative=3,
        n_redundant=1,
        n_classes=2,
        random_state=42,
        flip_y=0.15  # Introducir ruido
    )
    
    # Convertir etiquetas a -1 y 1 (requerido por AdaBoost)
    y = np.where(y == 0, -1, 1)
    
    # Dividir datos en entrenamiento y prueba
    X_ent, X_prueba, y_ent, y_prueba = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Crear y entrenar AdaBoost
    print("🚀 Entrenando AdaBoost...")
    ada = AdaBoost(n_clasificadores=20)
    ada.entrenar(X_ent, y_ent)
    
    # Evaluar el modelo
    y_pred = ada.predecir(X_prueba)
    precision = accuracy_score(y_prueba, y_pred)
    
    print("\n📊 Resultados de evaluación:")
    print(f"- Precisión: {precision:.2%}")
    print("\nReporte de clasificación:")
    print(classification_report(y_prueba, y_pred, target_names=['Clase -1', 'Clase 1']))
    
    # Mostrar importancia de características
    print("\n🔍 Importancia de características:")
    for i, importancia in enumerate(ada.importancias_caracteristicas):
        print(f"Característica {i}: {importancia:.4f}")
    
    # Visualizar proceso de boosting (solo para 2D)
    if X.shape[1] >= 2:
        print("\n🌱 Visualizando proceso de boosting (primeras 2 características)...")
        ada.visualizar_proceso(X_ent, y_ent, [f"Característica {i}" for i in range(2)])
    
    # Comparar con un solo árbol de decisión
    print("\n🔎 Comparación con un solo árbol de decisión:")
    arbol = DecisionTreeClassifier(max_depth=1, random_state=42)
    arbol.fit(X_ent, y_ent)
    y_pred_arbol = arbol.predict(X_prueba)
    print(f"- Precisión árbol simple: {accuracy_score(y_prueba, y_pred_arbol):.2%}")