# 📚 Importamos librerías
from sympy import symbols
from sympy.logic.boolalg import Implies, And
from sympy.logic.inference import satisfiable

# 🎓 Definimos nuestros símbolos lógicos
Humano = symbols('Humano')
Mortal = symbols('Mortal')
Socrates = symbols('Socrates')

# 🗂️ Creamos nuestra base de conocimiento (KB) como una lista de reglas y hechos

# Regla 1: Si alguien es humano, entonces es mortal
regla1 = Implies(Humano, Mortal)

# Hecho 1: Socrates es humano
hecho1 = Implies(Socrates, Humano)

# 🔎 Queremos consultar: ¿Socrates es mortal?
# Creamos la consulta como una implicación
consulta = Implies(Socrates, Mortal)

# 🧠 Combinamos todo en la base de conocimiento
KB = And(regla1, hecho1)

# 🔬 Verificamos si la consulta es satisfacible junto con la KB
resultado = satisfiable(And(KB, ~consulta))

# 📢 Mostramos respuesta
if resultado == False:
    print("✅ Según la base de conocimiento, Socrates es mortal.")
else:
    print("❌ No podemos concluir que Socrates es mortal con la información dada.")
