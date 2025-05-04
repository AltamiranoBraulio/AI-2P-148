# Función que verifica si es seguro colocar una reina en la posición (fila, col)
def es_seguro(tablero, fila, col, N):
    # Verificar la columna: recorremos todas las filas previas y revisamos si hay una reina en la misma columna.
    for i in range(fila):
        if tablero[i][col] == 1:  # Si encontramos una reina en la columna, no es seguro.
            return False

    # Verificar la diagonal superior izquierda: recorremos hacia arriba y a la izquierda desde la posición actual
    for i, j in zip(range(fila-1, -1, -1), range(col-1, -1, -1)):
        if tablero[i][j] == 1:  # Si encontramos una reina en esta diagonal, no es seguro.
            return False

    # Verificar la diagonal superior derecha: recorremos hacia arriba y a la derecha desde la posición actual
    for i, j in zip(range(fila-1, -1, -1), range(col+1, N)):
        if tablero[i][j] == 1:  # Si encontramos una reina en esta diagonal, no es seguro.
            return False

    return True  # Si ninguna de las condiciones anteriores encontró un conflicto, es seguro colocar la reina.

# Función recursiva que resuelve el problema de las N-Reinas
def resolver_n_reinas(tablero, fila, N):
    # Si hemos colocado reinas en todas las filas, hemos encontrado una solución
    if fila >= N:
        return True

    # Intentamos colocar una reina en cada columna de la fila actual
    for col in range(N):
        if es_seguro(tablero, fila, col, N):  # Verificamos si es seguro colocar la reina en (fila, col)
            tablero[fila][col] = 1  # Colocamos la reina en la posición actual del tablero

            # Recursivamente intentamos colocar la siguiente reina en la siguiente fila
            if resolver_n_reinas(tablero, fila + 1, N):
                return True  # Si la llamada recursiva tiene éxito, retornamos True (se encontró solución)

            # Si no pudimos colocar la reina en la siguiente fila, deshacemos la colocación (backtrack)
            tablero[fila][col] = 0

    # Si no se puede colocar una reina en ninguna columna de esta fila, devolvemos False
    return False

# Función para imprimir el tablero de solución
def imprimir_tablero(tablero, N):
    for i in range(N):
        for j in range(N):
            # Imprimimos "Q" si hay una reina en la posición (i, j), y "." si no hay reina.
            print("Q" if tablero[i][j] == 1 else ".", end=" ")
        print()  # Salto de línea después de imprimir cada fila

# Tamaño del tablero (N Reinas) - En este caso, se usa 8 reinas como ejemplo
N = 8  # Número de reinas y el tamaño del tablero
# Creamos un tablero vacío de NxN (todo inicializado en 0, es decir, sin reinas)
tablero = [[0 for _ in range(N)] for _ in range(N)]

# Intentamos resolver el problema de las N-Reinas
if resolver_n_reinas(tablero, 0, N):  # Comenzamos desde la primera fila (índice 0)
    print("Solución encontrada:")  # Si se encontró una solución, la mostramos
    imprimir_tablero(tablero, N)  # Imprimimos el tablero con la solución
else:
    print("No se pudo encontrar una solución.")  # Si no se encontró solución, mostramos un mensaje de error
