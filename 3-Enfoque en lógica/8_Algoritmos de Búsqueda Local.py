import random
import math

# Definir la función que queremos maximizar
def funcion(x):
    return -x**2 + 4*x  # La función f(x) = -x^2 + 4x

# Función para realizar un paso de ascenso de colina
def ascenso_de_colina(funcion, solucion_inicial, tasa_aprendizaje=0.1, max_iter=100):
    solucion = solucion_inicial
    for _ in range(max_iter):
        # Generamos una pequeña perturbación en la solución actual
        vecino = solucion + random.uniform(-tasa_aprendizaje, tasa_aprendizaje)
        
        # Si el vecino tiene un mejor valor de la función, actualizamos la solución
        if funcion(vecino) > funcion(solucion):
            solucion = vecino
            
    return solucion

# Usamos el ascenso de colina comenzando desde una solución inicial aleatoria
solucion_inicial = random.uniform(-10, 10)  # Empezamos con un valor aleatorio entre -10 y 10
solucion_optima = ascenso_de_colina(funcion, solucion_inicial)

# Mostrar la solución encontrada
print(f"Solución inicial: {solucion_inicial}")
print(f"Solución óptima encontrada: {solucion_optima}")
print(f"Valor de la función en la solución óptima: {funcion(solucion_optima)}")
