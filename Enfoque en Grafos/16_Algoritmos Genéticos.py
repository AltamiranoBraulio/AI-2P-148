# 🍊 Optimizador Evolutivo de Recetas de Jugo
# Autor: Babyarm (con ayuda de ChatGPT)
# Descripción: Algoritmo genético para encontrar la mejor mezcla de jugo

import random  # Para generar números aleatorios
from typing import List, Tuple  # Para anotar tipos en listas y tuplas
from collections import namedtuple  # Para definir estructuras simples

# 🧃 Definimos un ingrediente con nombre, mínimo y máximo porcentaje
Ingrediente = namedtuple('Ingrediente', ['nombre', 'min', 'max'])

# Un jugo es simplemente una lista de porcentajes de ingredientes
Jugo = List[float]

# 🔬 Clase que implementa el algoritmo genético
class OptimizadorJugo:
    def __init__(self):
        # Ingredientes con sus límites de porcentaje
        self.ingredientes = [
            Ingrediente('Naranja', 20, 70),
            Ingrediente('Zanahoria', 5, 30),
            Ingrediente('Jengibre', 0, 10),
            Ingrediente('Limón', 0, 15),
            Ingrediente('Remolacha', 0, 25)
        ]

    def generar_individuo(self) -> Jugo:
        """
        Genera una receta válida con ingredientes aleatorios que sumen ~100%
        """
        while True:
            receta = [random.uniform(i.min, i.max) for i in self.ingredientes]
            total = sum(receta)
            if 99 <= total <= 101:
                return [x / total * 100 for x in receta]

    def evaluar(self, jugo: Jugo) -> float:
        """
        Evalúa la calidad de una receta basada en criterios arbitrarios.
        """
        puntaje = 0
        puntaje += min(jugo[0], 50) * 1.2  # Naranja
        puntaje += min(jugo[1], 20) * 0.8  # Zanahoria
        puntaje += min(jugo[2], 3) * 2.0   # Jengibre
        puntaje -= abs(jugo[3] - 8) * 1.5  # Limón (ideal 8%)
        puntaje += min(jugo[4], 15) * 0.6  # Remolacha
        puntaje -= abs(sum(jugo) - 100) * 10  # Penalización si no suma 100
        return puntaje

    def cruzar(self, padre1: Jugo, padre2: Jugo) -> Tuple[Jugo, Jugo]:
        """
        Cruza dos recetas en un punto aleatorio.
        """
        punto = random.randint(1, len(self.ingredientes) - 2)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2

    def mutar(self, jugo: Jugo) -> Jugo:
        """
        Aplica una mutación a un ingrediente aleatorio.
        """
        mutado = jugo.copy()
        idx = random.randint(0, len(mutado) - 1)
        cambio = random.gauss(0, 5)
        mutado[idx] = max(self.ingredientes[idx].min,
                          min(self.ingredientes[idx].max,
                              mutado[idx] + cambio))
        total = sum(mutado)
        return [x / total * 100 for x in mutado]

# 🧬 Selección por torneo: elige los mejores individuos entre grupos pequeños
def seleccion_por_torneo(poblacion: List[Jugo], aptitudes: List[float], tam_torneo=3) -> List[Jugo]:
    seleccionados = []
    for _ in range(len(poblacion)):
        contendientes = random.sample(list(zip(poblacion, aptitudes)), tam_torneo)
        seleccionados.append(max(contendientes, key=lambda x: x[1])[0])
    return seleccionados

# 🧪 Algoritmo genético completo
def algoritmo_genetico_recetas(generaciones=50, tam_poblacion=30) -> Tuple[Jugo, float, OptimizadorJugo]:
    optimizador = OptimizadorJugo()
    poblacion = [optimizador.generar_individuo() for _ in range(tam_poblacion)]

    mejor_aptitud = -float('inf')
    mejor_receta = None

    for gen in range(generaciones):
        aptitudes = [optimizador.evaluar(ind) for ind in poblacion]
        max_apt = max(aptitudes)

        if max_apt > mejor_aptitud:
            mejor_aptitud = max_apt
            mejor_receta = poblacion[aptitudes.index(max_apt)]
            print(f"Gen {gen}: Nueva mejor aptitud = {mejor_aptitud:.2f}")

        padres = seleccion_por_torneo(poblacion, aptitudes)
        descendencia = []

        for i in range(0, len(padres) - 1, 2):
            hijo1, hijo2 = optimizador.cruzar(padres[i], padres[i + 1])
            descendencia.append(optimizador.mutar(hijo1))
            descendencia.append(optimizador.mutar(hijo2))

        poblacion = [mejor_receta] + descendencia[:tam_poblacion - 1]

    return mejor_receta, mejor_aptitud, optimizador

# 🏁 Punto de entrada del programa
if __name__ == "__main__":
    print("🍹 Optimizador Evolutivo de Recetas de Jugo 🧬")

    receta, aptitud, optimizador = algoritmo_genetico_recetas()

    print("\n🥇 Mejor receta encontrada:")
    for i, ing in enumerate(optimizador.ingredientes):
        print(f"- {ing.nombre}: {receta[i]:.1f}%")
    print(f"\nPuntaje de calidad: {aptitud:.2f}")
