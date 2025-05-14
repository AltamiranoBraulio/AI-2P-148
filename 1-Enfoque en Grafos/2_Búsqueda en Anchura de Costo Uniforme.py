import heapq  # Importa la biblioteca heapq, que permite trabajar con colas de prioridad (mínimos)
import time   # Importa la biblioteca time, usada para añadir pausas temporales (efecto visual)

# Diccionario que representa el mapa del Reino Mágico.
# Cada ciudad está conectada a otras con un "costo de viaje" (en monedas de oro).
reino_magico = {
    'Aldea Inicial': {'Valle Brillante': 5, 'Bosque Encantado': 3},
    'Valle Brillante': {'Aldea Inicial': 5, 'Montaña Nevada': 8, 'Ciudad Esmeralda': 10},
    'Bosque Encantado': {'Aldea Inicial': 3, 'Ciudad Esmeralda': 6, 'Pantano Sombrío': 4},
    'Montaña Nevada': {'Valle Brillante': 8, 'Castillo del Rey': 15},
    'Ciudad Esmeralda': {'Valle Brillante': 10, 'Bosque Encantado': 6, 'Castillo del Rey': 3},
    'Pantano Sombrío': {'Bosque Encantado': 4, 'Isla Perdida': 12},
    'Castillo del Rey': {'Montaña Nevada': 15, 'Ciudad Esmeralda': 3},
    'Isla Perdida': {'Pantano Sombrío': 12}
}

# Función que implementa la búsqueda de costo uniforme (UCS: Uniform Cost Search)
# Encuentra el camino más barato (económico) entre dos ciudades
def viaje_mas_economico(grafo, inicio, destino):
    """
    Encuentra el viaje más económico entre dos ciudades usando UCS.
    Devuelve el camino y el costo total.
    """

    # Creamos una cola de prioridad llamada 'frontera'.
    # Cada elemento de la cola es una tupla: (costo acumulado, ciudad actual, camino recorrido)
    frontera = []
    heapq.heappush(frontera, (0, inicio, []))  # Insertamos el nodo inicial con costo 0 y sin camino previo

    # Conjunto para llevar registro de ciudades ya visitadas (evita ciclos y repeticiones)
    ciudades_visitadas = set()
    
    # Mientras haya nodos en la frontera por explorar...
    while frontera:
        # Sacamos la ciudad con menor costo acumulado hasta ahora
        costo, ciudad, camino = heapq.heappop(frontera)
        
        # Si ya llegamos a la ciudad destino, devolvemos el camino y el costo total
        if ciudad == destino:
            return camino + [ciudad], costo  # Agregamos la ciudad actual al camino final y devolvemos

        # Si la ciudad aún no fue visitada...
        if ciudad not in ciudades_visitadas:
            ciudades_visitadas.add(ciudad)  # Marcamos la ciudad como visitada
            
            # Mostramos en pantalla qué ciudad estamos visitando y cuánto costó llegar
            print(f"✨ Visitando {ciudad} (Costo acumulado: {costo} monedas)")
            time.sleep(1)  # Esperamos un segundo (simula una pausa dramática para el usuario)
            
            # Recorremos todas las ciudades vecinas conectadas a la ciudad actual
            for ciudad_vecina, costo_viaje in grafo[ciudad].items():
                # Si la ciudad vecina no ha sido visitada aún...
                if ciudad_vecina not in ciudades_visitadas:
                    nuevo_camino = camino + [ciudad]  # Actualizamos el camino añadiendo la ciudad actual
                    # Añadimos la ciudad vecina a la frontera con su costo total hasta ahora
                    heapq.heappush(frontera, (costo + costo_viaje, ciudad_vecina, nuevo_camino))
    
    # Si no se encuentra una ruta al destino, devolvemos None y costo infinito
    return None, float('inf')

# --- Simulación interactiva del planificador de viaje ---

# Mensajes de introducción para el usuario
print("🏰 ¡Bienvenido al Planificador de Viajes del Reino Mágico! 🏰")
print("Calculando la ruta más económica...\n")

# Definimos la ciudad de partida y la de destino
inicio = 'Aldea Inicial'
destino = 'Castillo del Rey'

# Llamamos a la función para calcular el camino más barato
camino, costo = viaje_mas_economico(reino_magico, inicio, destino)

# Si se encontró un camino, lo mostramos con detalles
if camino:
    print("\n⚡ ¡Ruta encontrada! ⚡")
    print(f"📍 Camino: {' → '.join(camino)}")  # Unimos el camino con flechas para mostrar la ruta
    print(f"💰 Costo total: {costo} monedas de oro")  # Mostramos el costo final del viaje
    
    # Mostramos otras rutas posibles manualmente calculadas (referencias adicionales)
    print("\nOtras rutas posibles:")
    print("1. Aldea Inicial → Valle Brillante → Castillo del Rey (Costo: 5 + 15 = 20)")
    print("2. Aldea Inicial → Bosque Encantado → Ciudad Esmeralda → Castillo del Rey (Costo: 3 + 6 + 3 = 12)")
else:
    # Si no se encontró ruta posible, se informa al usuario
    print("No hay ruta disponible hasta el destino.")
