import random  # Importamos la librería estándar 'random' para generar números aleatorios

# --- Definimos las zonas y sus probabilidades de encontrar el tesoro --- #

# Diccionario donde las llaves son las zonas y los valores son las probabilidades
zonas = {
    'Bosque': 0.6,    # El Bosque tiene una alta probabilidad de contener el tesoro (60%)
    'Montaña': 0.3,   # La Montaña tiene una probabilidad media (30%)
    'Pantano': 0.1    # El Pantano es difícil, solo 10% de probabilidad
}

# --- Función de Muestreo Directo --- #
def muestreo_directo(zonas, n_busquedas):
    """
    Simula 'n_busquedas' elecciones de zona basadas directamente en las probabilidades dadas.
    """
    elecciones = []  # Lista donde guardaremos las zonas elegidas
    nombres_zonas = list(zonas.keys())  # Lista de los nombres de las zonas
    probabilidades = list(zonas.values())  # Lista de las probabilidades asociadas a cada zona

    # Repetimos la búsqueda n veces
    for _ in range(n_busquedas):
        # random.choices permite elegir un elemento según un peso asignado
        zona = random.choices(nombres_zonas, weights=probabilidades, k=1)[0]
        elecciones.append(zona)  # Guardamos la zona elegida
    
    return elecciones  # Devolvemos la lista de elecciones

# --- Función de Muestreo por Rechazo --- #
def muestreo_por_rechazo(zonas, n_busquedas):
    """
    Simula 'n_busquedas' elecciones aplicando la técnica de muestreo por rechazo.
    En este caso, hay un 'peligro' adicional al elegir una zona.
    """
    elecciones = []  # Lista donde guardaremos las zonas elegidas
    nombres_zonas = list(zonas.keys())  # Lista de zonas
    probabilidades = list(zonas.values())  # Lista de probabilidades
    prob_maxima = max(probabilidades)  # Guardamos la mayor probabilidad para normalizar

    # Continuamos hasta lograr la cantidad de elecciones necesarias
    while len(elecciones) < n_busquedas:
        zona_propuesta = random.choice(nombres_zonas)  # Elegimos una zona al azar SIN considerar probabilidades

        peligro = random.uniform(0, 1)  # Simulamos un nivel de peligro (0 a 1)

        u = random.uniform(0, prob_maxima)  
        # Número aleatorio para decidir si aceptamos la propuesta, normalizado al máximo de probabilidades

        # Condiciones para aceptar:
        # - El peligro no debe ser alto (>= 0.2 es un camino "seguro")
        # - El número aleatorio debe ser menor o igual a la probabilidad de la zona propuesta
        if peligro >= 0.2 and u <= zonas[zona_propuesta]:
            elecciones.append(zona_propuesta)  # Aceptamos la zona segura y añadimos
        # Si no, rechazamos y repetimos el proceso (no se suma nada)
    
    return elecciones  # Devolvemos la lista final de elecciones

# --- Ejecutamos ambas simulaciones --- #

# Simulación de Muestreo Directo
print("🔵 Exploradores usando Muestreo Directo:")
resultado_directo = muestreo_directo(zonas, 15)  # Realizamos 15 búsquedas
print(resultado_directo)  # Mostramos las zonas elegidas

# Simulación de Muestreo por Rechazo
print("\n🟢 Exploradores usando Muestreo por Rechazo:")
resultado_rechazo = muestreo_por_rechazo(zonas, 15)  # Realizamos 15 búsquedas
print(resultado_rechazo)  # Mostramos las zonas elegidas
