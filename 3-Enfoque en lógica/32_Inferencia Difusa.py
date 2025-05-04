import numpy as np
import matplotlib.pyplot as plt

class SistemaInferenciaDifusa:
    """
    Esta clase implementa un sistema básico de inferencia difusa.
    Utiliza funciones de pertenencia y reglas difusas para hacer inferencias y tomar decisiones.
    """

    def __init__(self, universo):
        """
        Inicializa el sistema de inferencia difusa.
        
        :param universo: Un arreglo de valores que define el universo de discurso (entrada).
        """
        self.universo = universo  # Universo de valores posibles (valores de entrada)

    def funcion_pertenencia(self, x, tipo='triangular', params=(0, 0, 0)):
        """
        Calcula el grado de pertenencia de un valor x dado a un conjunto difuso específico.
        
        :param x: El valor a evaluar en la función de pertenencia.
        :param tipo: El tipo de función de pertenencia ('triangular', 'trapezoidal', 'sigmoide').
        :param params: Parámetros específicos para la función de pertenencia.
        :return: El grado de pertenencia del valor x.
        """
        if tipo == 'triangular':
            # Función de pertenencia triangular: p(x) = max(0, min(1, (x-a)/(b-a), (c-x)/(c-b)))
            a, b, c = params
            return max(0, min(1, (x - a) / (b - a), (c - x) / (c - b)))

        elif tipo == 'trapezoidal':
            # Función de pertenencia trapezoidal: p(x) = max(0, min(1, (x-a)/(b-a), 1, (d-x)/(d-c)))
            a, b, c, d = params
            return max(0, min(1, (x - a) / (b - a), 1, (d - x) / (d - c)))

        elif tipo == 'sigmoide':
            # Función de pertenencia sigmoide: p(x) = 1 / (1 + exp(-(x - c) / b))
            c, b = params
            return 1 / (1 + np.exp(-(x - c) / b))
        
        return 0  # Si el tipo no es reconocido, devolver 0

    def regla_inferencia(self, valor_entrada, funcion_entrada, funcion_salida, params_entrada, params_salida):
        """
        Evalúa una regla difusa de inferencia.
        
        :param valor_entrada: El valor de entrada para la evaluación.
        :param funcion_entrada: La función de pertenencia para la entrada.
        :param funcion_salida: La función de pertenencia para la salida.
        :param params_entrada: Parámetros de la función de pertenencia de la entrada.
        :param params_salida: Parámetros de la función de pertenencia de la salida.
        :return: El valor difuso de salida.
        """
        # Evaluamos el grado de pertenencia de la entrada usando la función de pertenencia de la entrada
        pertenencia_entrada = self.funcion_pertenencia(valor_entrada, tipo=funcion_entrada, params=params_entrada)
        
        # Para simplificar, asumimos una salida lineal proporcional al grado de pertenencia de la entrada
        pertenencia_salida = pertenencia_entrada  # En este caso, para cada regla de ejemplo, la pertenencia es la misma
        
        # Calculamos el valor de salida difusa
        salida = pertenencia_salida * self.funcion_pertenencia(valor_entrada, tipo=funcion_salida, params=params_salida)
        
        return salida

    def solucion_ajustada(self, salida_difusa):
        """
        Ajusta el valor final de la salida difusa, utilizando la defuzzificación.
        
        :param salida_difusa: Los valores de salida difusa para defuzzificación.
        :return: El valor crisp (no difuso) calculado.
        """
        # Defuzzificación: Usaremos el método de centro de gravedad (Centroide)
        suma_numerador = sum(salida_difusa * self.universo)
        suma_denominador = sum(salida_difusa)
        
        # Calculamos el valor crisp
        return suma_numerador / suma_denominador if suma_denominador != 0 else 0


# Ejemplo de uso de Inferencia Difusa

# Definir el universo de discurso para la entrada (temperatura)
universo = np.linspace(0, 40, 100)  # Temperaturas de 0 a 40 grados Celsius

# Creamos un sistema de inferencia difusa
sistema = SistemaInferenciaDifusa(universo)

# Definir las funciones de pertenencia para las entradas
# Entrada: Baja temperatura, media temperatura, alta temperatura
params_baja = (0, 0, 20)  # Función triangular para baja temperatura
params_media = (10, 20, 30)  # Función triangular para temperatura media
params_alta = (25, 40, 40)  # Función triangular para alta temperatura

# Definir las funciones de pertenencia para las salidas
# Salida: Baja velocidad, media velocidad, alta velocidad
params_baja_salida = (0, 0, 10)
params_media_salida = (5, 15, 25)
params_alta_salida = (15, 35, 35)

# Evaluamos las reglas de inferencia
salidas = []
for temperatura in universo:
    # Aplicamos las reglas de inferencia para la temperatura
    salida_baja = sistema.regla_inferencia(temperatura, 'triangular', 'triangular', params_baja, params_baja_salida)
    salida_media = sistema.regla_inferencia(temperatura, 'triangular', 'triangular', params_media, params_media_salida)
    salida_alta = sistema.regla_inferencia(temperatura, 'triangular', 'triangular', params_alta, params_alta_salida)

    # Combinamos las salidas difusas
    salidas.append(salida_baja + salida_media + salida_alta)

# Calculamos la salida crisp a través de la defuzzificación
salida_crisp = sistema.solucion_ajustada(salidas)

# Mostramos el valor de salida final
print(f"Temperatura ajustada (valor crisp) para el control: {salida_crisp:.2f} (km/h)")

# Visualizamos las funciones de pertenencia para las entradas
plt.plot(universo, [sistema.funcion_pertenencia(x, 'triangular', params_baja) for x in universo], label='Baja Temperatura')
plt.plot(universo, [sistema.funcion_pertenencia(x, 'triangular', params_media) for x in universo], label='Temperatura Media')
plt.plot(universo, [sistema.funcion_pertenencia(x, 'triangular', params_alta) for x in universo], label='Alta Temperatura')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Grado de Pertenencia')
plt.title('Funciones de Pertenencia de Temperatura')
plt.legend()
plt.grid(True)
plt.show()
