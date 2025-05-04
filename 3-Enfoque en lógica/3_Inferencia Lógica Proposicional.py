# 📚 Importamos las funciones necesarias de sympy
# symbols() nos permite crear proposiciones lógicas
# Implies es para crear reglas tipo "Si A entonces B"
# And es para combinar varias proposiciones con "y"
from sympy import symbols
from sympy.logic.boolalg import Implies, And

# Importamos satisfiable, que nos dice si una proposición puede ser verdadera o no
from sympy.logic.inference import satisfiable

# 📝 Definimos nuestras proposiciones (variables booleanas)
# Por ejemplo, "Lluvia" es verdadero si está lloviendo y falso si no.
Lluvia = symbols('Lluvia')      # Proposición: ¿Está lloviendo?
Mojado = symbols('Mojado')      # Proposición: ¿La calle está mojada?
Trueno = symbols('Trueno')      # Proposición: ¿Hay truenos en el cielo?

# 🗂️ Creamos nuestra Base de Conocimiento (KB)
# Esto incluye reglas lógicas y hechos que sabemos como ciertos

# ✅ Regla 1: Si llueve, entonces la calle está mojada (Lluvia → Mojado)
regla1 = Implies(Lluvia, Mojado)

# ✅ Regla 2: Si llueve, entonces hay truenos (Lluvia → Trueno)
regla2 = Implies(Lluvia, Trueno)

# ✅ Hecho: Sabemos que actualmente está lloviendo (Lluvia es True)
hecho = Lluvia

# 🧠 Combinamos todo en la base de conocimiento (KB)
# Usamos And() para decir: todas estas cosas son verdaderas al mismo tiempo
KB = And(regla1, regla2, hecho)

# 🔎 Ahora queremos hacer consultas:
# Queremos saber si podemos inferir (deducir) que la calle está mojada y que hay truenos

# Primera consulta: ¿Está la calle mojada?
consulta1 = Mojado

# Segunda consulta: ¿Hay truenos?
consulta2 = Trueno

# 🔬 Realizamos la inferencia usando "satisfiable"
# Idea: si NO es posible que la KB sea cierta y la consulta sea falsa al mismo tiempo,
# entonces la consulta debe ser verdadera (esto es inferencia lógica)

# ➡️ Probamos si la KB y la negación de la consulta 1 es imposible (es decir, si es una tautología)
resultado1 = satisfiable(And(KB, ~consulta1))

# ➡️ Hacemos lo mismo para la consulta 2
resultado2 = satisfiable(And(KB, ~consulta2))

# 📢 Mostramos los resultados en pantalla

# Si resultado1 es False, significa que la inferencia es válida (la calle está mojada)
if resultado1 == False:
    print("✅ Inferencia: La calle está mojada.")
else:
    print("❌ No podemos concluir que la calle está mojada.")

# Si resultado2 es False, significa que podemos inferir que hay truenos
if resultado2 == False:
    print("✅ Inferencia: Hay truenos.")
else:
    print("❌ No podemos concluir que hay truenos.")
