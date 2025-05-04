# Esta función verifica si es válido colocar un número en una casilla específica del Sudoku
def es_valido(tablero, fila, col, num):
    # 🔎 Verifica si 'num' ya está en la misma fila
    for i in range(9):
        if tablero[fila][i] == num:
            return False  # ❌ Si ya está, no es válido ponerlo de nuevo en esa fila

    # 🔎 Verifica si 'num' ya está en la misma columna
    for i in range(9):
        if tablero[i][col] == num:
            return False  # ❌ Si ya está, tampoco es válido en esa columna

    # 🔎 Verifica si 'num' ya está en el subcuadro 3x3
    # Calcula la fila inicial del subcuadro (será 0, 3 o 6)
    start_row = (fila // 3) * 3
    # Calcula la columna inicial del subcuadro (será 0, 3 o 6)
    start_col = (col // 3) * 3

    # Recorre las 9 casillas del subcuadro 3x3
    for i in range(3):
        for j in range(3):
            if tablero[start_row + i][start_col + j] == num:
                return False  # ❌ Si ya está en el subcuadro, tampoco es válido

    return True  # ✅ Si pasó todas las pruebas, es válido colocar 'num' aquí


# Esta función intenta resolver el Sudoku usando Backtracking
def resolver_sudoku(tablero):
    # 🔄 Recorre todas las filas
    for fila in range(9):
        # 🔄 Recorre todas las columnas
        for col in range(9):
            # 🟦 Si encuentra una casilla vacía (representada por 0)
            if tablero[fila][col] == 0:
                # 🔢 Intenta poner los números del 1 al 9
                for num in range(1, 10):
                    # ✅ Si es válido poner 'num' en esa casilla
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num  # ✅ Coloca el número (hace la elección)

                        # 🔁 Llama recursivamente para seguir resolviendo el resto
                        if resolver_sudoku(tablero):
                            return True  # 🎯 Si se resolvió, termina y devuelve True

                        tablero[fila][col] = 0  # 🔙 Si no funcionó, deshace (backtracking)

                return False  # ❌ Si ningún número funcionó aquí, devuelve False (para retroceder)
    
    return True  # 🎉 Si no quedan casillas vacías, ¡el Sudoku está resuelto!
