import random

# -------------------------------------
# Contexto:
# Hay una enfermedad E que puede causar dos síntomas: Fiebre (F) y Tos (T)
# Las probabilidades son las siguientes:
#
# P(E) -> Probabilidad de tener la enfermedad
# P(F|E) -> Probabilidad de tener fiebre si tienes la enfermedad
# P(F|¬E) -> Probabilidad de tener fiebre si NO tienes la enfermedad
# P(T|E) -> Probabilidad de tener tos si tienes la enfermedad
# P(T|¬E) -> Probabilidad de tener tos si NO tienes la enfermedad
# -------------------------------------

# Definimos las probabilidades
P_E = 0.1            # 10% de probabilidad de tener la enfermedad
P_F_given_E = 0.8    # 80% de fiebre si tiene la enfermedad
P_F_given_not_E = 0.1 # 10% de fiebre si no tiene la enfermedad
P_T_given_E = 0.7    # 70% de tos si tiene la enfermedad
P_T_given_not_E = 0.2 # 20% de tos si no tiene la enfermedad

# -------------------------------------
# Simulamos si una persona tiene la enfermedad
# -------------------------------------

enfermo = random.random() < P_E

# Simulamos si tiene fiebre
if enfermo:
    fiebre = random.random() < P_F_given_E
    tos = random.random() < P_T_given_E
else:
    fiebre = random.random() < P_F_given_not_E
    tos = random.random() < P_T_given_not_E

# -------------------------------------
# Mostrar síntomas observados
# -------------------------------------

print("\n👩‍⚕️ Observación de un paciente:")
print(f"- ¿Fiebre? {'Sí' if fiebre else 'No'}")
print(f"- ¿Tos? {'Sí' if tos else 'No'}")

# -------------------------------------
# Ahora usamos la Regla de la Cadena inversa (Bayes implícito)
# Queremos: P(E | Fiebre y Tos)
# -------------------------------------

# Primero calculamos P(Fiebre y Tos | Enfermo)
p_sintomas_given_enfermo = (P_F_given_E if fiebre else (1 - P_F_given_E)) * (P_T_given_E if tos else (1 - P_T_given_E))

# Luego P(Fiebre y Tos | NO Enfermo)
p_sintomas_given_not_enfermo = (P_F_given_not_E if fiebre else (1 - P_F_given_not_E)) * (P_T_given_not_E if tos else (1 - P_T_given_not_E))

# Usamos la Regla de Bayes para calcular P(Enfermo | Síntomas)
# Fórmula:
# P(E|F,T) = [P(F,T|E) * P(E)] / [P(F,T|E)*P(E) + P(F,T|¬E)*P(¬E)]

numerador = p_sintomas_given_enfermo * P_E
denominador = (p_sintomas_given_enfermo * P_E) + (p_sintomas_given_not_enfermo * (1 - P_E))

if denominador == 0:
    probabilidad_enfermo_dado_sintomas = 0
else:
    probabilidad_enfermo_dado_sintomas = numerador / denominador

# -------------------------------------
# Mostrar diagnóstico basado en síntomas
# -------------------------------------

print(f"\n🧪 Probabilidad de que el paciente esté enfermo dado los síntomas observados: {probabilidad_enfermo_dado_sintomas:.2%}")

# También mostramos si realmente estaba enfermo (por simulación aleatoria)
print(f"✅ Realmente enfermo: {'Sí' if enfermo else 'No'}")

# -------------------------------------
# Nota:
# Este código simula la observación de síntomas y luego, usando probabilidades,
# calcula la probabilidad "inteligente" del diagnóstico.
# -------------------------------------
