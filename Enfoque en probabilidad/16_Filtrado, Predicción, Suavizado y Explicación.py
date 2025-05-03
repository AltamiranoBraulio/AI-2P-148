import random

# ----------------------------
# Estados posibles del robot
# ----------------------------
estados = ['A', 'B', 'C']

# ----------------------------
# Matriz de transición (cómo se mueve)
# ----------------------------
transiciones = {
    'A': {'A': 0.7, 'B': 0.2, 'C': 0.1},
    'B': {'A': 0.3, 'B': 0.4, 'C': 0.3},
    'C': {'A': 0.2, 'B': 0.3, 'C': 0.5},
}

# ----------------------------
# Matriz de sensores (probabilidad de ver algo dado el estado)
# ----------------------------
sensor_model = {
    'A': {'rojo': 0.9, 'verde': 0.1},
    'B': {'rojo': 0.2, 'verde': 0.8},
    'C': {'rojo': 0.1, 'verde': 0.9},
}

# ----------------------------
# Observaciones simuladas (sensores)
# ----------------------------
observaciones = ['rojo', 'rojo', 'verde', 'verde', 'rojo']

# ----------------------------
# Creemos una función para normalizar
# ----------------------------
def normalizar(distribucion):
    total = sum(distribucion.values())
    return {k: v / total for k, v in distribucion.items()}

# ----------------------------
# Filtrado: Probabilidad del estado actual dado las observaciones hasta ahora
# ----------------------------
def filtrado(observaciones):
    # Inicializamos creencia uniforme
    bel = {s: 1/len(estados) for s in estados}

    historial = []

    for obs in observaciones:
        # Paso 1: Predicción
        pred = {}
        for s in estados:
            pred[s] = sum(bel[ant] * transiciones[ant][s] for ant in estados)

        # Paso 2: Actualización con sensor
        for s in estados:
            pred[s] *= sensor_model[s][obs]

        # Paso 3: Normalización
        bel = normalizar(pred)

        historial.append(bel.copy())  # Guardamos el resultado en el tiempo

    return historial

# ----------------------------
# Predicción: ¿Dónde estará el robot en k pasos?
# ----------------------------
def predecir(bel_actual, pasos):
    bel = bel_actual.copy()
    for _ in range(pasos):
        nuevo_bel = {}
        for s in estados:
            nuevo_bel[s] = sum(bel[ant] * transiciones[ant][s] for ant in estados)
        bel = normalizar(nuevo_bel)
    return bel

# ----------------------------
# Suavizado: Mejoramos las estimaciones pasadas
# ----------------------------
def suavizar(observaciones, filtrados):
    n = len(observaciones)
    # Inicializamos backward mensaje
    b = {s: 1.0 for s in estados}

    resultados = [None] * n

    for t in reversed(range(n)):
        suavizado = {}
        for s in estados:
            suavizado[s] = filtrados[t][s] * b[s]
        resultados[t] = normalizar(suavizado)

        # Actualizamos el mensaje backward
        nuevo_b = {}
        for s in estados:
            nuevo_b[s] = sum(transiciones[s][s2] * sensor_model[s2][observaciones[t]] * b[s2] for s2 in estados)
        b = normalizar(nuevo_b)

    return resultados

# ----------------------------
# Explicación (Viterbi): la secuencia más probable
# ----------------------------
def viterbi(observaciones):
    V = [{}]  # tabla Viterbi
    path = {}

    # Inicialización
    for s in estados:
        V[0][s] = sensor_model[s][observaciones[0]] * (1/len(estados))
        path[s] = [s]

    # Recursión
    for t in range(1, len(observaciones)):
        V.append({})
        nuevo_path = {}

        for s in estados:
            (prob, estado_prev) = max(
                (V[t-1][s2] * transiciones[s2][s] * sensor_model[s][observaciones[t]], s2) for s2 in estados
            )
            V[t][s] = prob
            nuevo_path[s] = path[estado_prev] + [s]

        path = nuevo_path

    # Terminación
    (prob, estado_final) = max((V[-1][s], s) for s in estados)
    return path[estado_final], prob

# ----------------------------
# Ejecutamos todo
# ----------------------------
filtrados = filtrado(observaciones)

print("🔎 Filtrado paso a paso:")
for i, f in enumerate(filtrados):
    print(f"Paso {i+1}: {f}")

# Predicción 2 pasos al futuro desde el último filtrado
pred = predecir(filtrados[-1], 2)
print("\n🚀 Predicción (2 pasos al futuro):")
print(pred)

# Suavizado usando todas las observaciones
suaves = suavizar(observaciones, filtrados)
print("\n🎯 Suavizado:")
for i, s in enumerate(suaves):
    print(f"Paso {i+1}: {s}")

# Mejor secuencia explicativa
seq, prob = viterbi(observaciones)
print("\n🏆 Explicación (secuencia más probable):")
print(f"Secuencia: {seq}")
print(f"Probabilidad: {prob}")
