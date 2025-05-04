# Laberinto representado como una matriz 2D
# 1 = camino válido
# 0 = pared (bloqueado)
laberinto = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]

# Matriz para guardar el camino solucionado
# Al inicio está toda en ceros
solucion = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Función para verificar si podemos movernos a la celda (x, y)
def es_valido(laberinto, x, y):
    # Verifica que no se salga de los límites y que la celda sea 1 (camino)
    return 0 <= x < 4 and 0 <= y < 4 and laberinto[x][y] == 1

# Función principal que resuelve el laberinto usando Backtracking
def resolver_laberinto(laberinto, x, y, solucion):
    # 🟢 Caso base: Si llegamos a la última celda (meta en (3,3))
    if x == 3 and y == 3:
        solucion[x][y] = 1  # Marca la salida como parte del camino
        return True  # Éxito: camino encontrado

    # Verifica si la celda (x, y) es válida para moverse
    if es_valido(laberinto, x, y):
        # Marca la celda actual como parte del camino en la solución
        solucion[x][y] = 1

        # 🔽 Intenta mover hacia abajo (x + 1)
        if resolver_laberinto(laberinto, x + 1, y, solucion):
            return True  # Si encuentra solución en esa dirección, retorna éxito

        # ➡️ Intenta mover hacia la derecha (y + 1)
        if resolver_laberinto(laberinto, x, y + 1, solucion):
            return True  # Éxito si encuentra camino hacia la derecha

        # 🔙 Si no hay camino ni abajo ni derecha, hace backtracking:
        # Desmarca esta celda (la pone en 0 porque no es parte del camino correcto)
        solucion[x][y] = 0
        return False  # Retorna falso porque este camino no lleva a la meta

    # 🔴 Si la celda (x, y) no es válida, no puede moverse ahí
    return False

# 🏁 Código que ejecuta todo:
# Comienza desde la celda (0,0) y trata de resolver el laberinto
if resolver_laberinto(laberinto, 0, 0, solucion):
    # Si se encuentra una solución, imprime la matriz solución
    for fila in solucion:
        print(fila)
else:
    # Si no hay solución posible, muestra mensaje
    print("No hay solución")
