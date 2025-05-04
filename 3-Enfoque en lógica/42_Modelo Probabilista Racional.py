# -*- coding: utf-8 -*-
"""
MODELO PROBABILISTA RACIONAL PARA DECISIÓN DE INVERSIONES - VERSIÓN CORREGIDA
Autor: DeepSeek Chat
Enfoque: Teoría de la Utilidad Esperada + Inferencia Bayesiana
"""

import numpy as np

# ==================== CONFIGURACIÓN INICIAL ====================
class Config:
    """Clase para almacenar constantes de configuración"""
    # Probabilidades iniciales (priors)
    P_EXITO_INICIAL = 0.3  # 30% probabilidad inicial de éxito
    # Parámetros financieros
    GANANCIA_EXITO = 500000  # Ganancia si la startup tiene éxito
    PERDIDA_FRACASO = 0  # Pérdida si fracasa (se pierde toda la inversión)
    # Probabilidades condicionales (likelihoods)
    PROB_INFORME_POSITIVO_EXITO = 0.8
    PROB_INFORME_POSITIVO_FRACASO = 0.1

# ==================== FUNCIONES DEL MODELO ====================
def calcular_utilidad(inversion: float, resultado: str) -> float:
    """
    Calcula la utilidad monetaria neta de una inversión.
    
    Args:
        inversion: Cantidad invertida (ej. $100,000)
        resultado: "éxito" o "fracaso"
    
    Returns:
        Utilidad neta (ganancia - inversión o -inversión si fracaso)
    """
    if resultado == "éxito":
        return Config.GANANCIA_EXITO - inversion
    return -inversion

def verificar_informe(informe: str) -> str:
    """
    Valida y normaliza la entrada del informe.
    
    Args:
        informe: Cadena de texto con el informe
    
    Returns:
        informe normalizado ("positivo" o "negativo")
    
    Raises:
        ValueError: Si el informe no es válido
    """
    informe = informe.lower().strip()
    if informe in ("positivo", "pos", "p"):
        return "positivo"
    elif informe in ("negativo", "neg", "n"):
        return "negativo"
    raise ValueError("Informe no reconocido. Debe ser 'positivo' o 'negativo'")

def calcular_probabilidad_informe(informe: str, resultado: str) -> float:
    """
    Calcula P(informe|resultado) - probabilidad de observar el informe dado el resultado.
    
    Args:
        informe: "positivo" o "negativo"
        resultado: "éxito" o "fracaso"
    
    Returns:
        Probabilidad condicional
    """
    if informe == "positivo":
        return (Config.PROB_INFORME_POSITIVO_EXITO if resultado == "éxito" 
                else Config.PROB_INFORME_POSITIVO_FRACASO)
    return (1 - Config.PROB_INFORME_POSITIVO_EXITO if resultado == "éxito" 
            else 1 - Config.PROB_INFORME_POSITIVO_FRACASO)

def actualizar_probabilidad_exito(informe: str, prob_exito: float) -> float:
    """
    Actualiza la probabilidad de éxito usando el Teorema de Bayes.
    
    Args:
        informe: "positivo" o "negativo"
        prob_exito: Probabilidad inicial de éxito
    
    Returns:
        Probabilidad posterior P(éxito|informe)
    """
    # Calcular P(informe|éxito) y P(informe|fracaso)
    like_exito = calcular_probabilidad_informe(informe, "éxito")
    like_fracaso = calcular_probabilidad_informe(informe, "fracaso")
    
    # Calcular P(informe)
    prob_informe = (like_exito * prob_exito) + (like_fracaso * (1 - prob_exito))
    
    # Aplicar Teorema de Bayes
    if prob_informe == 0:
        return 0.0  # Evitar división por cero
    return (like_exito * prob_exito) / prob_informe

def calcular_utilidad_esperada(inversion: float, prob_exito: float, informe: str = None) -> dict:
    """
    Calcula la utilidad esperada de invertir vs no invertir.
    
    Args:
        inversion: Monto a invertir
        prob_exito: Probabilidad inicial de éxito
        informe: "positivo" o "negativo" (opcional)
    
    Returns:
        Diccionario con utilidades esperadas para ambas decisiones
    """
    # Actualizar probabilidad si hay informe
    prob_actual = (actualizar_probabilidad_exito(informe, prob_exito) 
                  if informe else prob_exito)
    
    # Calcular utilidades esperadas
    utilidad_invertir = (prob_actual * calcular_utilidad(inversion, "éxito") +
                       (1 - prob_actual) * calcular_utilidad(inversion, "fracaso"))
    utilidad_no_invertir = 0.0
    
    return {
        "Invertir": utilidad_invertir,
        "No invertir": utilidad_no_invertir
    }

# ==================== INTERFAZ DE USUARIO ====================
def obtener_entrada_numerica(mensaje: str, min_val: float = None, max_val: float = None) -> float:
    """
    Solicita y valida una entrada numérica del usuario.
    
    Args:
        mensaje: Mensaje a mostrar al usuario
        min_val: Valor mínimo permitido (opcional)
        max_val: Valor máximo permitido (opcional)
    
    Returns:
        Número válido ingresado por el usuario
    """
    while True:
        try:
            valor = float(input(mensaje))
            if min_val is not None and valor < min_val:
                print(f"Error: El valor debe ser mayor o igual a {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"Error: El valor debe ser menor o igual a {max_val}")
                continue
            return valor
        except ValueError:
            print("Error: Por favor ingrese un número válido")

def obtener_entrada_si_no(mensaje: str) -> bool:
    """
    Solicita una respuesta Sí/No al usuario.
    
    Args:
        mensaje: Mensaje a mostrar
    
    Returns:
        True para Sí, False para No
    """
    while True:
        respuesta = input(mensaje).lower().strip()
        if respuesta in ("s", "si", "sí", "y", "yes"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Error: Por favor responda con 's' o 'n'")

def main():
    """Función principal que ejecuta el sistema experto"""
    print("\n=== MODELO PROBABILISTA RACIONAL PARA DECISIONES DE INVERSIÓN ===")
    print("Este sistema ayuda a evaluar si invertir en una startup basado en análisis de riesgo.\n")
    
    try:
        # Obtener datos del usuario
        inversion = obtener_entrada_numerica("Monto a invertir (ej. 100000): $", min_val=0)
        prob_exito = obtener_entrada_numerica(
            f"Probabilidad inicial de éxito (ej. {Config.P_EXITO_INICIAL}): ",
            min_val=0, max_val=1)
        
        # Preguntar por informe de mercado
        informe = None
        if obtener_entrada_si_no("¿Hay un informe de mercado? (s/n): "):
            while True:
                try:
                    informe = verificar_informe(input("Tipo de informe (positivo/negativo): "))
                    break
                except ValueError as e:
                    print(e)
        
        # Calcular y mostrar resultados
        utilidades = calcular_utilidad_esperada(inversion, prob_exito, informe)
        
        print("\n=== RESULTADOS ===")
        print(f"Probabilidad inicial de éxito: {prob_exito*100:.1f}%")
        if informe:
            prob_actualizada = actualizar_probabilidad_exito(informe, prob_exito)
            print(f"Probabilidad actualizada: {prob_actualizada*100:.1f}%")
        
        print("\nUtilidades esperadas:")
        for decision, utilidad in utilidades.items():
            print(f"- {decision}: ${utilidad:,.2f}")
        
        mejor_decision = max(utilidades.items(), key=lambda x: x[1])[0]
        print(f"\nRECOMENDACIÓN: {mejor_decision.upper()} (utilidad esperada: ${utilidades[mejor_decision]:,.2f})")
    
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")

if __name__ == "__main__":
    main()