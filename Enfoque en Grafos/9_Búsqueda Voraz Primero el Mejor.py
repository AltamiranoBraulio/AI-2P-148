# Importación de módulos necesarios
# heapq: Para implementar la cola de prioridad (usaremos heappush y heappop)
# defaultdict: Para crear diccionarios con valores por defecto (aunque no se usa directamente aquí)
import heapq
from collections import defaultdict

# =============================================
# DEFINICIÓN DE LA RED DEL METRO DE GUADALAJARA
# =============================================
# Estructura de datos: Grafo representado como diccionario de diccionarios
# Cada clave es una estación, y su valor es otro diccionario con:
#   - Clave: estación conectada
#   - Valor: tiempo aproximado de viaje en minutos (aunque en este algoritmo no se usa)
metro_gdl = {
    # Línea 1 (Verde) - Sur a Norte
    'Periférico Sur': {'Santuario': 5},  # 5 minutos a Santuario
    'Santuario': {
        'Periférico Sur': 5,  # Conexión bidireccional
        'Washington': 3  # 3 minutos a Washington
    },
    'Washington': {
        'Santuario': 3,
        'Juárez': 2  # 2 minutos a Juárez (estación de transbordo)
    },
    # Juárez es estación de transbordo entre Línea 1 y Línea 2
    'Juárez': {
        'Washington': 2,
        'Mexicaltzingo': 2,  # Continuación Línea 1
        'Plaza Universidad': 2  # Conexión a Línea 2
    },
    'Mexicaltzingo': {
        'Juárez': 2,
        'Oblatos': 3  # 3 minutos a Oblatos
    },
    
    # Línea 2 (Amarilla) - Centro
    'Plaza Universidad': {
        'Juárez': 2,
        'San Juan de Dios': 3  # 3 minutos a San Juan de Dios
    },
    'San Juan de Dios': {
        'Plaza Universidad': 3,
        'Belisario Domínguez': 2  # 2 minutos a Belisario Domínguez
    },
    
    # Línea 3 (Roja) - Occidente a Oriente
    'Central de Autobuses': {
        'Periférico Belenes': 4  # 4 minutos a Periférico Belenes
    },
    'Periférico Belenes': {
        'Central de Autobuses': 4,
        'San Andrés': 3  # 3 minutos a San Andrés
    },
    # Nota: En la realidad, la Línea 3 tiene más estaciones
}

# =============================================
# HEURÍSTICAS PARA LA BÚSQUEDA
# =============================================
# Diccionario que asigna a cada estación un valor heurístico (estimado)
# Representa la "distancia estimada" en número de estaciones hasta Plaza Universidad (nuestro destino)
heuristicas_gdl = {
    'Periférico Sur': 6,  # Estimado: 6 estaciones de distancia
    'Santuario': 5,
    'Washington': 3,
    'Juárez': 1,  # Solo 1 estación de Plaza Universidad
    'Mexicaltzingo': 2,
    'Oblatos': 3,
    'Plaza Universidad': 0,  # ¡Estamos aquí!
    'San Juan de Dios': 1,
    'Belisario Domínguez': 2,
    'Central de Autobuses': 4,
    'Periférico Belenes': 3,
    'San Andrés': 2
}

# =============================================
# FUNCIÓN PRINCIPAL DE BÚSQUEDA VORAZ
# =============================================
def buscar_ruta_metro(origen, destino):
    # Inicializamos una cola de prioridad (min-heap)
    cola_prioridad = []
    
    # El heap almacenará tuplas con:
    # 1. Valor heurístico (para priorizar)
    # 2. Nombre de la estación actual
    # 3. Lista con el camino recorrido hasta ahora
    heapq.heappush(cola_prioridad, (heuristicas_gdl[origen], origen, [origen]))
    
    # Conjunto para llevar registro de estaciones ya visitadas
    # Evitamos ciclos infinitos y reprocesamiento
    visitados = set()
    
    # Mensaje inicial
    print(f"🔍 Buscando ruta de {origen} a {destino}...")
    
    # Bucle principal: se ejecuta mientras haya nodos por explorar
    while cola_prioridad:
        # Extraemos la estación con menor valor heurístico
        _, estacion, ruta = heapq.heappop(cola_prioridad)
        
        # Condición de éxito: hemos llegado al destino
        if estacion == destino:
            # Calculamos estadísticas de la ruta
            num_transbordos = len([x for x in ruta if x == 'Juárez']) - 1
            
            # Mostramos resultados
            print(f"\n🎉 Ruta encontrada ({num_transbordos} transbordos):")
            print(" → ".join(ruta))
            print("\n📊 Estadísticas:")
            print(f"🚇 Estaciones totales: {len(ruta)}")
            print(f"🔄 Transbordos: {num_transbordos}")
            return ruta
            
        # Si no hemos visitado esta estación...
        if estacion not in visitados:
            # La marcamos como visitada
            visitados.add(estacion)
            
            # Exploramos todas sus conexiones
            for conexion, _ in metro_gdl.get(estacion, {}).items():
                # Si la conexión no ha sido visitada
                if conexion not in visitados:
                    # Calculamos la nueva ruta (camino actual + nueva estación)
                    nueva_ruta = ruta + [conexion]
                    
                    # Añadimos a la cola de prioridad con su valor heurístico
                    heapq.heappush(cola_prioridad, 
                                 (heuristicas_gdl[conexion], 
                                  conexion, 
                                  nueva_ruta))
    
    # Si salimos del while sin retornar, no hay ruta
    print("\n⚠️ No hay ruta disponible")
    return None

# =============================================
# EJECUCIÓN DEL PROGRAMA
# =============================================
print("=== SISTEMA DE RUTAS DEL METRO DE GUADALAJARA ===")
print("=== (Algoritmo de Búsqueda Voraz) ===")
print("\nEstaciones disponibles:")
print(", ".join(metro_gdl.keys()))

# Definimos origen y destino
origen = 'Periférico Sur'
destino = 'Plaza Universidad'

# Ejecutamos la búsqueda
buscar_ruta_metro(origen, destino)