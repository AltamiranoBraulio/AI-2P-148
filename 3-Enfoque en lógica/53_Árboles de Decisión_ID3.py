#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IMPLEMENTACIÓN CORREGIDA DEL ALGORITMO ID3
"""

import numpy as np
from collections import Counter
import math
from graphviz import Digraph
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

class NodoDecision:
    def __init__(self, atributo=None, umbral=None, valor=None, profundidad=0):
        self.atributo = atributo
        self.umbral = umbral
        self.valor = valor
        self.hijos = {}
        self.profundidad = profundidad
        
    def es_hoja(self):
        return len(self.hijos) == 0
    
    def agregar_hijo(self, valor_atributo, nodo_hijo):
        self.hijos[valor_atributo] = nodo_hijo

class ArbolDecisionID3:
    def __init__(self, max_profundidad=5, min_muestras_division=2, metrica='entropia'):
        self.raiz = None
        self.max_profundidad = max_profundidad
        self.min_muestras_division = min_muestras_division
        self.metrica = metrica.lower()
        
    def _calcular_impureza(self, y):
        conteos = Counter(y)
        total = len(y)
        probabilidades = [count / total for count in conteos.values()]
        
        if self.metrica == 'gini':
            return 1 - sum(p**2 for p in probabilidades)
        else:  # entropía
            return -sum(p * math.log2(p) for p in probabilidades if p > 0)
    
    def _mejor_division(self, X, y, atributos):
        mejor_ganancia = -1
        mejor_atributo = None
        mejor_umbral = None
        impureza_padre = self._calcular_impureza(y)
        
        for atributo in atributos:
            valores = np.unique(X[:, atributo])
            
            if len(valores) < 10:  # Atributo discreto
                ganancia = self._ganancia_discreta(X, y, atributo, impureza_padre)
                if ganancia > mejor_ganancia:
                    mejor_ganancia = ganancia
                    mejor_atributo = atributo
                    mejor_umbral = None
            else:  # Atributo continuo
                umbral, ganancia = self._mejor_umbral_continuo(X, y, atributo, impureza_padre)
                if ganancia > mejor_ganancia:
                    mejor_ganancia = ganancia
                    mejor_atributo = atributo
                    mejor_umbral = umbral
        
        return mejor_atributo, mejor_umbral
    
    def _construir_arbol(self, X, y, atributos, profundidad=0):
        # Criterios de parada
        if (profundidad >= self.max_profundidad or 
            len(np.unique(y)) == 1 or 
            len(y) < self.min_muestras_division):
            return NodoDecision(valor=Counter(y).most_common(1)[0][0], profundidad=profundidad)
        
        # Mejor división
        mejor_atributo, umbral = self._mejor_division(X, y, atributos)
        
        if mejor_atributo is None:
            return NodoDecision(valor=Counter(y).most_common(1)[0][0], profundidad=profundidad)
        
        # Crear nodo
        nodo = NodoDecision(atributo=mejor_atributo, umbral=umbral, profundidad=profundidad)
        nuevos_atributos = [a for a in atributos if a != mejor_atributo]
        
        # Construir subárboles
        if umbral is None:  # Discreto
            for valor in np.unique(X[:, mejor_atributo]):
                mascara = X[:, mejor_atributo] == valor
                hijo = self._construir_arbol(X[mascara], y[mascara], nuevos_atributos, profundidad+1)
                nodo.agregar_hijo(valor, hijo)
        else:  # Continuo
            mascara = X[:, mejor_atributo] <= umbral
            hijo_izq = self._construir_arbol(X[mascara], y[mascara], nuevos_atributos, profundidad+1)
            hijo_der = self._construir_arbol(X[~mascara], y[~mascara], nuevos_atributos, profundidad+1)
            nodo.agregar_hijo(f"<={umbral:.2f}", hijo_izq)
            nodo.agregar_hijo(f">{umbral:.2f}", hijo_der)
        
        return nodo
    
    def entrenar(self, X, y):
        self.raiz = self._construir_arbol(X, y, list(range(X.shape[1])))
    
    def predecir(self, X):
        return np.array([self._predecir_muestra(x, self.raiz) for x in X])
    
    def _predecir_muestra(self, x, nodo):
        if nodo.es_hoja():
            return nodo.valor
        
        valor = x[nodo.atributo]
        
        if nodo.umbral is None:  # Discreto
            if valor in nodo.hijos:
                return self._predecir_muestra(x, nodo.hijos[valor])
            return next(iter(nodo.hijos.values())).valor
        else:  # Continuo
            rama = f"<={nodo.umbral:.2f}" if valor <= nodo.umbral else f">{nodo.umbral:.2f}"
            return self._predecir_muestra(x, nodo.hijos[rama])

if __name__ == "__main__":
    iris = load_iris()
    X, y = iris.data, iris.target
    X_ent, X_test, y_ent, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    arbol = ArbolDecisionID3(max_profundidad=3)
    arbol.entrenar(X_ent, y_ent)
    
    y_pred = arbol.predecir(X_test)
    print(f"Precisión: {np.mean(y_pred == y_test):.2%}")