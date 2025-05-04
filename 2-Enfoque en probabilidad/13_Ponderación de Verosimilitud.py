import random

# --- Definimos nuestras variables y sus probabilidades condicionales --- #

# Probabilidad de ver cada tipo de animal en un safari
probabilidades = {
    'León': 0.2,      # 20% de chance de ver un león
    'Cebra': 0.5,     # 50% de chance de ver una cebra
    'Elefante': 0.3   # 30% de chance de ver un elefante
}

# Características observables de cada animal (simplificado)
# Ejemplo: "Grande" y "Rayado" son características que podrían verse
caracteristicas = {
    'León': {'Grande': 1.0, 'Rayado': 0.0},
    'Cebra': {'Grande': 0.5, 'Rayado': 1.0},
    'Elefante': {'Grande': 1.0, 'Rayado': 0.0}
}

# --- Función para simular un animal avistado --- #
def simular_avistamiento(probabilidades):
    """
    Simula un avistamiento de un animal basándose en las probabilidades generales.
    """
    animales = list(probabilidades.keys())
    pesos = list(probabilidades.values())
    return random.choices(animales, weights=pesos, k=1)[0]

# --- Función para calcular el peso de verosimilitud --- #
def calcular_peso(animal, evidencia):
    """
    Calcula el peso basado en qué tan compatible es el animal con la evidencia observada.
    """
    peso = 1.0  # Partimos con peso 1
    for caracteristica, valor_observado in evidencia.items():
        if caracteristica in caracteristicas[animal]:
            # Multiplicamos el peso por la probabilidad de observar esa característica
            probabilidad_caracteristica = caracteristicas[animal][caracteristica]
            peso *= probabilidad_caracteristica if valor_observado else (1 - probabilidad_caracteristica)
    return peso

# --- Función principal que realiza el muestreo con ponderación de verosimilitud --- #
def muestreo_ponderado(probabilidades, evidencia, n_muestras):
    """
    Realiza múltiples simulaciones de avistamientos, ponderando según la evidencia observada.
    """
    resultados = []
    pesos = []

    for _ in range(n_muestras):
        animal = simular_avistamiento(probabilidades)  # Simulamos un animal
        peso = calcular_peso(animal, evidencia)        # Calculamos su peso de verosimilitud
        resultados.append(animal)
        pesos.append(peso)

    return resultados, pesos

# --- Parámetros de simulación --- #

# Evidencia observada: vimos un animal grande y rayado
evidencia = {
    'Grande': True,
    'Rayado': True
}

# Número de muestras que queremos generar
n_muestras = 30

# --- Ejecutamos el muestreo --- #
resultados, pesos = muestreo_ponderado(probabilidades, evidencia, n_muestras)

# --- Mostramos los resultados --- #
print("🔵 Resultados del Safari (Animal - Peso de Verosimilitud):\n")
for animal, peso in zip(resultados, pesos):
    print(f"Animal: {animal}, Peso: {peso:.3f}")

# --- Análisis resumido --- #
# Agrupamos los pesos por tipo de animal
resumen = {}
for animal, peso in zip(resultados, pesos):
    if animal not in resumen:
        resumen[animal] = 0
    resumen[animal] += peso

print("\n🟢 Resumen ponderado final:\n")
for animal, peso_total in resumen.items():
    print(f"{animal}: {peso_total:.3f}")
