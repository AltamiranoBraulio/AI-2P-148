# --- Datos iniciales ---
# Probabilidades a priori de Spam y No Spam
prob_spam = 0.30  # 30% de los correos son Spam
prob_no_spam = 1 - prob_spam  # 70% de los correos son No Spam

# Probabilidades de las palabras clave si el correo es Spam
prob_gratis_dado_spam = 0.80
prob_oferta_dado_spam = 0.70
prob_dinero_dado_spam = 0.60

# Probabilidades de las palabras clave si el correo es No Spam
prob_gratis_dado_no_spam = 0.10
prob_oferta_dado_no_spam = 0.15
prob_dinero_dado_no_spam = 0.05

# --- Probabilidad total de las palabras (Ley de la probabilidad total) ---
# Calculamos la probabilidad total de que las palabras aparezcan en un correo (Spam o No Spam)
prob_gratis = (prob_gratis_dado_spam * prob_spam) + (prob_gratis_dado_no_spam * prob_no_spam)
prob_oferta = (prob_oferta_dado_spam * prob_spam) + (prob_oferta_dado_no_spam * prob_no_spam)
prob_dinero = (prob_dinero_dado_spam * prob_spam) + (prob_dinero_dado_no_spam * prob_no_spam)

# --- Aplicamos la Regla de Bayes ---
# P(Spam | Palabras) = (P(Palabras | Spam) * P(Spam)) / P(Palabras)
# P(No Spam | Palabras) = (P(Palabras | No Spam) * P(No Spam)) / P(Palabras)

# Numerador de la Regla de Bayes para Spam
numerador_spam = prob_gratis_dado_spam * prob_oferta_dado_spam * prob_dinero_dado_spam * prob_spam

# Numerador de la Regla de Bayes para No Spam
numerador_no_spam = prob_gratis_dado_no_spam * prob_oferta_dado_no_spam * prob_dinero_dado_no_spam * prob_no_spam

# Denominador (total de las probabilidades de las palabras) - se calcula sumando los numeradores
denominador = (numerador_spam + numerador_no_spam)

# --- Calculamos las probabilidades finales ---
# P(Spam | Palabras)
prob_spam_dado_palabras = numerador_spam / denominador

# P(No Spam | Palabras)
prob_no_spam_dado_palabras = numerador_no_spam / denominador

# --- Resultado final ---
print(f"Probabilidad de que el correo sea Spam dado las palabras 'gratis', 'oferta' y 'dinero': {prob_spam_dado_palabras * 100:.2f}%")
print(f"Probabilidad de que el correo sea No Spam dado las palabras 'gratis', 'oferta' y 'dinero': {prob_no_spam_dado_palabras * 100:.2f}%")
