# -------------------------------------------
# 🚀 BÚSQUEDA EN PROFUNDIDAD ITERATIVA (IDDFS)
# 🔍 Simulación de exploración de una mazmorra en busca de un tesoro
# 💻 Autor: Babyarm con ayuda de ChatGPT
# -------------------------------------------

import time  # Importamos la librería time para simular pausas visuales durante la exploración

# -------------------------------------------
# 🌌 DEFINICIÓN DEL GRAFO: LA MAZMORRA
# -------------------------------------------
# Usamos un diccionario para representar un grafo donde cada sala está conectada a otras.
# Las claves del diccionario son los nombres de las salas,
# y los valores son listas con los nombres de las salas vecinas (a donde se puede ir directamente).

mazmorra = {
    "entrada": ["sala1", "sala2"],     # Desde la entrada puedes ir a sala1 o sala2
    "sala1": ["sala3", "sala4"],       # Desde sala1 puedes ir a sala3 o sala4
    "sala2": ["sala5"],                # Desde sala2 puedes ir solo a sala5
    "sala3": [],                       # sala3 no tiene salidas, es un callejón sin salida
    "sala4": ["tesoro"],              # sala4 lleva directamente al tesoro 🎯
    "sala5": [],                       # sala5 también es un callejón sin salida
    "tesoro": []                       # El tesoro es un nodo final sin conexiones
}

# -------------------------------------------
# 🔁 BÚSQUEDA EN PROFUNDIDAD LIMITADA (DFS)
# -------------------------------------------
# Esta función hace una búsqueda en profundidad limitada.
# Recorre los caminos desde un nodo, pero no va más allá del "límite" de profundidad que le indiquemos.
# Si llega al objetivo dentro del límite, devuelve el camino completo que siguió.

def dfs_limitado(nodo, objetivo, limite, camino):
    print(f"🔎 Explorando: {nodo} (límite restante: {limite})")  # Mostramos qué sala estamos explorando
    time.sleep(0.5)  # Pausamos para dar efecto visual y simular una exploración más real

    camino.append(nodo)  # Añadimos esta sala al camino actual

    if nodo == objetivo:  # Si encontramos el tesoro...
        return camino      # ¡Regresamos el camino completo hasta aquí!

    if limite <= 0:  # Si ya no tenemos profundidad para seguir explorando
        camino.pop()  # Quitamos la sala del camino porque no nos llevó al objetivo
        return None   # Y regresamos "None", indicando que este camino no funcionó

    # Exploramos todos los vecinos de la sala actual
    for vecino in mazmorra.get(nodo, []):  # Usamos get para evitar errores si el nodo no existe
        resultado = dfs_limitado(vecino, objetivo, limite - 1, camino)  # Llamamos de nuevo pero bajamos el límite
        if resultado:  # Si encontramos algo (es decir, no es None)...
            return resultado  # Regresamos ese resultado exitoso

    # Si terminamos de revisar todos los caminos desde esta sala sin encontrar el tesoro:
    camino.pop()  # Retrocedemos: quitamos la sala del camino
    return None   # Y avisamos que este camino tampoco funcionó

# -------------------------------------------
# 🔁 BÚSQUEDA EN PROFUNDIDAD ITERATIVA (IDDFS)
# -------------------------------------------
# Esta función es la que hace la magia:
# intenta hacer DFS limitado una y otra vez, cada vez aumentando el límite de profundidad.
# Empieza con profundidad 0 y va aumentando hasta el máximo permitido.

def iddfs(inicio, objetivo, max_profundidad):
    # Vamos a probar profundidades desde 0 hasta max_profundidad
    for profundidad in range(max_profundidad + 1):
        print(f"\n⚙️ Intentando con límite de profundidad: {profundidad}")
        camino = []  # Reiniciamos el camino en cada intento
        resultado = dfs_limitado(inicio, objetivo, profundidad, camino)  # Ejecutamos DFS con el límite actual
        if resultado:  # Si encontramos el tesoro...
            return resultado  # Regresamos el camino exitoso
    return None  # Si llegamos hasta aquí, es porque no lo encontramos 😢

# -------------------------------------------
# 🧪 EJECUCIÓN DEL PROGRAMA
# -------------------------------------------

# Indicamos desde dónde comenzamos y qué queremos encontrar
camino_encontrado = iddfs("entrada", "tesoro", 5)  # Desde 'entrada' buscando 'tesoro' con límite máximo de 5

# -------------------------------------------
# 🧾 MOSTRAR RESULTADO FINAL
# -------------------------------------------
if camino_encontrado:
    print("\n✅ ¡Tesoro encontrado! 🪙🎉")
    print("🛣️ Camino recorrido:", " -> ".join(camino_encontrado))  # Mostramos el camino como una flecha visual
else:
    print("\n❌ No se encontró el tesoro. 😭")
