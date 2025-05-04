import itertools  # Importamos itertools para generar combinaciones de True/False para las variables

# Función que evalúa una expresión lógica usando un diccionario con las asignaciones
def evaluar(expresion, valores):
    return eval(expresion, {}, valores)  # Evalúa la expresión usando los valores asignados a cada variable

# Función para generar y mostrar la tabla de verdad de una expresión lógica
def tabla_verdad(variables, expresion):
    print(f"\nTabla de verdad para: {expresion}")
    print("-" * (len(variables) * 8) + " Resultado")

    es_valida = True       # Suponemos que la fórmula es válida (siempre cierta)
    es_satisfacible = False  # Suponemos que no es satisfacible hasta encontrar un True

    # Genera todas las combinaciones posibles de valores para las variables
    for valores in itertools.product([False, True], repeat=len(variables)):
        asignacion = dict(zip(variables, valores))  # Crea el diccionario {'P': True, 'Q': False, ...}
        resultado = evaluar(expresion, asignacion)  # Evalúa la expresión con esa asignación

        # Prepara y muestra la fila de la tabla de verdad
        fila = "  ".join(f"{asignacion[var]:<5}" for var in variables)
        print(f"{fila}  {resultado}")

        # Comprueba validez: si alguna fila da False, ya no es válida
        if not resultado:
            es_valida = False

        # Comprueba satisfacibilidad: si alguna fila da True, es satisfacible
        if resultado:
            es_satisfacible = True

    return es_valida, es_satisfacible  # Retorna ambos resultados

# Función para verificar si dos expresiones son equivalentes lógicamente
def son_equivalentes(variables, expr1, expr2):
    print(f"\nComparando equivalencia entre:\n 1) {expr1}\n 2) {expr2}")
    equivalentes = True  # Asumimos que son equivalentes hasta que se pruebe lo contrario

    # Genera todas las combinaciones posibles de valores para las variables
    for valores in itertools.product([False, True], repeat=len(variables)):
        asignacion = dict(zip(variables, valores))  # Asigna valores actuales a las variables
        res1 = evaluar(expr1, asignacion)  # Evalúa primera expresión
        res2 = evaluar(expr2, asignacion)  # Evalúa segunda expresión

        # Muestra la comparación
        print(f"Con {asignacion} => {expr1}: {res1}, {expr2}: {res2}")

        # Si alguna combinación da resultados diferentes, no son equivalentes
        if res1 != res2:
            equivalentes = False

    return equivalentes  # Retorna True si son equivalentes en todos los casos

# ======== EJEMPLO ========

# Definimos las variables que se usan en las expresiones
variables = ["P", "Q"]

# Primera expresión lógica: P o Q
expr1 = "(P or Q)"

# Segunda expresión lógica usando la ley de Morgan: no (no P y no Q)
expr2 = "not (not P and not Q)"

# Mostramos la tabla de verdad para expr1
valida1, satis1 = tabla_verdad(variables, expr1)

# Mostramos la tabla de verdad para expr2
valida2, satis2 = tabla_verdad(variables, expr2)

# Comprobamos si expr1 y expr2 son equivalentes
equivalentes = son_equivalentes(variables, expr1, expr2)
print(f"\n🔎 ¿Son equivalentes? {'Sí' if equivalentes else 'No'}")

# Mostramos si expr1 es válida y satisfacible
print(f"\nPara '{expr1}':")
print(f"✅ ¿Es válida (siempre verdadera)? {'Sí' if valida1 else 'No'}")
print(f"✅ ¿Es satisfacible (alguna vez verdadera)? {'Sí' if satis1 else 'No'}")
