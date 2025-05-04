# 🧠 Lógica de Orden Superior en Python
# Este código demuestra cómo trabajar con lógicas de orden superior
# en un sistema lógico que manipula funciones como objetos y las pasa como argumentos.

# 📚 Definimos una función lógica de orden superior
def combinar_reglas(regla1, regla2, valor):
    """
    Esta función toma dos reglas lógicas y un valor de entrada.
    Aplica ambas reglas sobre el valor de entrada y devuelve el resultado combinado.

    :param regla1: Una función lógica que toma un valor y devuelve un resultado.
    :param regla2: Otra función lógica que toma un valor y devuelve un resultado.
    :param valor: El valor de entrada sobre el cual se aplicarán las reglas.
    :return: El resultado combinado de aplicar ambas reglas al valor de entrada.
    """
    resultado1 = regla1(valor)  # Aplica la primera regla sobre el valor
    resultado2 = regla2(valor)  # Aplica la segunda regla sobre el valor

    # Aquí decidimos cómo combinar los resultados de las dos reglas
    if resultado1 and resultado2:  # Si ambas reglas devuelven verdadero, el resultado es verdadero
        return True
    elif resultado1 or resultado2:  # Si al menos una regla es verdadera, el resultado es verdadero
        return True
    else:
        return False  # Si ninguna regla es verdadera, el resultado es falso

# 🔧 Definimos algunas reglas lógicas simples como funciones
def es_par(x):
    """
    Verifica si un número es par.
    :param x: El número a verificar.
    :return: True si el número es par, False de lo contrario.
    """
    return x % 2 == 0

def es_multiplo_de_tres(x):
    """
    Verifica si un número es múltiplo de tres.
    :param x: El número a verificar.
    :return: True si el número es múltiplo de tres, False de lo contrario.
    """
    return x % 3 == 0

def es_positivo(x):
    """
    Verifica si un número es positivo.
    :param x: El número a verificar.
    :return: True si el número es positivo, False de lo contrario.
    """
    return x > 0

# 🧑‍💻 Ejemplo de cómo aplicar las funciones de orden superior

# Definimos un conjunto de valores a evaluar
valores = [10, 15, -5, 6, 9, 20]

# 🚀 Probamos las reglas de forma independiente
print("Aplicando reglas de forma independiente:")
for valor in valores:
    print(f"Valor: {valor}")
    print(f"Es par: {es_par(valor)}")
    print(f"Es múltiplo de tres: {es_multiplo_de_tres(valor)}")
    print(f"Es positivo: {es_positivo(valor)}")
    print("-" * 30)

# 🚀 Ahora combinamos reglas utilizando la función de orden superior `combinar_reglas`
print("Aplicando combinación de reglas:")
for valor in valores:
    print(f"Valor: {valor}")
    # Combinamos las reglas es_par y es_multiplo_de_tres
    print(f"Es par o múltiplo de tres: {combinar_reglas(es_par, es_multiplo_de_tres, valor)}")
    # Combinamos las reglas es_positivo y es_multiplo_de_tres
    print(f"Es positivo o múltiplo de tres: {combinar_reglas(es_positivo, es_multiplo_de_tres, valor)}")
    print("-" * 30)

# 🧠 Definimos una función de orden superior que devuelve otra función lógica
def generar_regla_compleja():
    """
    Esta función de orden superior devuelve una función que combina reglas de manera compleja.
    La nueva función resultante verifica si un número es par y positivo.

    :return: Una función lógica que combina las reglas de ser par y ser positivo.
    """
    def regla_compleja(x):
        """
        La función que verifica si un número es par y positivo.
        :param x: El número a verificar.
        :return: True si el número es par y positivo, False de lo contrario.
        """
        return es_par(x) and es_positivo(x)  # Verifica si el número es par y positivo
    return regla_compleja  # Retorna la función generada

# 👨‍💻 Utilizamos la regla compleja generada dinámicamente
print("Usando una función generada dinámicamente:")
regla_generada = generar_regla_compleja()  # Obtenemos una nueva regla generada
for valor in valores:
    print(f"Valor: {valor} - ¿Es par y positivo? {regla_generada(valor)}")
    print("-" * 30)
