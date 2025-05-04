"""
====================================================
JERARQUÍA DE CHOMSKY - CLASIFICACIÓN DE GRAMÁTICAS
====================================================
Objetivo: Dada una gramática formal, determinar a qué tipo pertenece según la Jerarquía de Chomsky.
Tipos:
- Tipo 0 (Irrestrictas)
- Tipo 1 (Sensibles al contexto)
- Tipo 2 (Libres de contexto)
- Tipo 3 (Regulares)
"""

# ======================
# 1. DEFINICIÓN DE GRAMÁTICA
# ======================
# Usamos un diccionario para representar la gramática:
# - Clave: Símbolo no terminal (ej.: 'S')
# - Valor: Lista de producciones (ej.: ['aSb', 'ab'])
gramatica = {
    'S': ['aSb', 'ab']  # Ejemplo: Gramática libre de contexto (Tipo 2)
}

# ======================
# 2. FUNCIÓN PARA VERIFICAR TIPO 3 (REGULAR)
# ======================
def es_tipo_3(gramatica):
    """
    Verifica si la gramática es Tipo 3 (Regular).
    Reglas:
    - Producciones deben ser:
        A → aB (lineal por derecha) o
        A → Ba (lineal por izquierda) o
        A → a
    - Donde A, B son no terminales y 'a' es terminal.
    """
    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            # Caso 1: Producción A → a
            if len(produccion) == 1 and produccion.islower():
                continue
            # Caso 2: Producción A → aB (lineal por derecha)
            elif len(produccion) == 2 and produccion[0].islower() and produccion[1].isupper():
                continue
            # Caso 3: Producción A → Ba (lineal por izquierda)
            elif len(produccion) == 2 and produccion[0].isupper() and produccion[1].islower():
                continue
            else:
                return False
    return True

# ======================
# 3. FUNCIÓN PARA VERIFICAR TIPO 2 (LIBRE DE CONTEXTO)
# ======================
def es_tipo_2(gramatica):
    """
    Verifica si la gramática es Tipo 2 (Libre de contexto).
    Reglas:
    - Todas las producciones son de la forma A → α,
      donde A es un no terminal y α es cualquier cadena.
    """
    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            # Verificar que el lado izquierdo sea un solo no terminal
            if len(no_terminal) != 1 or not no_terminal.isupper():
                return False
    return True

# ======================
# 4. FUNCIÓN PARA VERIFICAR TIPO 1 (SENSIBLE AL CONTEXTO)
# ======================
def es_tipo_1(gramatica):
    """
    Verifica si la gramática es Tipo 1 (Sensible al contexto).
    Reglas:
    - Producciones son de la forma αAβ → αγβ,
      donde A es no terminal, γ no es vacía, y α, β son símbolos terminales/no terminales.
    - Alternativamente: |αAβ| ≤ |αγβ|
    """
    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            # Verificar que la producción no reduzca la longitud
            if len(produccion) < len(no_terminal):
                return False
    return True

# ======================
# 5. FUNCIÓN PARA VERIFICAR TIPO 0 (IRRESTRICTA)
# ======================
def es_tipo_0(gramatica):
    """
    Verifica si la gramática es Tipo 0 (Irrestricta).
    Reglas:
    - No tiene restricciones (todas las gramáticas son Tipo 0 por defecto).
    """
    return True  # Todas las gramáticas son al menos Tipo 0

# ======================
# 6. CLASIFICADOR DE GRAMÁTICAS
# ======================
def clasificar_gramatica(gramatica):
    """
    Clasifica la gramática según la Jerarquía de Chomsky.
    Devuelve el tipo más restrictivo posible.
    """
    if es_tipo_3(gramatica):
        return "Tipo 3 (Regular)"
    elif es_tipo_2(gramatica):
        return "Tipo 2 (Libre de contexto)"
    elif es_tipo_1(gramatica):
        return "Tipo 1 (Sensible al contexto)"
    else:
        return "Tipo 0 (Irrestricta)"

# ======================
# 7. EJEMPLOS DE GRAMÁTICAS
# ======================
gramatica_regular = {
    'S': ['aA', 'bB'],
    'A': ['aA', 'b'],
    'B': ['bB', 'a']
}

gramatica_libre_contexto = {
    'S': ['aSb', 'ab']
}

gramatica_sensible_contexto = {
    'S': ['aSb', 'ab'],
    'aSb': ['aAcBb']  # Ejemplo de producción sensible al contexto
}

gramatica_irrestricta = {
    'S': ['aSb', 'ab'],
    'aSb': ['abba']  # Producción que no cumple |αAβ| ≤ |αγβ|
}

# ======================
# 8. PRUEBA DEL CLASIFICADOR
# ======================
if __name__ == "__main__":
    print("=== CLASIFICACIÓN DE GRAMÁTICAS SEGÚN CHOMSKY ===")
    
    print("\n🔹 Gramática Regular (Tipo 3):")
    print(clasificar_gramatica(gramatica_regular))
    
    print("\n🔹 Gramática Libre de Contexto (Tipo 2):")
    print(clasificar_gramatica(gramatica_libre_contexto))
    
    print("\n🔹 Gramática Sensible al Contexto (Tipo 1):")
    print(clasificar_gramatica(gramatica_sensible_contexto))
    
    print("\n🔹 Gramática Irrestricta (Tipo 0):")
    print(clasificar_gramatica(gramatica_irrestricta))