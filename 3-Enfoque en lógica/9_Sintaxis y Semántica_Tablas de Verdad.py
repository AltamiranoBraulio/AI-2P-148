import itertools
import operator

# Definimos los operadores lógicos
def AND(a, b):
    return a and b

def OR(a, b):
    return a or b

def NOT(a):
    return not a

def IMPLIES(a, b):
    return not a or b

# Función para evaluar una expresión booleana a partir de una fórmula
def evaluar_formula(fórmula, valores):
    """
    Evaluar la fórmula lógica con valores de verdad dados para las variables.
    """
    # Reemplazamos las variables por sus valores en la fórmula
    for var, valor in valores.items():
        fórmula = fórmula.replace(var, str(valor))
    
    # Reemplazamos los operadores lógicos por sus equivalentes en Python
    fórmula = fórmula.replace("AND", "&").replace("OR", "|").replace("NOT", "~").replace("IMPLIES", "<=")
    
    # Evaluamos la expresión
    return eval(fórmula)

# Función para generar la tabla de verdad
def generar_tabla_verdad(fórmula):
    # Extraemos las variables únicas de la fórmula (asumiendo que son letras A, B, C, etc.)
    variables = sorted(set(c for c in fórmula if c.isalpha()))
    
    # Generar todas las combinaciones posibles de valores de verdad (True/False) para las variables
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    
    # Imprimir encabezado de la tabla
    encabezado = "  ".join(variables) + "  " + fórmula
    print(encabezado)
    
    # Evaluar la fórmula para cada combinación de valores
    for combinacion in combinaciones:
        valores = dict(zip(variables, combinacion))
        resultado = evaluar_formula(fórmula, valores)
        
        # Imprimir los resultados en formato tabular
        print("  ".join(str(v) for v in combinacion), "  ", resultado)

# Entrada de la fórmula lógica
fórmula = input("Introduce la fórmula lógica (por ejemplo, (A AND B) IMPLIES NOT C): ")

# Generar y mostrar la tabla de verdad
generar_tabla_verdad(fórmula)
