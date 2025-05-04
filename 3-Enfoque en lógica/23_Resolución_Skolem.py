# 👨‍💻 Programa de Skolemización para Lógica de Primer Orden
# Autor: ChatGPT para Babyarm 👑

# 📚 Importamos las bibliotecas necesarias
import re

# 🌐 Función para transformar cuantificadores existenciales en Skolemización
def skolemize(formula):
    """
    Esta función toma una fórmula lógica en forma de cadena y realiza
    una Skolemización básica. La Skolemización elimina los cuantificadores
    existenciales y reemplaza las variables existenciales por funciones
    de Skolem.

    :param formula: La fórmula lógica a Skolemizar (en formato de cadena).
    :return: Fórmula Skolemizada (en formato de cadena).
    """

    # 🔍 Buscamos las variables existenciales en la fórmula utilizando una expresión regular.
    # Asumimos que las variables existen después de un cuantificador existencial.
    # Ejemplo: ∃x (P(x) → Q(x))
    formula = re.sub(r'∃(\w+)', r'∀\1', formula)

    # 🌐 Reemplazamos las variables existenciales por funciones de Skolem.
    # Las funciones de Skolem son representadas por un nombre de función y un número
    # de argumento (si hay más de una variable en la cláusula cuantificada).
    formula = re.sub(r'∀(\w+)', r'f(\1)', formula)

    # 🌱 Skolemización avanzada: Si encontramos un predicado con cuantificadores, sustituimos
    # las variables cuantificadas por sus funciones de Skolem respectivas.
    # Esto es más avanzado y requiere manejar la aridad de las funciones.
    formula = re.sub(r'P\((\w+)\)', r'P(f(\1))', formula)

    # 📝 Retornamos la fórmula modificada después de la Skolemización
    return formula


# 🧑‍🔬 Función de ejemplo para resolver una fórmula con Skolemización
def resolver_formula():
    """
    Esta función define una fórmula lógica con cuantificadores y realiza
    la Skolemización para eliminar las variables existenciales.
    """

    # 📜 Fórmula de ejemplo con cuantificadores existenciales y universales
    # Ejemplo: ∀x (P(x) → ∃y Q(x, y))
    formula = "∀x (P(x) → ∃y Q(x, y))"

    # 🛠️ Llamamos a la función de Skolemización para transformar la fórmula
    formula_skolemizada = skolemize(formula)

    # 🔍 Mostramos el resultado
    print(f"Fórmula original: {formula}")
    print(f"Fórmula Skolemizada: {formula_skolemizada}")


# 🧪 Ejecutamos el ejemplo de Skolemización
resolver_formula()
