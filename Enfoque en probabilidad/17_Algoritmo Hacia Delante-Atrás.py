import random  # Importamos random por si queremos hacer simulaciones adicionales (aunque en este código no se usa directamente).

# ----------------------------
# ESTADOS POSIBLES DEL MODELO
# ----------------------------
# Nuestro sistema es un modelo oculto de Markov (HMM).
# Hay dos posibles estados ocultos:
# 1. 'Sano'   -> El paciente está sano.
# 2. 'Enfermo'-> El paciente está enfermo.
estados = ['Sano', 'Enfermo']

# ----------------------------
# MATRIZ DE TRANSICIÓN ENTRE ESTADOS
# ----------------------------
# Indica las probabilidades de cambiar de un estado al otro en cada paso de tiempo.
# Por ejemplo, si hoy estoy sano, tengo 80% de seguir sano y 20% de enfermarme mañana.
transiciones = {
    'Sano': {'Sano': 0.8, 'Enfermo': 0.2},
    'Enfermo': {'Sano': 0.3, 'Enfermo': 0.7},
}

# ----------------------------
# MODELO SENSORIAL (Probabilidad de observar síntomas dados los estados)
# ----------------------------
# Este modelo conecta los estados ocultos con las observaciones visibles (síntomas).
# Ejemplo: Si estoy enfermo, hay 80% de que tenga fiebre y 20% de que no.
sensor_model = {
    'Sano': {'Fiebre': 0.1, 'Normal': 0.9},
    'Enfermo': {'Fiebre': 0.8, 'Normal': 0.2},
}

# ----------------------------
# OBSERVACIONES DEL PACIENTE
# ----------------------------
# Esta es la secuencia de síntomas que se registró:
# Día 1: Fiebre
# Día 2: Normal
# Día 3: Fiebre
# Día 4: Fiebre
observaciones = ['Fiebre', 'Normal', 'Fiebre', 'Fiebre']

# ----------------------------
# FUNCIÓN DE NORMALIZACIÓN
# ----------------------------
# Dada una distribución de probabilidad (puede que no sume 1), la normaliza para que sí sume 1.
# Ejemplo: {'Sano': 0.2, 'Enfermo': 0.6} se convierte en {'Sano': 0.25, 'Enfermo': 0.75}
def normalizar(distribucion):
    total = sum(distribucion.values())  # Suma total de valores
    return {k: v / total for k, v in distribucion.items()}  # Divide cada valor por el total para normalizar

# ----------------------------
# PASO HACIA ADELANTE (FORWARD)
# ----------------------------
# Calcula la probabilidad del estado en cada momento usando solo las observaciones hasta ese tiempo.
def paso_forward(observaciones):
    # Inicializamos la creencia inicial de manera uniforme: 50% sano, 50% enfermo.
    bel = {s: 1/len(estados) for s in estados}

    forwards = []  # Lista para guardar las creencias en cada tiempo

    for obs in observaciones:
        # Predicción del siguiente estado según transiciones
        pred = {}
        for s in estados:
            # Sumamos sobre todos los posibles estados previos
            pred[s] = sum(bel[prev] * transiciones[prev][s] for prev in estados)
        
        # Incorporamos la evidencia (el síntoma observado en ese día)
        for s in estados:
            pred[s] *= sensor_model[s][obs]

        # Normalizamos la distribución resultante para que sea válida (sume 1)
        bel = normalizar(pred)

        # Guardamos esta creencia para este tiempo
        forwards.append(bel.copy())

    return forwards

# ----------------------------
# PASO HACIA ATRÁS (BACKWARD)
# ----------------------------
# Calcula la probabilidad de las observaciones futuras dado cada estado actual.
def paso_backward(observaciones):
    n = len(observaciones)
    # Inicializamos el mensaje backward como 1 para todos los estados (mensaje trivial)
    b = {s: 1.0 for s in estados}

    backwards = [None] * n  # Lista para guardar los mensajes backward

    for t in reversed(range(n)):  # Iteramos hacia atrás (del último día al primero)
        backwards[t] = b.copy()

        nuevo_b = {}
        for s in estados:
            # Suma sobre todos los estados siguientes posibles
            nuevo_b[s] = sum(
                transiciones[s][s2] * sensor_model[s2][observaciones[t]] * b[s2]
                for s2 in estados
            )
        # Normalizamos el nuevo mensaje backward
        b = normalizar(nuevo_b)

    return backwards

# ----------------------------
# ALGORITMO HACIA DELANTE-ATRÁS (SUAVIZADO)
# ----------------------------
# Combina la información del pasado (forward) y del futuro (backward) para estimar los estados ocultos.
def forward_backward(observaciones):
    # Ejecutamos paso forward y backward
    fwd = paso_forward(observaciones)
    bwd = paso_backward(observaciones)

    suaves = []  # Aquí guardaremos las distribuciones suavizadas (la mejor estimación)

    for t in range(len(observaciones)):
        suave = {}
        for s in estados:
            # Multiplicamos la probabilidad forward y backward para cada estado
            suave[s] = fwd[t][s] * bwd[t][s]
        # Normalizamos para obtener una distribución válida
        suaves.append(normalizar(suave))

    return suaves

# ----------------------------
# EJECUTAMOS EL CÓDIGO
# ----------------------------
print("🔎 Algoritmo Hacia Delante-Atrás")

# Calculamos paso hacia adelante
fwd = paso_forward(observaciones)
# Calculamos paso hacia atrás
bwd = paso_backward(observaciones)
# Calculamos suavizado (combinación de forward y backward)
suavizados = forward_backward(observaciones)

# Mostramos resultados paso a paso
print("\n➡️ Paso Adelante (Forward):")
for i, paso in enumerate(fwd):
    print(f"Tiempo {i+1}: {paso}")

print("\n⬅️ Paso Atrás (Backward):")
for i, paso in enumerate(bwd):
    print(f"Tiempo {i+1}: {paso}")

print("\n🎯 Suavizado (Combina ambos):")
for i, paso in enumerate(suavizados):
    print(f"Tiempo {i+1}: {paso}")
