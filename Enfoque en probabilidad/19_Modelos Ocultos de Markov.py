import random  # Importamos random, aunque en este código no se usa (pero podrías usarlo para generar observaciones aleatorias)

# ---------------------------------------------
# 🔒 Estados ocultos (Lo que no podemos ver directamente)
# Ejemplo: qué está haciendo la persona realmente.
# ---------------------------------------------
estados = ['Trabajando', 'De vacaciones', 'Enfermo']

# ---------------------------------------------
# 👀 Observaciones posibles (Lo que sí vemos)
# Ejemplo: cómo se comporta externamente (llamadas, correos, silencio).
# ---------------------------------------------
observaciones_posibles = ['Llamadas', 'Correo', 'Silencio']

# ---------------------------------------------
# 🔄 Matriz de transición entre estados ocultos
# Dice la probabilidad de pasar de un estado oculto a otro.
# Por ejemplo: si está "Trabajando" hoy, ¿qué probabilidad hay de que mañana esté "De vacaciones"?
# Cada fila suma aproximadamente 1 (porque cubre todas las opciones posibles desde un estado).
# ---------------------------------------------
transiciones = {
    'Trabajando': {'Trabajando': 0.6, 'De vacaciones': 0.3, 'Enfermo': 0.1},
    'De vacaciones': {'Trabajando': 0.2, 'De vacaciones': 0.7, 'Enfermo': 0.1},
    'Enfermo': {'Trabajando': 0.3, 'De vacaciones': 0.2, 'Enfermo': 0.5},
}

# ---------------------------------------------
# 📡 Matriz de emisión (también llamada sensor model)
# Relaciona cada estado oculto con las probabilidades de cada observación visible.
# Ejemplo: Si está "Enfermo", probablemente haya "Silencio" (80%)
# ---------------------------------------------
emisiones = {
    'Trabajando': {'Llamadas': 0.7, 'Correo': 0.2, 'Silencio': 0.1},
    'De vacaciones': {'Llamadas': 0.3, 'Correo': 0.1, 'Silencio': 0.6},
    'Enfermo': {'Llamadas': 0.1, 'Correo': 0.1, 'Silencio': 0.8},
}

# ---------------------------------------------
# 🎲 Distribución inicial (creencia inicial)
# Nos dice en qué estado creemos que está la persona al principio.
# Ejemplo: 50% de probabilidad de que esté "Trabajando" al inicio.
# ---------------------------------------------
inicial = {'Trabajando': 0.5, 'De vacaciones': 0.3, 'Enfermo': 0.2}

# ---------------------------------------------
# 🔄 Función para normalizar cualquier distribución
# Se asegura de que los valores sumen 1 (probabilidades válidas).
# No es usada en Viterbi, pero es útil en otros algoritmos.
# ---------------------------------------------
def normalizar(distribucion):
    total = sum(distribucion.values())
    return {k: v / total for k, v in distribucion.items()}

# ---------------------------------------------
# 🚀 Algoritmo Viterbi para decodificación
# Dado una secuencia de observaciones, encuentra la secuencia más probable de estados ocultos.
# Esto es como que un detective trate de adivinar qué pasó en realidad basándose en pistas.
# ---------------------------------------------
def viterbi(observaciones):
    V = [{}]  # Aquí guardamos la probabilidad máxima de cada estado en cada tiempo.
    path = {}  # Aquí guardamos el camino (la secuencia de estados) más probable.

    # ⏰ Paso de inicialización con la primera observación
    for estado in estados:
        # La probabilidad inicial es: probabilidad de estar en ese estado al inicio × probabilidad de emitir la observación
        V[0][estado] = inicial[estado] * emisiones[estado][observaciones[0]]
        # Guardamos que al inicio, el camino es solo este estado
        path[estado] = [estado]

    # 🔄 Ahora recorremos el resto de observaciones (t = 1 hasta el final)
    for t in range(1, len(observaciones)):
        V.append({})  # Agregamos un nuevo paso de tiempo
        nuevo_path = {}  # Para guardar los caminos actualizados

        for estado_actual in estados:
            # Para cada estado actual, buscamos el estado anterior que maximiza la probabilidad
            (prob_max, estado_previo) = max(
                # Multiplicamos:
                # 1) la mejor probabilidad hasta el estado anterior
                # 2) la probabilidad de transición al estado actual
                # 3) la probabilidad de emitir la observación actual desde este estado
                (V[t-1][estado_anterior] * transiciones[estado_anterior][estado_actual] * emisiones[estado_actual][observaciones[t]], estado_anterior)
                for estado_anterior in estados
            )
            # Guardamos la mejor probabilidad para este estado en tiempo t
            V[t][estado_actual] = prob_max
            # Guardamos el mejor camino que llega aquí
            nuevo_path[estado_actual] = path[estado_previo] + [estado_actual]

        # Actualizamos todos los caminos
        path = nuevo_path

    # ✅ Al final, seleccionamos el estado final que tenga la probabilidad más alta
    (prob_final, estado_final) = max((V[-1][estado], estado) for estado in estados)
    # Devolvemos el camino (secuencia de estados) y su probabilidad
    return path[estado_final], prob_final

# ---------------------------------------------
# 🎲 Secuencia de observaciones (simuladas)
# Lo que el detective recibe como pistas externas
# ---------------------------------------------
observaciones = ['Llamadas', 'Silencio', 'Silencio', 'Correo', 'Llamadas', 'Silencio']

# ---------------------------------------------
# 🚀 Ejecutamos el algoritmo Viterbi con nuestras observaciones
# ---------------------------------------------
print("🔎 Observaciones del detective:")
print(observaciones)  # Mostramos lo que recibimos como pistas

# Corremos Viterbi para encontrar la secuencia oculta más probable
camino_mas_probable, probabilidad = viterbi(observaciones)

# Mostramos la secuencia de estados ocultos (la explicación interna más probable)
print("\n🕵️‍♂️ Secuencia más probable de actividades ocultas:")
print(camino_mas_probable)

# Mostramos la probabilidad total de este camino (qué tan seguro está el algoritmo)
print(f"\n🎯 Probabilidad total del camino: {probabilidad:.5f}")
