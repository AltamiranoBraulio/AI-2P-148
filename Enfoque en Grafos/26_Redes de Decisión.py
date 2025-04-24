import random  # Importamos el módulo random para posibles simulaciones aleatorias si fuera necesario

# Definir las probabilidades y resultados de un partido de fútbol
# En el diccionario DECISIONES, las claves son las decisiones de apuestas posibles
# y los valores son listas con los posibles resultados y sus respectivas probabilidades y utilidades.
DECISIONES = {
    # Apuesta por el Equipo A
    "Apostar a Equipo A": [
        {
            "resultado": "Victoria Equipo A",  # Resultado donde gana el Equipo A
            "probabilidad": 0.45,  # Probabilidad de que el Equipo A gane (45%)
            "utilidad": 100  # Ganancia de 100 si el Equipo A gana
        },
        {
            "resultado": "Victoria Equipo B",  # Resultado donde gana el Equipo B
            "probabilidad": 0.35,  # Probabilidad de que el Equipo B gane (35%)
            "utilidad": -10  # Pérdida de 10 si el Equipo A pierde
        },
        {
            "resultado": "Empate",  # Resultado en el que el partido termina en empate
            "probabilidad": 0.20,  # Probabilidad de empate (20%)
            "utilidad": -10  # Pérdida de 10 si el partido termina en empate
        }
    ],
    
    # Apuesta por el Equipo B
    "Apostar a Equipo B": [
        {
            "resultado": "Victoria Equipo B",  # Resultado donde gana el Equipo B
            "probabilidad": 0.35,  # Probabilidad de que el Equipo B gane (35%)
            "utilidad": 100  # Ganancia de 100 si el Equipo B gana
        },
        {
            "resultado": "Victoria Equipo A",  # Resultado donde gana el Equipo A
            "probabilidad": 0.45,  # Probabilidad de que el Equipo A gane (45%)
            "utilidad": -10  # Pérdida de 10 si el Equipo B pierde
        },
        {
            "resultado": "Empate",  # Resultado en el que el partido termina en empate
            "probabilidad": 0.20,  # Probabilidad de empate (20%)
            "utilidad": -10  # Pérdida de 10 si el partido termina en empate
        }
    ],
    
    # Apuesta por el Empate
    "Apostar a Empate": [
        {
            "resultado": "Empate",  # Resultado donde el partido termina en empate
            "probabilidad": 0.20,  # Probabilidad de empate (20%)
            "utilidad": 200  # Ganancia de 200 si el partido termina en empate
        },
        {
            "resultado": "Victoria Equipo A",  # Resultado donde gana el Equipo A
            "probabilidad": 0.45,  # Probabilidad de que el Equipo A gane (45%)
            "utilidad": -10  # Pérdida de 10 si el Equipo A gana
        },
        {
            "resultado": "Victoria Equipo B",  # Resultado donde gana el Equipo B
            "probabilidad": 0.35,  # Probabilidad de que el Equipo B gane (35%)
            "utilidad": -10  # Pérdida de 10 si el Equipo B gana
        }
    ]
}

# Función que calcula la utilidad ponderada de cada posible resultado
# Esta función recibe las utilidades y probabilidades de los resultados posibles
def calcular_utilidad_ponderada(utilidades, probabilidades):
    """
    Calcula la utilidad ponderada de cada resultado posible multiplicando la probabilidad por la utilidad.
    Luego suma todas las utilidades ponderadas.
    """
    # Usamos una lista por comprensión para multiplicar las probabilidades por las utilidades
    # y luego sumar los resultados.
    return sum(probabilidades[i] * utilidades[i] for i in range(len(utilidades)))

# Función que calcula la utilidad esperada de una apuesta
def utilidad_esperada(decision):
    """
    Calcula la utilidad esperada de una decisión en función de sus resultados probables.
    """
    # Obtenemos los posibles resultados de la apuesta según la decisión (Apostar a A, B o Empate)
    escenarios = DECISIONES[decision]
    # Inicializamos la utilidad total en cero
    utilidad_total = 0
    # Iteramos sobre los escenarios posibles para esa decisión
    for evento in escenarios:
        # Extraemos la utilidad y la probabilidad de cada resultado
        utilidad = evento["utilidad"]
        probabilidad = evento["probabilidad"]
        # Sumamos la utilidad ponderada al total
        utilidad_total += probabilidad * utilidad
    # Devolvemos la utilidad total calculada
    return utilidad_total

# Función que simula las decisiones de apuestas y recomienda la mejor opción
def simular_decisiones():
    """
    Simula la toma de decisiones sobre las apuestas y devuelve la mejor opción.
    """
    print("🧠 Simulador de Apuestas Deportivas: Partido de Fútbol\n")
    
    # Listamos las opciones de apuestas con su utilidad esperada
    mejores_opciones = []
    for decision in DECISIONES:
        # Calculamos la utilidad esperada para cada decisión
        ue = utilidad_esperada(decision)
        # Añadimos la decisión y su utilidad esperada a la lista de mejores opciones
        mejores_opciones.append((decision, ue))
        # Imprimimos el nombre de la decisión junto con su utilidad esperada
        print(f"🔹 {decision}: Utilidad esperada = {ue:.2f}")

    # Ordenamos las opciones de apuestas por la utilidad esperada, de mayor a menor
    mejores_opciones.sort(key=lambda x: x[1], reverse=True)
    
    # Imprimimos la mejor recomendación
    print("\n🚀 Recomendación estratégica:")
    print(f"👉 {mejores_opciones[0][0]} (Utilidad esperada: {mejores_opciones[0][1]:.2f})")
    
    # Devolvemos la mejor opción de apuesta, que es la que tiene la mayor utilidad esperada
    return mejores_opciones[0][0]

# Ejecutamos el simulador
# Este bloque de código se ejecutará solo cuando el script sea corrido directamente (no cuando sea importado como módulo)
if __name__ == "__main__":
    simular_decisiones()
