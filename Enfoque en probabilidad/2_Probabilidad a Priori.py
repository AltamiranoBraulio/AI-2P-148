# Importamos la librería random para poder hacer selecciones aleatorias
import random  

# --- DATOS INICIALES ---

# Definimos un diccionario llamado 'equipos'
# Cada equipo tiene asociado un valor numérico que representa su "fuerza"
# Cuanto mayor sea la fuerza, más posibilidades tiene de ganar el torneo
equipos = {
    "Leones": 90,
    "Tigres": 70,
    "Águilas": 50,
    "Lobos": 30,
    "Serpientes": 10
}

# Calculamos la suma total de todas las fuerzas
# Esto servirá para normalizar las probabilidades
fuerza_total = sum(equipos.values())

# Mostramos en pantalla las probabilidades a priori de ganar el torneo para cada equipo
print("🏆 Probabilidad a priori de ganar el torneo:")

# Creamos un diccionario vacío para guardar las probabilidades calculadas
probabilidades = {}

# Recorremos cada equipo y su fuerza en el diccionario 'equipos'
for equipo, fuerza in equipos.items():
    # Calculamos la probabilidad de cada equipo como (fuerza del equipo) / (fuerza total)
    prob = fuerza / fuerza_total
    # Guardamos esta probabilidad en el diccionario 'probabilidades'
    probabilidades[equipo] = prob
    # Imprimimos el nombre del equipo junto con su probabilidad
    # Se muestra en formato decimal y porcentaje
    print(f"   {equipo}: {prob:.2f} ({prob*100:.1f}%)")

# --- SIMULACIÓN DE UN TORNEO SENCILLO ---

# Indicamos que vamos a simular un torneo
print("\n🎲 Simulando un torneo...")

# Creamos una lista vacía llamada 'urna'
# La idea es llenar la urna con los nombres de los equipos repetidos tantas veces como su fuerza
urna = []

# Recorremos cada equipo y su fuerza en 'equipos'
for equipo, fuerza in equipos.items():
    # Agregamos el nombre del equipo a la urna 'fuerza' veces
    # Por ejemplo, si 'Leones' tiene fuerza 90, lo agregamos 90 veces
    urna.extend([equipo] * fuerza)

# Ahora que la urna está llena, hacemos una elección aleatoria
# Elegimos un equipo de manera aleatoria ponderada (porque hay más repeticiones para equipos más fuertes)
ganador = random.choice(urna)

# Mostramos en pantalla el equipo que ganó el torneo en esta simulación
print(f"\n🏆 ¡El ganador del torneo es: {ganador}!")

# --- COMPARACIÓN TEÓRICA Y SIMULADA ---

# Recordatorio importante:
# Explicamos que en una sola simulación los resultados pueden no coincidir exactamente con las probabilidades teóricas
print("\n📈 (Nota: en una sola simulación puede no coincidir con la probabilidad teórica)")
# También aclaramos que si se simulan muchos torneos, los resultados reales se acercarán mucho a las probabilidades teóricas
print("📈 (Si simulas miles de torneos, las frecuencias se acercarán a las probabilidades a priori)")
