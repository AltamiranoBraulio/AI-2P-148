import numpy as np  # Importamos numpy para operaciones numéricas eficientes
import pandas as pd  # Importamos pandas para manipular datos en forma de tablas
from sklearn.linear_model import LinearRegression  # Importamos regresión lineal de sklearn

# Clase que representa un nodo en el árbol M5
class M5Node:
    def __init__(self, depth=0):
        self.depth = depth  # Profundidad del nodo dentro del árbol
        self.split_feature = None  # Nombre de la característica usada para dividir
        self.split_value = None  # Valor numérico donde hacemos la división
        self.left = None  # Subárbol izquierdo (para valores menores)
        self.right = None  # Subárbol derecho (para valores mayores)
        self.model = None  # Regresión lineal almacenada si es hoja

# Clase que representa el Árbol de Regresión M5 completo
class M5Tree:
    def __init__(self, min_samples_leaf=5, max_depth=5):
        self.min_samples_leaf = min_samples_leaf  # Mínimo de datos requeridos en una hoja
        self.max_depth = max_depth  # Profundidad máxima permitida del árbol
        self.root = None  # Nodo raíz del árbol

    # Método público para entrenar el árbol
    def fit(self, X, y):
        data = X.copy()  # Copiamos las características
        data['target'] = y  # Agregamos la columna objetivo
        self.root = self._build_tree(data, depth=0)  # Llamamos método privado para construir

    # Método recursivo que construye el árbol M5
    def _build_tree(self, data, depth):
        node = M5Node(depth=depth)  # Creamos un nodo con la profundidad actual

        # Condición para detener el crecimiento y hacer hoja
        if len(data) <= self.min_samples_leaf or depth >= self.max_depth:
            node.model = LinearRegression()  # Creamos modelo lineal
            X_train = data.drop(columns='target')  # Entradas sin columna target
            y_train = data['target']  # Columna target
            node.model.fit(X_train, y_train)  # Ajustamos la regresión
            return node  # Retornamos nodo hoja

        best_feature = None  # Inicializamos la mejor característica
        best_value = None  # Inicializamos el mejor valor para división
        best_score = float('inf')  # Mejor puntuación (MSE más bajo)

        # Probamos cada característica para hacer la mejor división
        for feature in data.columns.drop('target'):
            for value in data[feature].unique():  # Probamos cada valor único
                left = data[data[feature] <= value]  # Datos menores o iguales
                right = data[data[feature] > value]  # Datos mayores

                # Aseguramos que las divisiones sean válidas
                if len(left) < self.min_samples_leaf or len(right) < self.min_samples_leaf:
                    continue

                # Calculamos MSE para izquierda y derecha
                mse_left = np.var(left['target']) * len(left)
                mse_right = np.var(right['target']) * len(right)
                mse_total = mse_left + mse_right  # Suma total de errores

                # Si encontramos mejor partición, la guardamos
                if mse_total < best_score:
                    best_feature = feature
                    best_value = value
                    best_score = mse_total

        # Si no encontramos una buena división, hacemos hoja con regresión
        if best_feature is None:
            node.model = LinearRegression()
            X_train = data.drop(columns='target')
            y_train = data['target']
            node.model.fit(X_train, y_train)
            return node

        # Guardamos la mejor división encontrada en el nodo
        node.split_feature = best_feature
        node.split_value = best_value

        # Creamos ramas izquierda y derecha recursivamente
        left_data = data[data[best_feature] <= best_value]
        right_data = data[data[best_feature] > best_value]

        node.left = self._build_tree(left_data, depth + 1)  # Construimos rama izquierda
        node.right = self._build_tree(right_data, depth + 1)  # Construimos rama derecha

        return node  # Retornamos nodo creado

    # Método público para predecir con nuevos datos
    def predict(self, X):
        return np.array([self._predict_row(row, self.root) for _, row in X.iterrows()])

    # Método recursivo para predecir fila por fila
    def _predict_row(self, row, node):
        # Si estamos en nodo hoja, usamos regresión para predecir
        if node.model is not None:
            return node.model.predict([row.values])[0]

        # Si valor es menor o igual al split, vamos a izquierda
        if row[node.split_feature] <= node.split_value:
            return self._predict_row(row, node.left)
        else:  # Si no, vamos a derecha
            return self._predict_row(row, node.right)

# ---------------- EJEMPLO PRÁCTICO: Predicción del precio de casas ---------------- #

# Generamos datos sintéticos para casas
np.random.seed(42)  # Fijamos semilla para reproducibilidad
data = pd.DataFrame({
    'tamaño_m2': np.random.randint(50, 200, 100),  # Tamaño de casa en m2
    'habitaciones': np.random.randint(1, 5, 100),  # Número de habitaciones
})

# Generamos precios con algo de ruido
precios = data['tamaño_m2'] * 3000 + data['habitaciones'] * 50000 + np.random.normal(0, 10000, 100)

# Creamos instancia de nuestro árbol M5 personalizado
arbol_m5 = M5Tree(min_samples_leaf=5, max_depth=4)

# Entrenamos el árbol usando nuestros datos
arbol_m5.fit(data, precios)

# Hacemos predicción con nuevas casas
nuevas_casas = pd.DataFrame({
    'tamaño_m2': [60, 150],
    'habitaciones': [2, 4]
})

# Obtenemos predicciones
predicciones = arbol_m5.predict(nuevas_casas)

# Mostramos los resultados
print("Predicciones de precios para nuevas casas:")
print(predicciones)
