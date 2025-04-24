# Importamos la librería random que nos permitirá generar valores aleatorios
import random

# 🧪 Ponderación de prioridades: cuánto valora la colonia cada factor
# Aquí estamos definiendo qué tan importante es cada criterio para la colonia.
# La vida tiene el mayor peso (0.5), seguido por moral (0.2), tecnología (0.2), y recursos (0.1).
PESOS = {
    "vida": 0.5,       # La vida tiene un peso de 0.5 en la decisión final.
    "moral": 0.2,      # La moral tiene un peso de 0.2 en la decisión final.
    "tecnología": 0.2, # La tecnología también tiene un peso de 0.2.
    "recursos": 0.1    # Los recursos tienen el peso más bajo (0.1).
}

# 📦 Acciones posibles con escenarios y probabilidades
# Aquí definimos varias decisiones que puede tomar el comandante de la colonia.
# Cada decisión tiene una lista de posibles resultados (eventos), con una probabilidad de que ocurran y la utilidad asociada a cada resultado.
DECISIONES = {
    "Explorar cueva subterránea": [  # Decisión 1: Explorar una cueva subterránea.
        {
            "resultado": "Descubrimiento científico",  # Un posible resultado es hacer un descubrimiento científico.
            "probabilidad": 0.3,                      # Este evento tiene una probabilidad del 30%.
            "utilidad": {"vida": 0, "moral": 10, "tecnología": 40, "recursos": 5}  # La utilidad de este evento: más moral, más tecnología, pocos recursos.
        },
        {
            "resultado": "Accidente fatal",  # Otro posible resultado es un accidente fatal.
            "probabilidad": 0.2,            # Este evento tiene una probabilidad del 20%.
            "utilidad": {"vida": -50, "moral": -20, "tecnología": 0, "recursos": -10}  # La utilidad: la vida se ve gravemente afectada, moral baja, y recursos también disminuyen.
        },
        {
            "resultado": "Sin hallazgos",  # El tercer resultado es no encontrar nada en la cueva.
            "probabilidad": 0.5,            # Este evento tiene una probabilidad del 50%.
            "utilidad": {"vida": 0, "moral": -5, "tecnología": 0, "recursos": 0}  # No hay cambios en vida o tecnología, pero la moral baja ligeramente.
        }
    ],
    "Construir invernadero": [  # Decisión 2: Construir un invernadero.
        {
            "resultado": "Autoabastecimiento exitoso",  # Un posible resultado es un autoabastecimiento exitoso.
            "probabilidad": 0.6,  # Este evento tiene una probabilidad del 60%.
            "utilidad": {"vida": 20, "moral": 15, "tecnología": 0, "recursos": 25}  # La utilidad de este evento: mejora la vida y la moral, recursos adicionales.
        },
        {
            "resultado": "Fallo estructural",  # Otro posible resultado es un fallo estructural.
            "probabilidad": 0.2,  # Este evento tiene una probabilidad del 20%.
            "utilidad": {"vida": -10, "moral": -10, "tecnología": -5, "recursos": -30}  # La utilidad de este evento: la vida y moral disminuyen, la tecnología empeora y se pierden recursos.
        },
        {
            "resultado": "Resultado neutro",  # Un tercer resultado es que no pase nada relevante.
            "probabilidad": 0.2,  # Este evento tiene una probabilidad del 20%.
            "utilidad": {"vida": 0, "moral": 0, "tecnología": 0, "recursos": 0}  # Sin cambios en los valores de vida, moral, tecnología ni recursos.
        }
    ],
    "Lanzar señal interestelar": [  # Decisión 3: Lanzar una señal hacia el espacio.
        {
            "resultado": "Rescate detectado",  # Un posible resultado es que se detecte una señal de rescate.
            "probabilidad": 0.1,  # Este evento tiene una probabilidad del 10%.
            "utilidad": {"vida": 50, "moral": 30, "tecnología": 10, "recursos": -10}  # La utilidad de este evento: se mejora la vida y moral, pero se pierden recursos.
        },
        {
            "resultado": "Respuesta hostil",  # Otro posible resultado es que la respuesta sea hostil.
            "probabilidad": 0.1,  # Este evento tiene una probabilidad del 10%.
            "utilidad": {"vida": -30, "moral": -25, "tecnología": 0, "recursos": -15}  # La utilidad de este evento: vida y moral se ven muy afectadas, recursos se pierden.
        },
        {
            "resultado": "Sin respuesta",  # El tercer resultado es que no haya ninguna respuesta.
            "probabilidad": 0.8,  # Este evento tiene una probabilidad del 80%.
            "utilidad": {"vida": 0, "moral": -5, "tecnología": 0, "recursos": 0}  # La utilidad de este evento: sin cambios en la vida o tecnología, pero la moral disminuye ligeramente.
        }
    ]
}

# 🎯 Función que calcula la utilidad total ponderada
# Esta función calcula la "utilidad ponderada" para un conjunto de utilidades, usando los pesos definidos previamente.
# Lo que hace es multiplicar el valor de cada factor por su peso respectivo y luego sumar los resultados.
def calcular_utilidad_ponderada(utilidades, pesos):
    # Itera sobre todos los factores (vida, moral, etc.), calcula su valor ponderado y lo suma.
    return sum(utilidades[factor] * pesos[factor] for factor in utilidades)

# 📊 Calcula la utilidad esperada de una decisión
# Esta función toma una decisión (por ejemplo, "Explorar cueva subterránea") y calcula la utilidad esperada
# basándose en las probabilidades de los distintos eventos y las utilidades asociadas.
def utilidad_esperada(decision):
    # Obtiene los escenarios posibles para la decisión actual.
    escenarios = DECISIONES[decision]
    
    # Inicializa la variable que almacenará la utilidad total esperada.
    utilidad_total = 0
    
    # Itera sobre cada uno de los escenarios posibles para la decisión.
    for evento in escenarios:
        # Calcula la utilidad ponderada para el evento actual usando la función calcular_utilidad_ponderada.
        u = calcular_utilidad_ponderada(evento["utilidad"], PESOS)
        
        # Multiplica la utilidad ponderada por la probabilidad del evento y sumamos al total.
        utilidad_total += evento["probabilidad"] * u
    
    # Retorna la utilidad total esperada de la decisión.
    return utilidad_total

# 🤖 Simulador de decisiones
# Esta función simula el proceso de tomar decisiones en base a la utilidad esperada.
def simular_decisiones():
    print("🧠 Simulador de Estrategia: Colonia Marte 2189\n")  # Imprime el título del simulador.
    
    # Lista para almacenar las decisiones y sus utilidades esperadas.
    mejores_opciones = []
    
    # Itera sobre todas las decisiones posibles definidas en el diccionario DECISIONES.
    for decision in DECISIONES:
        # Calcula la utilidad esperada para cada decisión usando la función utilidad_esperada.
        ue = utilidad_esperada(decision)
        
        # Agrega la decisión y su utilidad esperada a la lista de mejores opciones.
        mejores_opciones.append((decision, ue))
        
        # Imprime la decisión y su utilidad esperada calculada.
        print(f"🔹 {decision}: Utilidad esperada = {ue:.2f}")
    
    # Ordena las decisiones por su utilidad esperada, de mayor a menor.
    mejores_opciones.sort(key=lambda x: x[1], reverse=True)
    
    # Imprime la recomendación estratégica basada en la decisión con la mayor utilidad esperada.
    print("\n🚀 Recomendación estratégica:")
    print(f"👉 {mejores_opciones[0][0]} (Utilidad esperada: {mejores_opciones[0][1]:.2f})")

    # Retorna la mejor decisión (la de mayor utilidad esperada).
    return mejores_opciones[0][0]

# 🎬 Ejecutamos el simulador de decisiones
# Este bloque de código es el que inicia el proceso del simulador.
if __name__ == "__main__":
    simular_decisiones()
