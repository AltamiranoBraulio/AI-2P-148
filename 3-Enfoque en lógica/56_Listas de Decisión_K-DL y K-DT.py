import numpy as np  # Importamos numpy para manejo de datos numéricos
import pandas as pd  # Importamos pandas para manejo de datos en tablas
from sklearn.datasets import load_iris  # Cargamos dataset Iris como ejemplo

# ---------------------------- K-DL: K-Decision List ---------------------------- #

# Clase que implementa una lista de decisión simple (K-DL)
class KDecisionList:
    def __init__(self, k=1):  # Inicializamos con parámetro k
        self.k = k  # Número de condiciones en cada regla
        self.rules = []  # Lista donde guardaremos las reglas (condición, clase)

    # Método para entrenar la lista de decisión
    def fit(self, X, y):
        data = X.copy()  # Copiamos las características
        data['target'] = y  # Agregamos columna target

        remaining = data.copy()  # Creamos copia de datos que aún no se han cubierto

        # Mientras queden ejemplos sin clasificar
        while not remaining.empty:
            best_rule = None  # Inicializamos mejor regla
            best_score = -1  # Inicializamos mejor puntuación

            # Probamos cada característica
            for feature in X.columns:
                for value in remaining[feature].unique():  # Probamos cada valor único

                    # Seleccionamos ejemplos donde se cumple la condición
                    covered = remaining[remaining[feature] == value]

                    # Si no cubre nada, saltamos
                    if covered.empty:
                        continue

                    # Vemos cuál es la clase mayoritaria
                    majority_class = covered['target'].mode()[0]

                    # Contamos cuántos ejemplos son correctamente clasificados
                    correct = (covered['target'] == majority_class).sum()

                    # Si esta regla es mejor, la guardamos
                    if correct > best_score:
                        best_score = correct
                        best_rule = (feature, value, majority_class)

            # Si encontramos una regla, la agregamos
            if best_rule:
                self.rules.append(best_rule)  # Guardamos la regla en la lista

                # Eliminamos ejemplos ya cubiertos por esta regla
                feature, value, _ = best_rule
                remaining = remaining[remaining[feature] != value]
            else:
                break  # Si no se puede mejorar, terminamos

    # Método para predecir clases
    def predict(self, X):
        predictions = []  # Lista para guardar predicciones
        for _, row in X.iterrows():  # Iteramos sobre cada fila
            predicted = None  # Inicializamos predicción
            # Revisamos cada regla
            for feature, value, label in self.rules:
                if row[feature] == value:  # Si se cumple condición
                    predicted = label  # Usamos clase de la regla
                    break  # Rompemos el ciclo
            if predicted is None:
                predicted = self.rules[-1][2]  # Si no coincide, usamos última regla
            predictions.append(predicted)  # Guardamos predicción
        return predictions  # Retornamos todas las predicciones


# ---------------------------- K-DT: K-Decision Tree ---------------------------- #

# Clase que implementa un árbol de decisión basado en listas (K-DT)
class KDecisionTree:
    def __init__(self, max_depth=3):  # Inicializamos con profundidad máxima
        self.max_depth = max_depth  # Guardamos la profundidad
        self.tree = {}  # Diccionario donde guardaremos el árbol

    # Método para entrenar el árbol
    def fit(self, X, y, depth=0, node='root'):
        data = X.copy()  # Copiamos datos
        data['target'] = y  # Agregamos columna target

        # Si todos los ejemplos son de la misma clase
        if len(data['target'].unique()) == 1 or depth == self.max_depth:
            self.tree[node] = ('leaf', data['target'].mode()[0])  # Guardamos clase
            return

        best_feature = None
        best_score = -1

        # Buscamos la mejor característica para dividir
        for feature in X.columns:
            score = data[feature].nunique()  # Número de valores únicos
            if score > best_score:
                best_score = score
                best_feature = feature

        self.tree[node] = ('split', best_feature)  # Guardamos división

        # Dividimos por cada valor posible
        for value in data[best_feature].unique():
            subset = data[data[best_feature] == value]  # Subconjunto que cumple condición
            child_node = f"{node}_{best_feature}_{value}"  # Nombre del nodo hijo

            # Si subset está vacío, hacemos hoja con clase mayoritaria
            if subset.empty:
                self.tree[child_node] = ('leaf', data['target'].mode()[0])
            else:
                # Entrenamos recursivamente en el hijo
                self.fit(subset.drop(columns='target'), subset['target'], depth + 1, child_node)

    # Método para predecir clase
    def predict_row(self, row, node='root'):
        node_type, value = self.tree[node]  # Obtenemos tipo de nodo y valor
        if node_type == 'leaf':
            return value  # Si es hoja, retornamos clase
        else:
            feature = value  # Si es split, usamos la característica
            child_node = f"{node}_{feature}_{row[feature]}"  # Buscamos el hijo correspondiente
            if child_node in self.tree:
                return self.predict_row(row, child_node)  # Repetimos recursivamente
            else:
                return self.tree[node][1]  # Si no hay hijo, usamos clase actual

    # Método para predecir varias filas
    def predict(self, X):
        return [self.predict_row(row) for _, row in X.iterrows()]  # Retornamos lista de predicciones


# ------------------------- Ejemplo con Dataset Iris ---------------------------- #

# Cargamos dataset Iris
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)  # Creamos DataFrame con características
y = pd.Series(iris.target)  # Creamos Serie con las etiquetas

# Discretizamos las características para usarlas en listas de decisión
X_discrete = X.apply(lambda col: pd.cut(col, bins=3, labels=[0, 1, 2]))

# --------------------- Entrenamiento y prueba de K-DL --------------------- #
kdl = KDecisionList()
kdl.fit(X_discrete, y)  # Entrenamos la lista de decisión
predicciones_kdl = kdl.predict(X_discrete)  # Hacemos predicciones
print("Predicciones usando K-DL:", predicciones_kdl[:5])  # Mostramos 5 predicciones

# --------------------- Entrenamiento y prueba de K-DT --------------------- #
kdt = KDecisionTree(max_depth=3)
kdt.fit(X_discrete, y)  # Entrenamos el árbol de decisión
predicciones_kdt = kdt.predict(X_discrete)  # Hacemos predicciones
print("Predicciones usando K-DT:", predicciones_kdt[:5])  # Mostramos 5 predicciones
