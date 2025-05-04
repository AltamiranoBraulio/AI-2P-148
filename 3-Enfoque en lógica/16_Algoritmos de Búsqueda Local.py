import random  # Importamos la librería random para generar números aleatorios

# --------------------------------------------
# Función que evalúa cuántas reinas se atacan entre sí
# --------------------------------------------
def evaluar(tablero):
    ataques = 0  # Contador de ataques entre reinas

    # Comparamos cada pareja de reinas
    for i in range(len(tablero)):
        for j in range(i + 1, len(tablero)):
            # Si están en la misma diagonal, se atacan
            if abs(tablero[i] - tablero[j]) == abs(i - j):
                ataques += 1  # Suma 1 al contador de ataques
    return ataques  # Devuelve el total de ataques encontrados


# --------------------------------------------
# Función que genera un tablero vecino (una variante del actual)
# --------------------------------------------
def generar_vecino(tablero):
    vecino = tablero[:]  # Hacemos una copia del tablero actual para modificarlo

    # Seleccionamos una columna aleatoria donde moveremos la reina
    col = random.randint(0, len(tablero) - 1)

    # Escogemos una fila aleatoria para colocar la reina en esa columna
    fila = random.randint(0, len(tablero) - 1)

    # Realizamos el movimiento: cambiamos la fila en la columna seleccionada
    vecino[col] = fila

    return vecino  # Retornamos el tablero modificado (el vecino)


# --------------------------------------------
# Función principal que ejecuta Hill Climbing
# --------------------------------------------
def hill_climbing():
    # Creamos un estado inicial aleatorio:
    # cada columna recibe una fila aleatoria (posición de la reina)
    estado_actual = [random.randint(0, 7) for _ in range(8)]

    while True:  # Bucle infinito hasta que encontremos una solución válida
        # Contamos los ataques en el tablero actual
        conflictos_actual = evaluar(estado_actual)

        # Si no hay conflictos, es solución válida
        if conflictos_actual == 0:
            return estado_actual  # Retornamos la solución

        # Generamos un tablero vecino (modificamos la posición de una reina)
        vecino = generar_vecino(estado_actual)

        # Contamos los ataques en el vecino
        conflictos_vecino = evaluar(vecino)

        # Si el vecino es mejor (menos ataques), adoptamos ese cambio
        if conflictos_vecino < conflictos_actual:
            estado_actual = vecino  # Nos movemos al mejor vecino
        # Si no es mejor, seguimos en el estado actual (esto puede estancar el algoritmo)


# --------------------------------------------
# Ejecución del algoritmo
# --------------------------------------------

# Llamamos a la función para resolver el problema
solucion = hill_climbing()

# Mostramos la solución encontrada
print("Solución encontrada (posición de las reinas por columna):")
print(solucion)

# Extra: Mostramos el tablero de forma visual
print("\nTablero:")

# Recorremos cada fila del tablero
for fila in range(8):
    linea = ""
    for col in range(8):
        # Si la reina está en esta posición, imprimimos una "Q"
        if solucion[col] == fila:
            linea += "Q "
        else:
            linea += ". "  # Si no, imprimimos un punto
    print(linea)  # Imprimimos la fila completa
