# Laberinto: 1 = camino, 0 = pared
laberinto = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]

# Crear una matriz para guardar la solución
solucion = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Verifica si (x, y) es posición válida
def es_valido(laberinto, x, y):
    return 0 <= x < 4 and 0 <= y < 4 and laberinto[x][y] == 1

# Algoritmo de Backtracking
def resolver_laberinto(laberinto, x, y, solucion):
    # 🎯 Caso base: llegó a la meta (última celda)
    if x == 3 and y == 3:
        solucion[x][y] = 1
        return True

    if es_valido(laberinto, x, y):
        # Marca la celda como parte de la solución
        solucion[x][y] = 1

        # 🔽 Mueve hacia abajo
        if resolver_laberinto(laberinto, x + 1, y, solucion):
            return True

        # ➡️ Mueve hacia la derecha
        if resolver_laberinto(laberinto, x, y + 1, solucion):
            return True

        # 🔙 Si no sirve ninguna dirección, hace backtrack
        solucion[x][y] = 0
        return False

    return False

# Ejecuta la función
if resolver_laberinto(laberinto, 0, 0, solucion):
    for fila in solucion:
        print(fila)
else:
    print("No hay solución")
