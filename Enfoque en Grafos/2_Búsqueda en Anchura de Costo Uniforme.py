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