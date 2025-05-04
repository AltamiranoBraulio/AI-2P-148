# Importamos las librerías necesarias de sympy
from sympy import symbols  # Para definir las variables simbólicas en las fórmulas lógicas
from sympy.logic.boolalg import to_cnf, Or, And, Not  # Para manipular y convertir las fórmulas a CNF (Forma Normal Conjuntiva) y operadores lógicos
from sympy.logic.inference import satisfiable  # Para determinar si una fórmula es satisfacible
from sympy.parsing.sympy_parser import parse_expr  # Para analizar las fórmulas lógicas ingresadas por el usuario
from sympy.logic.boolalg import is_tautology  # Para verificar si una fórmula es una tautología (si es válida en todos los casos)

# 🚀 Función para verificar si dos fórmulas son equivalentes
def verificar_equivalencia(formula1, formula2):
    # La función 'equals' compara dos fórmulas y devuelve True si son equivalentes
    if formula1.equals(formula2):  # Si las fórmulas son equivalentes
        print("✅ Las fórmulas son equivalentes.")  # Mensaje de confirmación si son equivalentes
    else:
        print("⚠️ Las fórmulas NO son equivalentes.")  # Mensaje de advertencia si no son equivalentes

# 🎯 Función para convertir una fórmula a su Forma Normal Conjuntiva (CNF)
def convertir_a_cnf(formula):
    cnf = to_cnf(formula, simplify=True)  # Convierte la fórmula a su forma normal conjuntiva (FNC) y la simplifica
    return cnf  # Retorna la fórmula convertida a CNF

# 🔄 Función para aplicar la resolución a un conjunto de cláusulas
def resolver(clausulas):
    nuevos = set()  # Usamos un set para almacenar los nuevos resolventes generados
    # Convertimos las cláusulas a conjuntos de literales para que sea más fácil comparar
    clausulas = [set([c]) if not isinstance(c.args, tuple) else set(c.args) for c in clausulas]

    # Bucle principal de resolución
    while True:
        # Generamos todos los pares posibles de cláusulas para intentar resolverlas
        pares = [(clausulas[i], clausulas[j]) for i in range(len(clausulas)) for j in range(i + 1, len(clausulas))]
        for (ci, cj) in pares:  # Iteramos sobre cada par de cláusulas
            for di in ci:  # Iteramos sobre cada literal en la primera cláusula
                for dj in cj:  # Iteramos sobre cada literal en la segunda cláusula
                    # Si encontramos literales opuestos, los resolvemos (eliminamos los literales opuestos)
                    if di == ~dj or ~di == dj:
                        # Generamos el resolvente, que es la unión de las cláusulas sin los literales opuestos
                        resolvente = (ci - {di}) | (cj - {dj})
                        if not resolvente:
                            print("🎯 Se llegó a una cláusula vacía: fórmula insatisfacible (es válida)")
                            return True  # Si obtenemos una cláusula vacía, la fórmula es insatisfacible (es válida)
                        nuevos.add(frozenset(resolvente))  # Añadimos el resolvente a los nuevos resolventes
        # Si los nuevos resolventes no agregan nada nuevo, terminamos
        if nuevos.issubset(map(frozenset, clausulas)):
            return False  # Si no se generaron más resolventes, la fórmula no es satisfacible
        for n in nuevos:  # Añadimos los nuevos resolventes a las cláusulas
            if set(n) not in clausulas:  # Si el resolvente no está ya en las cláusulas
                clausulas.append(set(n))  # Lo añadimos a la lista de cláusulas

# ✅ Función para generar la tabla de verdad de una fórmula lógica
def tabla_de_verdad(formula, variables):
    from itertools import product  # Usamos product para generar todas las combinaciones posibles de valores de verdad
    result = []  # Lista para almacenar los resultados de la tabla de verdad
    # Generamos todas las combinaciones posibles de valores de verdad para las variables
    for valores in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, valores))  # Creamos un diccionario que asigna valores de verdad a las variables
        result.append([assignment, formula.subs(assignment)])  # Evaluamos la fórmula con la asignación de valores y la añadimos al resultado
    return result  # Retorna la lista con la tabla de verdad

# Función principal para interactuar con el usuario
def main():
    # Definimos las variables lógicas que usaremos
    A, B, C = symbols('A B C')

    print("🧩 Bienvenido al Verificador Lógico")  # Mensaje inicial de bienvenida

    while True:  # Bucle principal para seguir pidiendo fórmulas
        # Entrada de fórmulas por parte del usuario
        entrada1 = input("\nIngresa la primera fórmula (o 'salir' para terminar): ")
        if entrada1.lower() == 'salir':  # Si el usuario escribe 'salir', terminamos el programa
            break
        entrada2 = input("Ingresa la segunda fórmula: ")

        try:
            # Intentamos parsear las fórmulas ingresadas por el usuario
            formula1 = parse_expr(entrada1, evaluate=False)  # Convertimos la cadena de texto en una expresión lógica
            formula2 = parse_expr(entrada2, evaluate=False)  # Hacemos lo mismo con la segunda fórmula
        except Exception as e:  # Si ocurre algún error durante el parseo, mostramos un mensaje de error
            print("❌ Error al interpretar:", e)
            continue  # Volvemos a pedir las fórmulas si ocurrió un error

        print("\n📦 Fórmula 1:", formula1)  # Mostramos la primera fórmula
        print("📦 Fórmula 2:", formula2)  # Mostramos la segunda fórmula

        # Verificamos si las fórmulas son equivalentes
        verificar_equivalencia(formula1, formula2)

        # Convertimos ambas fórmulas a CNF (Forma Normal Conjuntiva)
        cnf1 = convertir_a_cnf(formula1)
        cnf2 = convertir_a_cnf(formula2)

        print("📚 Forma Normal Conjuntiva (FNC) de Fórmula 1:", cnf1)  # Mostramos la FNC de la primera fórmula
        print("📚 Forma Normal Conjuntiva (FNC) de Fórmula 2:", cnf2)  # Mostramos la FNC de la segunda fórmula

        # Aplicamos resolución para determinar si las fórmulas son válidas
        print("\n🔄 Resolviendo Fórmula 1...")
        clausulas1 = extraer_clausulas(cnf1)  # Extraemos las cláusulas de la CNF de la fórmula 1
        valido1 = resolver(clausulas1)  # Aplicamos la resolución sobre las cláusulas de la fórmula 1
        if valido1:  # Si la fórmula 1 es válida
            print("✅ Fórmula 1 es válida.")
        else:  # Si la fórmula 1 no es válida
            print("⚠️ Fórmula 1 NO es válida.")

        print("\n🔄 Resolviendo Fórmula 2...")
        clausulas2 = extraer_clausulas(cnf2)  # Extraemos las cláusulas de la CNF de la fórmula 2
        valido2 = resolver(clausulas2)  # Aplicamos la resolución sobre las cláusulas de la fórmula 2
        if valido2:  # Si la fórmula 2 es válida
            print("✅ Fórmula 2 es válida.")
        else:  # Si la fórmula 2 no es válida
            print("⚠️ Fórmula 2 NO es válida.")

        # Generamos la tabla de verdad para ambas fórmulas
        variables = [A, B, C]  # Definimos las variables que usaremos en las tablas de verdad
        print("\n🔎 Tabla de verdad para la Fórmula 1:")
        t1 = tabla_de_verdad(formula1, variables)  # Generamos la tabla de verdad de la fórmula 1
        for entrada, valor in t1:  # Iteramos sobre las entradas y sus valores en la tabla de verdad
            print(f"{entrada} => {valor}")  # Mostramos cada asignación de valores y el resultado de la fórmula

        print("\n🔎 Tabla de verdad para la Fórmula 2:")
        t2 = tabla_de_verdad(formula2, variables)  # Generamos la tabla de verdad de la fórmula 2
        for entrada, valor in t2:  # Iteramos sobre las entradas y sus valores en la tabla de verdad
            print(f"{entrada} => {valor}")  # Mostramos cada asignación de valores y el resultado de la fórmula

# Ejecutamos el programa si es que este archivo es el principal
if __name__ == "__main__":
    main()
