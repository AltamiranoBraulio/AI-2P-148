# 🧠 Resolver Sudoku con Backtracking

# Función para imprimir el tablero de Sudoku de forma visualmente ordenada
def imprimir_sudoku(tablero):
    for i in range(9):  # Recorre cada fila
        if i % 3 == 0 and i != 0:  # Después de cada 3 filas (excepto la primera), imprime una línea divisoria
            print("-"*21)
        for j in range(9):  # Recorre cada columna de la fila actual
            if j % 3 == 0 and j != 0:  # Después de cada 3 columnas, imprime una barra vertical divisoria
                print("|", end=" ")
            # Imprime el número si no es cero; si es cero, imprime un punto (casilla vacía)
            print(tablero[i][j] if tablero[i][j] != 0 else ".", end=" ")
        print()  # Salto de línea al final de cada fila
    print()  # Salto de línea extra después del tablero

# Función que encuentra la primera casilla vacía (con valor 0)
def encontrar_vacio(tablero):
    for i in range(9):  # Recorre filas
        for j in range(9):  # Recorre columnas
            if tablero[i][j] == 0:  # Si encuentra un 0, devuelve su posición (fila, columna)
                return (i, j)
    return None  # Si no hay casillas vacías, devuelve None

# Función que verifica si es válido colocar un número en una casilla específica
def es_valido(tablero, num, fila, col):
    # Verifica si el número ya está en la fila
    if num in tablero[fila]:
        return False
    # Verifica si el número ya está en la columna (se crea una lista con los valores de esa columna)
    if num in [tablero[i][col] for i in range(9)]:
        return False
    # Calcula el índice inicial del subcuadro 3x3 al que pertenece la casilla
    fila_inicio = (fila // 3) * 3
    col_inicio = (col // 3) * 3
    # Recorre el subcuadro 3x3 para verificar si el número ya está presente
    for i in range(fila_inicio, fila_inicio + 3):
        for j in range(col_inicio, col_inicio + 3):
            if tablero[i][j] == num:
                return False
    return True  # Si pasa todas las verificaciones, el número es válido

# Función principal que intenta resolver el Sudoku usando búsqueda de vuelta atrás
def resolver_sudoku(tablero):
    vacio = encontrar_vacio(tablero)  # Busca la siguiente casilla vacía
    if not vacio:  # Si no hay casillas vacías, el Sudoku está resuelto
        return True

    fila, col = vacio  # Obtiene la posición de la casilla vacía

    for num in range(1, 10):  # Intenta colocar los números del 1 al 9 en esa casilla
        if es_valido(tablero, num, fila, col):  # Verifica si el número es válido
            tablero[fila][col] = num  # Coloca el número provisionalmente
            if resolver_sudoku(tablero):  # Llama recursivamente para resolver el resto del tablero
                return True  # Si la llamada recursiva retorna True, el Sudoku se resolvió correctamente
            tablero[fila][col] = 0  # Si no funcionó, borra el número (retroceso: backtracking)
    return False  # Si ningún número del 1 al 9 funcionó, devuelve False para retroceder

# 🎯 Tablero de Sudoku con casillas vacías (representadas por ceros)
sudoku = [
    [5, 1, 7, 6, 0, 0, 0, 3, 4],  # Fila 0
    [2, 8, 9, 0, 0, 4, 0, 0, 0],  # Fila 1
    [3, 4, 6, 2, 0, 5, 0, 9, 0],  # Fila 2
    [6, 0, 2, 0, 0, 0, 0, 1, 0],  # Fila 3
    [0, 3, 8, 0, 0, 6, 0, 4, 7],  # Fila 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Fila 5
    [0, 9, 0, 0, 0, 0, 0, 7, 8],  # Fila 6
    [7, 0, 3, 4, 0, 0, 5, 6, 0],  # Fila 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Fila 8
]

# Muestra el Sudoku original antes de resolverlo
print("🧩 Sudoku Inicial:")
imprimir_sudoku(sudoku)

# Intenta resolver el Sudoku y muestra el resultado
if resolver_sudoku(sudoku):  # Si la función devuelve True, se resolvió correctamente
    print("🎉 ¡Sudoku Resuelto!")  # Mensaje de éxito
    imprimir_sudoku(sudoku)  # Muestra el Sudoku ya resuelto
else:
    print("🚫 No se pudo resolver el Sudoku.")  # Si no hay solución, muestra mensaje de error
