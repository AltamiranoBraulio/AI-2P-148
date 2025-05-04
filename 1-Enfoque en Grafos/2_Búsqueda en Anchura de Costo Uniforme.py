import heapq
import time

# Mapa del reino mágico con costos de viaje (en monedas de oro)
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

def viaje_mas_economico(grafo, inicio, destino):
    """
    Encuentra el viaje más económico entre dos ciudades usando UCS.
    Devuelve el camino y el costo total.
    """
    # Cola de prioridad: (costo_acumulado, ciudad_actual, camino)
    frontera = []
    heapq.heappush(frontera, (0, inicio, []))
    
    ciudades_visitadas = set()
    
    while frontera:
        costo, ciudad, camino = heapq.heappop(frontera)
        
        if ciudad == destino:
            return camino + [ciudad], costo  # Esta línea DEBE estar indentada
        
        if ciudad not in ciudades_visitadas:
            ciudades_visitadas.add(ciudad)
            
            print(f"✨ Visitando {ciudad} (Costo acumulado: {costo} monedas)")
            time.sleep(1)  # Pausa dramática
            
            for ciudad_vecina, costo_viaje in grafo[ciudad].items():
                if ciudad_vecina not in ciudades_visitadas:
                    nuevo_camino = camino + [ciudad]
                    heapq.heappush(frontera, (costo + costo_viaje, ciudad_vecina, nuevo_camino))
    
    return None, float('inf')

# Simulación del viaje
print("🏰 ¡Bienvenido al Planificador de Viajes del Reino Mágico! 🏰")
print("Calculando la ruta más económica...\n")

inicio = 'Aldea Inicial'
destino = 'Castillo del Rey'

camino, costo = viaje_mas_economico(reino_magico, inicio, destino)

if camino:
    print("\n⚡ ¡Ruta encontrada! ⚡")
    print(f"📍 Camino: {' → '.join(camino)}")
    print(f"💰 Costo total: {costo} monedas de oro")
    
    print("\nOtras rutas posibles:")
    print("1. Aldea Inicial → Valle Brillante → Castillo del Rey (Costo: 5 + 15 = 20)")
    print("2. Aldea Inicial → Bosque Encantado → Ciudad Esmeralda → Castillo del Rey (Costo: 3 + 6 + 3 = 12)")
else:
    print("No hay ruta disponible hasta el destino.")