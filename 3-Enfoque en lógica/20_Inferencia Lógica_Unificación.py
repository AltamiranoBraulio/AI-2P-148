# 🔥 Motor simple de unificación lógica en Python
# Autor: ChatGPT para Braulio 🧠
# Tema: Inferencia Lógica - Unificación

# Esta función verifica si un término es una **variable lógica**
# Regla: si es una cadena y comienza con letra mayúscula, es variable (como X, Y)
def es_variable(x):
    return isinstance(x, str) and x[0].isupper()

# 🔄 Función principal de unificación
# x e y son las expresiones que queremos unificar
# sustituciones es un diccionario que va guardando qué variable se sustituye por qué valor
def unificar(x, y, sustituciones={}):
    # Caso base: si ya hubo un fallo previo
    if sustituciones is None:
        return None
    # Si ambos son idénticos (ejemplo: "juan" y "juan"), ya están unificados
    elif x == y:
        return sustituciones
    # Si x es una variable lógica, tratamos de unificarla con y
    elif es_variable(x):
        return unificar_variable(x, y, sustituciones)
    # Si y es variable lógica, tratamos de unificarla con x
    elif es_variable(y):
        return unificar_variable(y, x, sustituciones)
    # Si ambos son listas (ejemplo: ['padre', 'X', 'juan']), y tienen la misma longitud
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        # Unificamos cada elemento de las listas uno por uno
        for xi, yi in zip(x, y):
            sustitaciones_nuevas = unificar(xi, yi, sustituciones)
            if sustitaciones_nuevas is None:
                return None  # Fallo en unificación
            sustituciones = sustitaciones_nuevas  # Actualizamos sustituciones
        return sustituciones
    else:
        # Si no cae en ninguno de los casos anteriores, no se puede unificar
        return None

# 🔄 Unifica una variable con un término
def unificar_variable(var, x, sustituciones):
    # Si la variable ya tiene una sustitución previa, seguimos unificando
    if var in sustituciones:
        return unificar(sustituciones[var], x, sustituciones)
    # Si x ya tiene sustitución previa, seguimos unificando
    elif x in sustituciones:
        return unificar(var, sustituciones[x], sustituciones)
    # Evitamos bucles infinitos (ejemplo: X = f(X)) usando ocurre_en
    elif ocurre_en(var, x, sustituciones):
        return None  # No se puede unificar (auto-referencia)
    else:
        # Añadimos nueva sustitución var -> x
        sustituciones_nuevo = sustituciones.copy()
        sustituciones_nuevo[var] = x
        return sustituciones_nuevo

# 🔄 Verifica si una variable ocurre dentro de x (para evitar bucles)
def ocurre_en(var, x, sustituciones):
    if var == x:
        return True  # La variable es igual a x
    elif es_variable(x) and x in sustituciones:
        # Buscamos recursivamente en la sustitución de x
        return ocurre_en(var, sustituciones[x], sustituciones)
    elif isinstance(x, list):
        # Revisamos cada elemento de la lista
        return any(ocurre_en(var, xi, sustituciones) for xi in x)
    else:
        return False  # No ocurre

# 🌟 Ejemplo práctico: inferir relaciones familiares y de amistad
def prueba():
    print("🔎 Ejemplo 1: padre(X, juan) y padre(carlos, Y)")
    # Intentamos unificar padre(X, juan) con padre(carlos, Y)
    resultado = unificar(['padre', 'X', 'juan'], ['padre', 'carlos', 'Y'])
    print("➡️ Resultado:", resultado)

    print("\n🔎 Ejemplo 2: amigo(X, Y) y amigo(mario, pedro)")
    # Intentamos unificar amigo(X, Y) con amigo(mario, pedro)
    resultado = unificar(['amigo', 'X', 'Y'], ['amigo', 'mario', 'pedro'])
    print("➡️ Resultado:", resultado)

    print("\n🔎 Ejemplo 3: hermano(X, X) y hermano(juan, pedro)")
    # Intentamos unificar hermano(X, X) con hermano(juan, pedro)
    resultado = unificar(['hermano', 'X', 'X'], ['hermano', 'juan', 'pedro'])
    print("➡️ Resultado:", resultado or "❌ No se puede unificar (X tendría que ser juan y pedro a la vez)")

# 🚀 Ejecutamos la función de prueba
prueba()
