import random

# Configuración del dilema
RECOMPENSAS = {
    ('C', 'C'): (3, 3),
    ('C', 'T'): (0, 5),
    ('T', 'C'): (5, 0),
    ('T', 'T'): (1, 1)
}

# Estrategias base
def cooperador(_history): return 'C'
def traidor(_history): return 'T'

# Tit for Tat (responde lo que hizo el oponente en la ronda anterior)
def tit_for_tat(history):
    if not history: return 'C'
    return history[-1][1]

# Evolución entre generaciones
class Jugador:
    def __init__(self, estrategia_func):
        self.estrategia_func = estrategia_func
        self.historia = []
        self.score = 0

    def jugar(self, oponente):
        a = self.estrategia_func(self.historia)
        b = oponente.estrategia_func(oponente.historia)
        s1, s2 = RECOMPENSAS[(a, b)]
        self.historia.append((a, b))
        oponente.historia.append((b, a))
        self.score += s1
        oponente.score += s2

# Simulación de generaciones
def simular_generaciones(generaciones=10, n=10):
    poblacion = []
    for _ in range(n // 3):
        poblacion.append(Jugador(cooperador))
        poblacion.append(Jugador(traidor))
        poblacion.append(Jugador(tit_for_tat))

    for gen in range(generaciones):
        print(f"\n--- Generación {gen+1} ---")
        for jugador in poblacion:
            jugador.score = 0
            jugador.historia = []

        # Todos contra todos
        for i in range(len(poblacion)):
            for j in range(i + 1, len(poblacion)):
                for _ in range(5):  # 5 rondas por par
                    poblacion[i].jugar(poblacion[j])

        # Imprimir puntajes
        scores = [(jugador.score, jugador.estrategia_func.__name__) for jugador in poblacion]
        scores.sort(reverse=True)
        for s, name in scores:
            print(f"{name}: {s}")

        # Evolución: los peores se reemplazan por copias de los mejores
        scores_sorted = sorted(poblacion, key=lambda x: x.score, reverse=True)
        top = scores_sorted[:len(poblacion)//2]
        poblacion = [Jugador(j.estrategia_func) for j in top for _ in range(2)]

simular_generaciones(10, 12)
