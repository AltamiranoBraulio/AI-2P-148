# Importación de módulos necesarios
import time       # Para controlar pausas en la ejecución
import random     # Para aleatorizar el orden de exploración

# =============================================
# CONFIGURACIÓN INICIAL DEL ENTORNO DE SIMULACIÓN
# =============================================

# Definición del mapa del suelo como una matriz 5x5
# 'T' = Tierra (espacio disponible para crecimiento)
# 'N' = Nutriente (objetivo a encontrar)
# 'P' = Piedra (obstáculo infranqueable)
# 'R' = Raíz (posición actual de la raíz)
suelo = [
    ['T', 'T', 'T', 'T', 'T'],  # Fila 0
    ['T', 'P', 'T', 'N', 'T'],  # Fila 1
    ['T', 'T', 'P', 'T', 'T'],  # Fila 2
    ['T', 'N', 'T', 'P', 'T'],  # Fila 3
    ['T', 'T', 'T', 'T', 'N']   # Fila 4
]

# Posición inicial de la raíz en el centro del mapa (fila 2, columna 2)
posicion_inicial = (2, 2)  # Tupla con coordenadas (x, y)

# Marcamos la posición inicial como raíz en el mapa
suelo[posicion_inicial[0]][posicion_inicial[1]] = 'R'

# =============================================
# DEFINICIÓN DE FUNCIONES PRINCIPALES
# =============================================

def mostrar_suelo():
    """
    Función que muestra visualmente el estado actual del suelo.
    Imprime la matriz con formato legible y hace una pausa.
    """
    # Imprime un salto de línea para separar visualmente
    print("\nEstado del suelo:")
    
    # Itera sobre cada fila de la matriz suelo
    for fila in suelo:
        # Une los elementos de la fila con espacios y la imprime
        print(" ".join(fila))
    
    # Imprime otro salto de línea al final
    print()
    
    # Pausa la ejecución por 1 segundo para visualización
    time.sleep(1)

def dls_crecimiento_raiz(x, y, profundidad_actual, limite_profundidad, nutrientes_encontrados):
    """
    Función recursiva que implementa el algoritmo DLS para simular el crecimiento de raíces.
    
    Parámetros:
        x (int): Coordenada x (fila) actual
        y (int): Coordenada y (columna) actual
        profundidad_actual (int): Profundidad actual de recursión
        limite_profundidad (int): Límite máximo de profundidad
        nutrientes_encontrados (list): Lista para almacenar nutrientes encontrados
    
    La función modifica la matriz suelo directamente y actualiza nutrientes_encontrados.
    """
    
    # 1. Mostrar el estado actual del suelo
    mostrar_suelo()
    
    # 2. Condición de éxito: Encontrar un nutriente
    if suelo[x][y] == 'N':
        print(f"¡Nutriente encontrado en ({x}, {y})!")
        # Registrar la posición del nutriente encontrado
        nutrientes_encontrados.append((x, y))
        # Marcar la posición como raíz (la raíz absorbe el nutriente)
        suelo[x][y] = 'R'
        return  # Terminar esta rama de exploración
    
    # 3. Condición de límite: Profundidad máxima alcanzada
    if profundidad_actual >= limite_profundidad:
        print(f"Límite de profundidad alcanzado en ({x}, {y})")
        return  # Terminar esta rama por haber alcanzado el límite
    
    # 4. Preparar direcciones de exploración (arriba, abajo, izquierda, derecha)
    direcciones = [
        (-1, 0),  # Arriba (decrementar fila)
        (1, 0),   # Abajo (incrementar fila)
        (0, -1),  # Izquierda (decrementar columna)
        (0, 1)    # Derecha (incrementar columna)
    ]
    
    # Mezclar aleatoriamente las direcciones para crecimiento más natural
    random.shuffle(direcciones)
    
    # 5. Explorar cada dirección posible
    for dx, dy in direcciones:
        # Calcular nueva posición
        nx = x + dx  # Nueva coordenada x
        ny = y + dy  # Nueva coordenada y
        
        # Verificar si la nueva posición está dentro de los límites del mapa
        if 0 <= nx < len(suelo) and 0 <= ny < len(suelo[0]):
            # Verificar si la nueva posición es tierra o nutriente
            if suelo[nx][ny] in ['T', 'N']:
                # Marcar la nueva posición como raíz
                suelo[nx][ny] = 'R'
                
                # Llamada recursiva para continuar el crecimiento
                dls_crecimiento_raiz(
                    nx, ny, 
                    profundidad_actual + 1, 
                    limite_profundidad, 
                    nutrientes_encontrados
                )

# =============================================
# PROGRAMA PRINCIPAL - SIMULACIÓN
# =============================================

# Mostrar encabezado del simulador
print("🌱 SIMULADOR DE CRECIMIENTO DE RAÍCES 🌱")
print("Objetivo: Encontrar nutrientes (N) evitando piedras (P)")
print("Símbolos: R=Raíz, T=Tierra, N=Nutriente, P=Piedra\n")

# Mostrar el estado inicial del suelo
mostrar_suelo()

# Configurar parámetros de la simulación
try:
    # Solicitar al usuario el límite de profundidad
    limite_crecimiento = int(input("Ingresa el límite de profundidad para las raíces (1-5): "))
    # Validar el rango de entrada
    if not 1 <= limite_crecimiento <= 5:
        raise ValueError
except ValueError:
    print("Valor inválido. Usando valor por defecto: 3")
    limite_crecimiento = 3

# Lista para almacenar nutrientes encontrados
nutrientes = []

# Iniciar el proceso de crecimiento
print("\nIniciando crecimiento de raíces...")
dls_crecimiento_raiz(
    posicion_inicial[0],  # Coordenada x inicial
    posicion_inicial[1],  # Coordenada y inicial
    0,                    # Profundidad inicial (0)
    limite_crecimiento,   # Límite de profundidad
    nutrientes            # Lista para almacenar resultados
)

# =============================================
# MOSTRAR RESULTADOS FINALES
# =============================================

# Resumen de la simulación
print("\n💧 Resumen del crecimiento:")
print(f"Nutrientes encontrados: {len(nutrientes)}")
print(f"Posiciones: {nutrientes}")

# Mostrar el estado final del mapa
print("Mapa final:")
mostrar_suelo()