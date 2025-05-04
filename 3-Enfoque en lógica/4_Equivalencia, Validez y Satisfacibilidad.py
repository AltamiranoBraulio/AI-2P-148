# 📚 Importamos las funciones y módulos necesarios de sympy
from sympy import symbols  # Para crear variables simbólicas lógicas (A, B, C...)
from sympy.logic.boolalg import to_cnf  # Para convertir fórmulas a Forma Normal Conjuntiva (CNF)
from sympy.logic.inference import satisfiable  # Para verificar satisfacibilidad (si existe algún caso que hace verdadera la fórmula)
from sympy.parsing.sympy_parser import parse_expr  # Para convertir texto que escribe el usuario en una expresión lógica

# 👇 Creamos 4 variables lógicas comunes que el usuario puede usar (A, B, C, D)
A, B, C, D = symbols('A B C D')

# 🔥 Definimos una función para analizar cualquier fórmula lógica que el usuario escriba
def analizar_formula(entrada):
    # 📝 Primero, tratamos de convertir el texto ingresado a una fórmula lógica usando parse_expr
    try:
        formula = parse_expr(entrada, evaluate=False)  # No evaluamos de inmediato, solo convertimos a objeto lógico
    except Exception as e:  # Si hay error (por ejemplo, el usuario escribe mal)
        print("❌ Error al interpretar la fórmula:", e)  # Mostramos un mensaje de error
        return  # Salimos de la función

    # 🔍 Mostramos la fórmula lógica que el usuario ingresó ya parseada
    print("\n🔍 Fórmula ingresada:", formula)
    
    # ✅ Usamos satisfiable() para verificar si existe alguna asignación de verdad que haga verdadera la fórmula
    sat_result = satisfiable(formula)
    
    # 🤔 Si satisfiable devuelve un diccionario, entonces la fórmula es satisfacible
    if sat_result:
        print("✅ La fórmula ES satisfacible. Ejemplo de asignación que la hace verdadera:", sat_result)
    else:  # Si devuelve False, no hay ninguna asignación que la haga verdadera
        print("❌ La fórmula NO es satisfacible (es una contradicción).")

    # 🔎 Para verificar validez: una fórmula es válida si su negación NO es satisfacible (es insatisfacible)
    es_valida = satisfiable(~formula) == False  # Si la negación no es satisfacible, entonces es válida
    # ✅ o ❌ Mostramos si es válida o no
    print("🔎 Validez:", "✅ La fórmula ES válida (siempre cierta)" if es_valida else "❌ La fórmula NO es válida (hay casos falsos)")

    # ⚠️ Si la fórmula no es válida, mostramos un contraejemplo: valores que la hacen falsa
    if not es_valida:
        contraejemplo = satisfiable(~formula)  # Buscamos una asignación que haga falsa la fórmula
        print("⚠️ Contraejemplo (asignación que la hace falsa):", contraejemplo)

    # 📦 Mostramos la versión equivalente de la fórmula en Forma Normal Conjuntiva (CNF)
    print("📦 Forma normal conjuntiva (CNF):", to_cnf(formula, simplify=True))


# 🚀 Iniciamos un bucle para que el usuario pueda probar varias fórmulas
print("🧮 Verificador Lógico Proposicional")  # Mensaje inicial
print("Usa variables: A, B, C, D")  # Explicamos qué variables están disponibles
print("Operadores: & (AND), | (OR), ~ (NOT), >> (IMPLICA), == (EQUIVALENTE)")  # Explicamos la sintaxis de operadores

# 🔁 Bucle infinito hasta que el usuario escriba 'salir'
while True:
    entrada = input("\nEscribe una fórmula lógica (o 'salir' para terminar): ")  # Pedimos al usuario que escriba su fórmula
    if entrada.lower() == 'salir':  # Si escribe "salir"
        print("👋 Hasta luego!")  # Mensaje de despedida
        break  # Salimos del bucle y termina el programa
    analizar_formula(entrada)  # Llamamos a la función para analizar la fórmula ingresada
