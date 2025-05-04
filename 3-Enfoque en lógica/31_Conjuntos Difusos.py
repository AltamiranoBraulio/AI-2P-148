import numpy as np
import matplotlib.pyplot as plt

class ConjuntoDifuso:
    """
    Esta clase representa un conjunto difuso. Los conjuntos difusos son aquellos
    en los cuales los elementos tienen un grado de pertenencia en el rango [0, 1].
    """

    def __init__(self, universo, func_pertenencia):
        """
        Inicializa el conjunto difuso.
        
        :param universo: Un arreglo de valores que define el universo de discurso.
        :param func_pertenencia: Una función que asigna un valor de pertenencia a cada elemento del universo.
        """
        self.universo = universo  # Universo de elementos posibles (valores de entrada)
        self.func_pertenencia = func_pertenencia  # Función de pertenencia

    def pertenencia(self, x):
        """
        Devuelve el grado de pertenencia de un elemento x al conjunto difuso.

        :param x: El elemento cuyo grado de pertenencia queremos conocer.
        :return: El grado de pertenencia de x al conjunto difuso.
        """
        return self.func_pertenencia(x)

    def mostrar(self):
        """
        Muestra la representación gráfica del conjunto difuso.
        """
        pertenencias = [self.pertenencia(x) for x in self.universo]
        plt.plot(self.universo, pertenencias, label='Conjunto Difuso')
        plt.xlabel('Elemento')
        plt.ylabel('Grado de Pertenencia')
        plt.title('Conjunto Difuso')
        plt.legend()
        plt.grid(True)
        plt.show()

    def interseccion(self, otro_conjunto):
        """
        Calcula la intersección de dos conjuntos difusos, el grado de pertenencia
        de la intersección es el mínimo entre los grados de pertenencia de cada conjunto.

        :param otro_conjunto: El segundo conjunto difuso con el que se va a hacer la intersección.
        :return: Un nuevo conjunto difuso que es la intersección de los dos conjuntos.
        """
        def nueva_func_pertenencia(x):
            return min(self.pertenencia(x), otro_conjunto.pertenencia(x))

        return ConjuntoDifuso(self.universo, nueva_func_pertenencia)

    def union(self, otro_conjunto):
        """
        Calcula la unión de dos conjuntos difusos, el grado de pertenencia
        de la unión es el máximo entre los grados de pertenencia de cada conjunto.

        :param otro_conjunto: El segundo conjunto difuso con el que se va a hacer la unión.
        :return: Un nuevo conjunto difuso que es la unión de los dos conjuntos.
        """
        def nueva_func_pertenencia(x):
            return max(self.pertenencia(x), otro_conjunto.pertenencia(x))

        return ConjuntoDifuso(self.universo, nueva_func_pertenencia)

    def complemento(self):
        """
        Calcula el complemento del conjunto difuso. El grado de pertenencia de un elemento
        en el complemento es 1 menos el grado de pertenencia al conjunto original.

        :return: Un nuevo conjunto difuso que es el complemento del conjunto original.
        """
        def nueva_func_pertenencia(x):
            return 1 - self.pertenencia(x)

        return ConjuntoDifuso(self.universo, nueva_func_pertenencia)

# Ejemplo de uso

# Definimos el universo de discurso, que son los valores entre 0 y 10
universo = np.linspace(0, 10, 100)

# Definimos la función de pertenencia de un conjunto difuso "Temperatura Alta"
def func_temperatura_alta(x):
    # La función de pertenencia es una función sigmoide (función de S)
    return 1 / (1 + np.exp(-(x - 30) / 5))

# Creamos el conjunto difuso "Temperatura Alta"
conjunto_temperatura_alta = ConjuntoDifuso(universo, func_temperatura_alta)

# Mostramos el gráfico del conjunto "Temperatura Alta"
conjunto_temperatura_alta.mostrar()

# Definimos la función de pertenencia para otro conjunto difuso "Temperatura Baja"
def func_temperatura_baja(x):
    # Función de pertenencia para temperatura baja, forma inversa de la alta
    return 1 / (1 + np.exp((x - 30) / 5))

# Creamos el conjunto difuso "Temperatura Baja"
conjunto_temperatura_baja = ConjuntoDifuso(universo, func_temperatura_baja)

# Mostramos el gráfico del conjunto "Temperatura Baja"
conjunto_temperatura_baja.mostrar()

# Calculamos la intersección de los conjuntos "Temperatura Alta" y "Temperatura Baja"
conjunto_interseccion = conjunto_temperatura_alta.interseccion(conjunto_temperatura_baja)

# Mostramos el gráfico de la intersección de los conjuntos
conjunto_interseccion.mostrar()

# Calculamos la unión de los conjuntos "Temperatura Alta" y "Temperatura Baja"
conjunto_union = conjunto_temperatura_alta.union(conjunto_temperatura_baja)

# Mostramos el gráfico de la unión de los conjuntos
conjunto_union.mostrar()

# Calculamos el complemento del conjunto "Temperatura Alta"
conjunto_complemento = conjunto_temperatura_alta.complemento()

# Mostramos el gráfico del complemento del conjunto "Temperatura Alta"
conjunto_complemento.mostrar()
