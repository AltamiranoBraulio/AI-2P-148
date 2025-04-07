import time
import random

# Mapa del suelo: 'T'=tierra, 'N'=nutriente, 'P'=piedra, 'R'=raíz
suelo = [
    ['T', 'T', 'T', 'T', 'T'],
    ['T', 'P', 'T', 'N', 'T'],
    ['T', 'T', 'P', 'T', 'T'],
    ['T', 'N', 'T', 'P', 'T'],
    ['T', 'T', 'T', 'T', 'N']
]

# Posición inicial de la raíz (centro)
posicion_inicial = (2, 2)
suelo[posicion_inicial[0]][posicion_inicial[1]] = 'R'

def mostrar_suelo():
    """Muestra el estado actual del suelo de forma visual"""
    print("\nEstado del suelo:")
    for fila in suelo:
        print(" ".join(fila))
    print()
    time.sleep(1)
    def dls_crecimiento_raiz(x, y, profundidad_actual, limite_profundidad, nutrientes_encontrados):
    """
    Simula el crecimiento de raíces usando DLS
    
    Args:
        x, y: Posición actual
        profundidad_actual: Profundidad de la raíz
        limite_profundidad: Límite máximo de crecimiento
        nutrientes_encontrados: Lista de nutrientes encontrados
    """
    # Mostrar el estado actual
    mostrar_suelo()

    # Si encontramos un nutriente
    if suelo[x][y] == 'N':
        print(f"¡Nutriente encontrado en ({x}, {y})!")
        nutrientes_encontrados.append((x, y))
        suelo[x][y] = 'R'  # La raíz absorbe el nutriente
        return
    
    # Si llegamos al límite de profundidad
    if profundidad_actual >= limite_profundidad:
        print(f"Límite de profundidad alcanzado en ({x}, {y})")
        return
     # Explorar direcciones posibles (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(direcciones)  # Para hacer el crecimiento más natural
    
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        
        # Verificar límites del terreno y obstáculos
        if 0 <= nx < len(suelo) and 0 <= ny < len(suelo[0]):
            if suelo[nx][ny] in ['T', 'N']:  # Solo tierra o nutrientes
                suelo[nx][ny] = 'R'  # Crece la raíz
                dls_crecimiento_raiz(nx, ny, profundidad_actual + 1, 
                                    limite_profundidad, nutrientes_encontrados)
                
# Simulación
print("🌱 SIMULADOR DE CRECIMIENTO DE RAÍCES 🌱")
print("Objetivo: Encontrar nutrientes (N) evitando piedras (P)")
print("Símbolos: R=Raíz, T=Tierra, N=Nutriente, P=Piedra\n")

# Mostrar estado inicial
mostrar_suelo()

# Configurar parámetros
limite_crecimiento = int(input("Ingresa el límite de profundidad para las raíces (1-5): "))
nutrientes = []

# Iniciar crecimiento
print("\nIniciando crecimiento de raíces...")
dls_crecimiento_raiz(posicion_inicial[0], posicion_inicial[1], 
                     0, limite_crecimiento, nutrientes)
# Resultados
print("\n💧 Resumen del crecimiento:")
print(f"Nutrientes encontrados: {len(nutrientes)}")
print(f"Posiciones: {nutrientes}")
print("Mapa final:")
mostrar_suelo()