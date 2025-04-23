import random  # Importamos la librería random para generar movimientos aleatorios

# Mapa oculto, solo se revelan casillas adyacentes al agente
# 'S' es el punto de inicio, 'G' es el objetivo y '#' son los obstáculos.
MAPA_REAL = [
    ['S', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', 'G'],  # Mapa en la primera fila
    [' ', '#', '#', ' ', '#', '#', ' ', '#', '#', ' '],  # Segunda fila, contiene más obstáculos
    [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],  # Tercera fila
    [' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#'],  # Cuarta fila con más obstáculos
    [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '],  # Quinta fila
]

# Definimos el tamaño del mapa
FILAS = len(MAPA_REAL)  # Número de filas en el mapa
COLUMNAS = len(MAPA_REAL[0])  # Número de columnas en el mapa

# Definimos las direcciones posibles para moverse: arriba, abajo, izquierda, derecha
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Función para encontrar la posición de un objetivo ('S' o 'G') en el mapa
def encontrar_posicion(mapa, objetivo):
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if mapa[i][j] == objetivo:  # Si encontramos el objetivo, devolvemos la posición
                return (i, j)

# Función que devuelve los vecinos de una posición dada (casillas adyacentes)
def vecinos(pos):
    x, y = pos
    return [(x + dx, y + dy) for dx, dy in DIRECCIONES if 0 <= x + dx < FILAS and 0 <= y + dy < COLUMNAS]

# Función para calcular la distancia de Manhattan entre dos puntos (suma de las diferencias absolutas)
def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Definimos la clase AgenteLRTA que implementa el algoritmo LRTA*
class AgenteLRTA:
    def __init__(self, mapa_real):
        self.real = mapa_real  # El mapa real donde el agente se mueve
        self.inicio = encontrar_posicion(mapa_real, 'S')  # Encuentra la posición de inicio 'S'
        self.meta = encontrar_posicion(mapa_real, 'G')  # Encuentra la posición del objetivo 'G'
        # Inicializa el mapa conocido del agente con todas las casillas marcadas como desconocidas ('?')
        self.mapa_conocido = [['?' for _ in range(COLUMNAS)] for _ in range(FILAS)]
        # Calcula la heurística de Manhattan para cada casilla
        self.h = { (i, j): distancia_manhattan((i, j), self.meta) for i in range(FILAS) for j in range(COLUMNAS) }
        self.mapa_conocido[self.inicio[0]][self.inicio[1]] = 'S'  # Marca la casilla de inicio en el mapa conocido
        self.pos = self.inicio  # El agente comienza en la posición de inicio

    # Función que actualiza la vista del agente, revelando las casillas adyacentes
    def actualizar_vista(self):
        x, y = self.pos  # Posición actual del agente
        self.mapa_conocido[x][y] = self.real[x][y]  # Marca la casilla actual como conocida
        # Revela las casillas adyacentes (vecinas) a la casilla actual
        for dx, dy in DIRECCIONES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
                self.mapa_conocido[nx][ny] = self.real[nx][ny]

    # Función principal que ejecuta el agente LRTA*
    def ejecutar(self):
        camino = [self.pos]  # Lista para guardar el camino recorrido por el agente
        pasos = 0  # Contador de pasos

        # Bucle principal: el agente se mueve hasta llegar al objetivo o hasta alcanzar 500 pasos
        while self.pos != self.meta and pasos < 500:
            pasos += 1  # Incrementa el contador de pasos
            self.actualizar_vista()  # El agente actualiza su vista del entorno

            posibles = []  # Lista para almacenar las posiciones vecinas viables

            # Recorre todos los vecinos de la posición actual
            for v in vecinos(self.pos):
                vx, vy = v
                if self.mapa_conocido[vx][vy] != '#':  # Si el vecino no es un obstáculo
                    costo = 1 + self.h[v]  # Calcula el costo total (1 para moverse + la heurística)
                    posibles.append((costo, v))  # Añade el vecino a la lista de opciones

            if not posibles:  # Si no hay caminos viables, el agente está atorado
                print("🚧 Sin caminos viables. Atorado.")
                break

            # Ordena los vecinos por el costo (costo más bajo primero)
            posibles.sort()
            mejor_costo, siguiente = posibles[0]  # Selecciona el vecino con el costo mínimo

            # Aprendizaje: si es necesario, actualiza la heurística de la posición actual
            actual_h = self.h[self.pos]  # Obtiene la heurística actual de la posición
            self.h[self.pos] = max(actual_h, mejor_costo)  # Actualiza la heurística con el valor máximo

            # El agente se mueve a la nueva posición seleccionada
            self.pos = siguiente
            camino.append(self.pos)  # Añade la nueva posición al camino recorrido

        # Al final del ciclo, si el agente llega a la meta, muestra el resultado
        if self.pos == self.meta:
            print(f"✅ Meta alcanzada en {len(camino) - 1} pasos.")
        else:
            print("❌ No se alcanzó la meta.")  # Si el agente no llegó a la meta

        return camino  # Devuelve el camino recorrido

# Función para imprimir el mapa descubierto por el agente
def imprimir_mapa(mapa, camino):
    mapa_temp = [fila.copy() for fila in mapa]  # Copia del mapa para no modificar el original
    # Marca las posiciones recorridas en el camino como puntos ('.')
    for (x, y) in camino:
        if mapa_temp[x][y] == ' ' or mapa_temp[x][y] == '?':  # Si la casilla es libre o desconocida
            mapa_temp[x][y] = '.'  # Marca como recorrido
    # Imprime el mapa descubierto
    for fila in mapa_temp:
        print(''.join(fila))

# 🧪 Ejecutamos el agente LRTA*
agente = AgenteLRTA(MAPA_REAL)  # Crea un nuevo agente con el mapa real
camino = agente.ejecutar()  # Ejecuta el agente para encontrar la meta

# Imprime el mapa descubierto con el camino seguido
print("\n🗺️ Mapa descubierto:")
imprimir_mapa(agente.mapa_conocido, camino)
