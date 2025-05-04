# -*- coding: utf-8 -*-
"""
SISTEMA EXPERTO PARA DIAGNÓSTICO DE FALLAS EN AUTOMÓVILES
Autor: DeepSeek Chat
Tipo: Motor de Inferencia Basado en Reglas (Forward Chaining)
"""

# ==================== IMPORTAR LIBRERÍAS ====================
import sys  # Para manejar la salida del programa

# ==================== BASE DE CONOCIMIENTO (REGLAS) ====================
# Las reglas se definen como diccionarios que relacionan síntomas con diagnósticos.
# Formato: {"síntomas": ["síntoma1", "síntoma2"], "diagnóstico": "falla", "solución": "recomendación"}

REGLA_DIAGNOSTICO = [
    {
        "síntomas": ["El auto no enciende", "No hay sonido al girar la llave"],
        "diagnóstico": "Batería descargada",
        "solución": "Recarga o reemplaza la batería. Verifica los bornes."
    },
    {
        "síntomas": ["El auto no enciende", "El motor hace clic pero no arranca"],
        "diagnóstico": "Problema con el motor de arranque",
        "solución": "Revisa el motor de arranque o el solenoide."
    },
    {
        "síntomas": ["El auto se apaga repentinamente", "Humo negro del escape"],
        "diagnóstico": "Problema en el sistema de combustible",
        "solución": "Limpia o reemplaza los inyectores de combustible."
    },
    {
        "síntomas": ["Sobrecalentamiento del motor", "Fuga de líquido refrigerante"],
        "diagnóstico": "Fuga en el sistema de refrigeración",
        "solución": "Revisa mangueras, radiador y tapa del refrigerante."
    },
    {
        "síntomas": ["Ruido anormal al frenar", "Vibración en el volante"],
        "diagnóstico": "Frenos desgastados",
        "solución": "Reemplaza las pastillas o discos de freno."
    }
]

# ==================== FUNCIÓN PARA OBTENER SÍNTOMAS DEL USUARIO ====================
def obtener_síntomas():
    """
    Pregunta al usuario qué síntomas experimenta y los retorna en una lista.
    """
    síntomas_usuario = []
    print("\n=== SISTEMA EXPERTO DE DIAGNÓSTICO DE AUTOS ===")
    print("Por favor, indica los síntomas que presenta tu vehículo (ingresa 'fin' para terminar):")
    
    while True:
        síntoma = input("> ").strip()  # Elimina espacios en blanco
        
        if síntoma.lower() == "fin":
            break  # Termina el ingreso de síntomas
        
        if síntoma:  # Asegura que no se ingresen cadenas vacías
            síntomas_usuario.append(síntoma)
        else:
            print("⚠️ Por favor, ingresa un síntoma válido o escribe 'fin'.")
    
    return síntomas_usuario

# ==================== FUNCIÓN PARA EVALUAR REGLAS (MOTOR DE INFERENCIA) ====================
def evaluar_reglas(síntomas_usuario):
    """
    Compara los síntomas del usuario con las reglas de diagnóstico.
    Retorna una lista de diagnósticos posibles.
    """
    diagnósticos_posibles = []
    
    # Itera sobre cada regla en la base de conocimiento
    for regla in REGLA_DIAGNOSTICO:
        síntomas_regla = regla["síntomas"]
        # Verifica si TODOS los síntomas de la regla están en los síntomas del usuario
        if all(síntoma in síntomas_usuario for síntoma in síntomas_regla):
            diagnósticos_posibles.append({
                "diagnóstico": regla["diagnóstico"],
                "solución": regla["solución"]
            })
    
    return diagnósticos_posibles

# ==================== FUNCIÓN PARA MOSTRAR RESULTADOS ====================
def mostrar_resultados(diagnósticos):
    """
    Muestra los diagnósticos y soluciones encontrados.
    """
    if not diagnósticos:
        print("\n🔍 No se encontró un diagnóstico claro. Revisa manualmente o consulta un mecánico.")
    else:
        print("\n=== DIAGNÓSTICOS POSIBLES ===")
        for idx, diag in enumerate(diagnósticos, 1):
            print(f"\n{idx}. **{diag['diagnóstico']}**")
            print(f"   Solución: {diag['solución']}")

# ==================== FUNCIÓN PRINCIPAL ====================
def sistema_experto_automotriz():
    """
    Función principal que orquesta el sistema experto:
    1. Obtiene síntomas del usuario.
    2. Evalúa las reglas.
    3. Muestra los diagnósticos.
    """
    síntomas = obtener_síntomas()  # Paso 1: Obtener entrada del usuario
    
    if not síntomas:  # Si no hay síntomas ingresados
        print("❌ No se ingresaron síntomas. Saliendo...")
        sys.exit(0)
    
    diagnósticos = evaluar_reglas(síntomas)  # Paso 2: Evaluar reglas
    
    mostrar_resultados(diagnósticos)  # Paso 3: Mostrar resultados

# ==================== EJECUCIÓN DEL PROGRAMA ====================
if __name__ == "__main__":
    sistema_experto_automotriz()  # Inicia el sistema experto