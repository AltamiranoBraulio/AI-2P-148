import random

# -------------------------------
# Probabilidades base conocidas
# -------------------------------

# Probabilidad de que ocurra un robo (evento A)
P_robo = 0.01  # 1%

# Probabilidad de que la alarma suene dado que hubo un robo (evento B dado A)
P_alarma_given_robo = 0.95  # 95%

# Probabilidad de que la alarma suene sin que haya robo (falsa alarma)
P_alarma_given_no_robo = 0.02  # 2%

# Probabilidad de que el vecino llame si la alarma suena (evento C dado B)
P_vecino_llama_given_alarma = 0.90  # 90%

# Probabilidad de que el vecino llame si NO suena alarma
P_vecino_llama_given_no_alarma = 0.05  # 5%

# -------------------------------
# Regla de la Cadena aplicada
# -------------------------------

# Queremos: P(robo ∩ alarma ∩ vecino_llama)
# = P(robo) * P(alarma | robo) * P(vecino_llama | alarma)

P_conjunta = P_robo * P_alarma_given_robo * P_vecino_llama_given_alarma

print(f"Probabilidad conjunta de robo, alarma y vecino llama: {P_conjunta * 100:.4f}%")

# -------------------------------
# Ahora, vamos a SIMULAR 10 casos
# -------------------------------

print("\nSimulación de 10 días:")

for dia in range(1, 11):
    # Se determina si hay robo este día
    hay_robo = random.random() < P_robo

    # Se determina si la alarma suena
    if hay_robo:
        alarma_suena = random.random() < P_alarma_given_robo
    else:
        alarma_suena = random.random() < P_alarma_given_no_robo

    # Se determina si el vecino llama
    if alarma_suena:
        vecino_llama = random.random() < P_vecino_llama_given_alarma
    else:
        vecino_llama = random.random() < P_vecino_llama_given_no_alarma

    # Mostrar resultados
    print(f"Día {dia}: Robo={'Sí' if hay_robo else 'No'}, Alarma={'Sí' if alarma_suena else 'No'}, Vecino llama={'Sí' if vecino_llama else 'No'}")
