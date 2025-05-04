# Importamos pandas para manejar datos tabulares
import pandas as pd  

# Importamos numpy para operaciones numéricas
import numpy as np  

# Definimos nuestros ejemplos como un DataFrame usando pandas
# Estos son ejemplos positivos y negativos para inducir reglas
data = pd.DataFrame({
    'edad': [25, 32, 47, 51, 29, 60, 18, 35],  # Edad de cada persona
    'condicion_fisica': ['buena', 'buena', 'mala', 'mala', 'buena', 'mala', 'buena', 'buena'],  # Estado físico
    'es_apto': ['si', 'si', 'no', 'no', 'si', 'no', 'si', 'si']  # Etiqueta si es apto o no
})

# Función que implementa un FOIL muy simplificado
def foil_algorithm(data):
    # Creamos una lista vacía para guardar las reglas encontradas
    reglas = []

    # Seleccionamos solo las filas donde la etiqueta es 'si' (positivos)
    positivos = data[data['es_apto'] == 'si']

    # Seleccionamos las filas donde la etiqueta es 'no' (negativos)
    negativos = data[data['es_apto'] == 'no']

    # Reglas candidatas para el atributo 'edad'
    if positivos['edad'].min() >= 18 and negativos['edad'].max() < 60:
        # Si los positivos son mayores de 18 y los negativos menores de 60, agregamos una regla
        reglas.append("edad >= 18")

    # Reglas candidatas para la 'condicion_fisica'
    if 'buena' in positivos['condicion_fisica'].values and 'buena' not in negativos['condicion_fisica'].values:
        # Si sólo los positivos tienen 'buena' condición, agregamos esta regla
        reglas.append("condicion_fisica == 'buena'")

    # Retornamos las reglas inducidas
    return reglas

# Llamamos a la función FOIL y guardamos las reglas
reglas_descubiertas = foil_algorithm(data)

# Imprimimos las reglas encontradas por nuestro FOIL simplificado
print("Reglas inducidas para determinar si alguien es apto:")
for regla in reglas_descubiertas:
    # Mostramos cada regla
    print(f"- Si {regla}, entonces es apto")

# Ahora creamos una función que aplica las reglas inducidas a un nuevo ejemplo
def predecir_apto(edad, condicion_fisica):
    # Aplicamos cada regla con condiciones lógicas
    if edad >= 18 and condicion_fisica == 'buena':
        # Si cumple todas las reglas, decimos que es apto
        return "si"
    else:
        # Si no cumple, decimos que no es apto
        return "no"

# Probamos nuestro sistema con un nuevo ejemplo
# Definimos una nueva persona de 40 años y buena condición física
nuevo_ejemplo = {'edad': 40, 'condicion_fisica': 'buena'}

# Llamamos a la función para predecir si es apto
resultado = predecir_apto(nuevo_ejemplo['edad'], nuevo_ejemplo['condicion_fisica'])

# Imprimimos el resultado de la predicción
print(f"\n¿La nueva persona es apta? {resultado}")
