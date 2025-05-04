# Importamos pandas para manejar datos en tablas
import pandas as pd

# Definimos nuestros ejemplos de entrenamiento (cada fila es una instancia)
# Con atributos simples: Color, Tamaño, Forma
data = pd.DataFrame({
    'Color': ['Rojo', 'Rojo', 'Azul', 'Rojo', 'Azul'],
    'Tamaño': ['Grande', 'Pequeño', 'Grande', 'Grande', 'Pequeño'],
    'Forma': ['Circular', 'Circular', 'Cuadrado', 'Cuadrado', 'Circular'],
    'Clase': ['Sí', 'Sí', 'No', 'Sí', 'No']  # Clase objetivo (Sí o No)
})

# Imprimimos los datos para verlos
print("=== Datos de Entrenamiento ===")
print(data)

# Inicializamos la hipótesis específica S con la primera instancia positiva
# Así: si es Sí, entonces es nuestro punto de partida
S = data[data['Clase'] == 'Sí'].iloc[0, :-1].tolist()

# Inicializamos la hipótesis general G como todo '?', significa cualquier valor
G = [['?' for _ in range(len(S))]]

# Función para verificar si un ejemplo es consistente con una hipótesis
def consistente(h, x):
    # Comprobamos cada atributo
    for i in range(len(h)):
        if h[i] != '?' and h[i] != x[i]:
            return False  # Si no coincide, no es consistente
    return True  # Si todos coinciden, sí es consistente

# Ahora vamos a recorrer cada instancia para actualizar S y G
for index, row in data.iterrows():
    # Obtenemos los atributos (sin la clase)
    x = row[:-1].tolist()
    # Obtenemos la clase (Sí o No)
    y = row[-1]
    
    # Si es un ejemplo positivo (Sí)
    if y == 'Sí':
        for i in range(len(S)):
            # Si S no coincide con el ejemplo, lo generalizamos usando '?'
            if S[i] != x[i]:
                S[i] = '?'
        # Filtramos G: solo mantenemos hipótesis que sean consistentes con x
        G = [g for g in G if consistente(g, x)]
    
    # Si es un ejemplo negativo (No)
    else:
        # Necesitamos especializar G para excluir este ejemplo negativo
        G_new = []
        for g in G:
            for i in range(len(g)):
                # Solo especializamos si el atributo es '?'
                if g[i] == '?':
                    if S[i] != '?':
                        # Creamos una hipótesis nueva donde el atributo es S[i]
                        h = g.copy()
                        h[i] = S[i]
                        # Si la nueva hipótesis es consistente con S, la agregamos
                        if consistente(h, x) == False:
                            G_new.append(h)
        G = G_new  # Actualizamos G con las nuevas especializaciones

# Mostramos la hipótesis más específica (S) y las generales (G)
print("\n=== Hipótesis Específica (S) ===")
print(S)

print("\n=== Hipótesis General (G) ===")
for g in G:
    print(g)

# Simulación simple del Algoritmo AQ: genera reglas para la clase "Sí"
# Extraemos solo ejemplos positivos
positivos = data[data['Clase'] == 'Sí']

# Creamos una lista para almacenar las reglas
reglas_aq = []

# Por cada positivo, creamos una regla específica
for index, row in positivos.iterrows():
    # Tomamos atributos excepto la clase
    condiciones = []
    for col in data.columns[:-1]:
        condiciones.append(f"{col} = {row[col]}")
    # Unimos las condiciones con "Y"
    regla = " SI " + " Y ".join(condiciones) + " => Clase = Sí"
    reglas_aq.append(regla)

# Mostramos las reglas generadas por AQ
print("\n=== Reglas Generadas por AQ ===")
for r in reglas_aq:
    print(r)
