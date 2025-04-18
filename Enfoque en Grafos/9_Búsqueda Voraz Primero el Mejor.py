import heapq
from collections import defaultdict
metro_gdl = {
    'Periférico Sur': {'Santuario': 5},
    'Santuario': {'Periférico Sur': 5, 'Washington': 3},
        'Washington': {'Santuario': 3, 'Juárez': 2},
    'Juárez': {'Washington': 2, 'Mexicaltzingo': 2},
    'Mexicaltzingo': {'Juárez': 2, 'Oblatos': 3},
    'Juárez': {'Plaza Universidad': 2},  # Conexión entre líneas
    'Plaza Universidad': {'Juárez': 2, 'San Juan de Dios': 3},
    'San Juan de Dios': {'Plaza Universidad': 3, 'Belisario Domínguez': 2},
    'Central de Autobuses': {'Periférico Belenes': 4},
    'Periférico Belenes': {'Central de Autobuses': 4, 'San Andrés': 3}
}
heuristicas_gdl = {
    'Periférico Sur': 6,
    'Santuario': 5,
    'Washington': 3,
    'Juárez': 1,
    'Mexicaltzingo': 2,
    'Oblatos': 3,
    'Plaza Universidad': 0,  # Nuestro destino
    'San Juan de Dios': 1,
    'Belisario Domínguez': 2,
    'Central de Autobuses': 4,
    'Periférico Belenes': 3,
    'San Andrés': 2
}
def buscar_ruta_metro(origen, destino):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (heuristicas_gdl[origen], origen, [origen]))
    visitados = set()
    print(f"🔍 Buscando ruta de {origen} a {destino}...")
    while cola_prioridad:
        _, estacion, ruta = heapq.heappop(cola_prioridad)
        if estacion == destino:
            print(f"\n🎉 Ruta encontrada ({len(ruta)-1} transbordos):")
            print(" → ".join(ruta))
            print("\n🚇 Estaciones:", len(ruta))
            print("🔄 Transbordos:", len([x for x in ruta if x == 'Juárez'])-1)
            return ruta

