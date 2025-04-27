import random  # Para generar selecciones aleatorias con ponderación

# --- DEFINIMOS LA DISTRIBUCIÓN DE PROBABILIDAD ---

# Aquí definimos las probabilidades de que salga "Cara" o "Cruz".
# Puedes ajustar estas probabilidades para simular una moneda cargada (con un sesgo).
distribucion_moneda = {
    "Cara": 0.7,   # 70% de probabilidad de que salga "Cara"
    "Cruz": 0.3    # 30% de probabilidad de que salga "Cruz"
}

# Verificamos que las probabilidades sumen 1 (condición importante)
if abs(sum(distribucion_moneda.values()) - 1.0) > 0.01:
    raise ValueError("🚨 Las probabilidades no suman 1. Revisa tu distribución.")

# --- FUNCIONES PARA SIMULAR LANZAMIENTOS ---

# Función que simula un único lanzamiento de la moneda
def lanzar_moneda(distribucion):
    # Extraemos las opciones y sus probabilidades (pesos)
    caras = list(distribucion.keys())  # ["Cara", "Cruz"]
    probabilidades = list(distribucion.values())  # [0.7, 0.3]
    # Usamos random.choices para seleccionar un resultado basado en la probabilidad
    resultado = random.choices(caras, weights=probabilidades, k=1)[0]  # k=1 significa una sola elección
    return resultado

# --- SIMULACIÓN DE VARIOS LANZAMIENTOS ---

# Definimos cuántos lanzamientos queremos hacer
lanzamientos = 1000  # Simulamos 1000 lanzamientos de la moneda

# Contador de resultados
conteo_resultados = {
    "Cara": 0,
    "Cruz": 0
}

print("\n🪙 Simulando lanzamientos de la moneda...")

# Simulamos los lanzamientos
for _ in range(lanzamientos):
    resultado = lanzar_moneda(distribucion_moneda)  # Lanzamos la moneda
    conteo_resultados[resultado] += 1  # Aumentamos el contador según el resultado

# --- MOSTRAR RESULTADOS ---

print(f"\n📊 Resultados después de {lanzamientos} lanzamientos:\n")

# Imprimimos los resultados de las simulaciones
for resultado, cantidad in conteo_resultados.items():
    porcentaje = (cantidad / lanzamientos) * 100  # Calculamos el porcentaje de cada resultado
    print(f"   {resultado}: {cantidad} veces ({porcentaje:.1f}%)")

# --- COMPARACIÓN CON LA DISTRIBUCIÓN DE PROBABILIDAD ---

# Mostramos las probabilidades originales para comparar
print("\n📈 Comparación con las probabilidades iniciales:")
for resultado, probabilidad in distribucion_moneda.items():
    print(f"   {resultado}: {probabilidad * 100:.1f}% de probabilidad esperada")

# --- ANÁLISIS DE RESULTADOS ---

# Nota: En simulaciones con pocos lanzamientos, los resultados no siempre coincidirán
# con las probabilidades, pero conforme aumenten los lanzamientos, los porcentajes
# deben acercarse más a las probabilidades iniciales.
