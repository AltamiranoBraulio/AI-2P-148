import sympy
from sympy import symbols
from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import is_tautology
from sympy.logic.boolalg import satisfiable

# Paso 1: Definir las variables lógicas
p, q, r, s = symbols('p q r s')

# Paso 2: Pide al usuario que escriba su proposición lógica en Python-style
print("Bienvenido al Analizador Lógico 🚀")
print("Usa estas variables: p, q, r, s")
print("Operadores disponibles:")
print("  & (AND),  | (OR),  ~ (NOT),  >> (IMPLICA),  << (IMPLICADO POR)")
print("Ejemplo: (p & q) >> r")
user_input = input("\nEscribe tu proposición lógica: ")

# Paso 3: Evalúa la proposición escrita por el usuario
try:
    proposicion = eval(user_input)
except Exception as e:
    print("Error en la fórmula lógica:", e)
    exit()

# Paso 4: Muestra la fórmula bonita
print("\n✅ Tu proposición es:", proposicion)

# Paso 5: Mostrar la tabla de verdad
print("\n📊 Tabla de Verdad:")
tabla = sympy.logic.boolalg.truthtable(proposicion)
for fila in tabla:
    print(fila)

# Paso 6: Mostrar forma normal conjuntiva (CNF)
cnf = to_cnf(proposicion, simplify=True)
print("\n🔎 Forma Normal Conjuntiva (CNF):", cnf)

# Paso 7: Verificar si es tautología, contradicción o contingencia
if is_tautology(proposicion):
    print("\n🎉 Resultado: Esta proposición es una TAUTOLOGÍA (siempre verdadera).")
elif not satisfiable(proposicion):
    print("\n❌ Resultado: Esta proposición es una CONTRADICCIÓN (siempre falsa).")
else:
    print("\nℹ️ Resultado: Esta proposición es una CONTINGENCIA (a veces verdadera, a veces falsa).")
