# --- DATOS INICIALES ---

# Definimos las probabilidades base:
# P(F) = Probabilidad de que un paciente sea fumador
p_fumador = 0.30  

# P(F ∩ E) = Probabilidad de que un paciente sea fumador Y tenga enfermedad pulmonar
p_fumador_y_enfermo = 0.10  

# Calculamos la probabilidad condicionada usando la fórmula:
# P(E | F) = P(F ∩ E) / P(F)
p_enfermo_dado_fumador = p_fumador_y_enfermo / p_fumador

# Mostramos el resultado
print(f"📋 Probabilidad de estar enfermo dado que es fumador: {p_enfermo_dado_fumador:.2f} ({p_enfermo_dado_fumador*100:.1f}%)")

# --- PARTE DE NORMALIZACIÓN ---

print("\n📚 Ahora vamos a normalizar un conjunto de probabilidades...")

# Supongamos que tenemos estos datos "no normalizados" de tipos de enfermedades:
# (Los valores no suman 1)
probabilidades_no_normalizadas = {
    "Enfermedad Pulmonar": 0.10,
    "Gripe": 0.20,
    "Covid": 0.50,
    "Asma": 0.15
}

# Calculamos la suma total de estos valores
suma_total = sum(probabilidades_no_normalizadas.values())

# Creamos un nuevo diccionario donde las probabilidades estén normalizadas
probabilidades_normalizadas = {}

# Recorremos el diccionario original
for enfermedad, prob in probabilidades_no_normalizadas.items():
    # Dividimos cada probabilidad entre la suma total para normalizar
    prob_normalizada = prob / suma_total
    # Guardamos el valor normalizado
    probabilidades_normalizadas[enfermedad] = prob_normalizada
    # Mostramos cada probabilidad normalizada
    print(f"   {enfermedad}: {prob_normalizada:.2f} ({prob_normalizada*100:.1f}%)")

# Verificación extra:
# Comprobamos que la suma de las probabilidades normalizadas sea 1 (o muy cercano)
suma_normalizada = sum(probabilidades_normalizadas.values())
print(f"\n✅ Suma total después de normalizar: {suma_normalizada:.2f}")
