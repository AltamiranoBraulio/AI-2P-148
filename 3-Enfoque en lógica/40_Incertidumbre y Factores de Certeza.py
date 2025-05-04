# -*- coding: utf-8 -*-
"""
Sistema de diagnóstico médico con manejo de incertidumbre y factores de certeza.
Autor: DeepSeek Chat
"""

# ==================== IMPORTAR LIBRERÍAS ====================
import numpy as np  # Para operaciones matemáticas

# ==================== DEFINICIÓN DE ENFERMEDADES Y SÍNTOMAS ====================
# Base de conocimiento: Enfermedades y sus síntomas asociados con factores de certeza (CF).
# CF: 0 (no relacionado) a 1 (totalmente relacionado).
ENFERMEDADES = {
    "Gripe": {
        "Fiebre": 0.9,       # Fiebre alta es muy indicativa de gripe (CF=0.9)
        "Tos": 0.7,          # Tos común en gripe (CF=0.7)
        "Dolor de cabeza": 0.8,  
        "Congestión nasal": 0.4  # Menos común en gripe (CF=0.4)
    },
    "Resfriado": {
        "Fiebre": 0.2,       # Fiebre baja en resfriado (CF=0.2)
        "Tos": 0.8,
        "Dolor de cabeza": 0.5,
        "Congestión nasal": 0.9  # Muy común en resfriado (CF=0.9)
    },
    "Alergia": {
        "Fiebre": 0.1,       # Raro en alergias (CF=0.1)
        "Tos": 0.6,
        "Dolor de cabeza": 0.3,
        "Congestión nasal": 0.95  # Síntoma principal (CF=0.95)
    }
}

# ==================== FUNCIÓN PARA OBTENER SÍNTOMAS DEL USUARIO ====================
def obtener_sintomas():
    """
    Pide al usuario ingresar sus síntomas y su certeza (0 a 1).
    Retorna un diccionario con los síntomas y su certeza.
    Ejemplo: {"Fiebre": 0.8, "Tos": 0.6}
    """
    sintomas_usuario = {}
    sintomas_disponibles = ["Fiebre", "Tos", "Dolor de cabeza", "Congestión nasal"]
    
    print("\n=== Ingresa tus síntomas y su certeza (0 a 1) ===")
    for sintoma in sintomas_disponibles:
        while True:
            try:
                certeza = float(input(f"¿Tienes {sintoma}? (Certeza de 0 a 1, ej. 0.7): "))
                if 0 <= certeza <= 1:
                    sintomas_usuario[sintoma] = certeza
                    break
                else:
                    print("¡Error! La certeza debe estar entre 0 y 1.")
            except ValueError:
                print("¡Error! Ingresa un número válido.")
    
    return sintomas_usuario

# ==================== FUNCIÓN PARA CALCULAR FACTOR DE CERTEZA DE ENFERMEDAD ====================
def calcular_factor_certeza(enfermedad, sintomas_usuario):
    """
    Calcula el factor de certeza (CF) de una enfermedad dada los síntomas del usuario.
    Fórmula: CF_enfermedad = Σ (CF_sintoma_enfermedad * certeza_usuario) / Σ CF_sintoma_enfermedad
    """
    total_cf = 0.0
    total_peso = 0.0
    
    for sintoma, certeza_usuario in sintomas_usuario.items():
        # Obtener el CF del síntoma para esta enfermedad
        cf_sintoma = ENFERMEDADES[enfermedad].get(sintoma, 0.0)
        
        # Sumar al total ponderado (CF_sintoma * certeza_usuario)
        total_cf += cf_sintoma * certeza_usuario
        
        # Sumar al total de pesos (CF_sintoma)
        total_peso += cf_sintoma
    
    # Evitar división por cero
    if total_peso == 0:
        return 0.0
    
    # Calcular el factor de certeza final
    return total_cf / total_peso

# ==================== FUNCIÓN PRINCIPAL ====================
def diagnostico_medico():
    """
    Función principal que:
    1. Obtiene síntomas del usuario.
    2. Calcula el CF para cada enfermedad.
    3. Muestra el diagnóstico con el mayor CF.
    """
    print("===== SISTEMA DE DIAGNÓSTICO MÉDICO CON INCERTIDUMBRE =====")
    
    # Paso 1: Obtener síntomas del usuario
    sintomas_usuario = obtener_sintomas()
    
    # Paso 2: Calcular CF para cada enfermedad
    resultados = {}
    for enfermedad in ENFERMEDADES:
        cf = calcular_factor_certeza(enfermedad, sintomas_usuario)
        resultados[enfermedad] = cf
    
    # Paso 3: Mostrar resultados ordenados por CF
    print("\n=== RESULTADOS DEL DIAGNÓSTICO ===")
    for enfermedad, cf in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
        print(f"{enfermedad}: {cf * 100:.2f}% de certeza")
    
    # Obtener la enfermedad con mayor CF
    diagnostico = max(resultados, key=resultados.get)
    print(f"\nDiagnóstico más probable: {diagnostico}")

# ==================== EJECUTAR EL PROGRAMA ====================
if __name__ == "__main__":
    diagnostico_medico()