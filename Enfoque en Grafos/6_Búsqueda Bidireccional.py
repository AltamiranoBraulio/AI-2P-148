# Importamos las librerías necesarias
from collections import deque  # deque es una cola de doble extremo, ideal para BFS o búsqueda bidireccional.
import random  # Para generar valores aleatorios si lo necesitáramos (aunque no lo usamos aquí).
import time  # Para agregar retrasos entre las impresiones en la consola y dar ese efecto de "hackeo".

# Definimos el mapa de la red cibernética, la cual está estructurada como un grafo.
# Cada nodo tiene una lista de nodos conectados a él, representando el ciberespacio.
cyber_red = {
    "Terminal_Hacker": ["Nodo_A", "Nodo_B"],  # El hacker puede empezar desde la Terminal y conectarse a Nodo_A o Nodo_B.
    "Nodo_A": ["Nodo_C", "Nodo_D"],  # Desde Nodo_A, se puede acceder a Nodo_C o Nodo_D.
    "Nodo_B": ["Nodo_E"],  # Desde Nodo_B solo se puede ir a Nodo_E.
    "Nodo_C": ["Nodo_F"],  # Desde Nodo_C, se puede ir solo a Nodo_F.
    "Nodo_D": [],  # Nodo_D no tiene conexión a otros nodos.
    "Nodo_E": ["Nodo_G", "Nodo_H"],  # Nodo_E tiene conexiones a Nodo_G y Nodo_H.
    "Nodo_F": [],  # Nodo_F no tiene conexiones.
    "Nodo_G": ["IA_Central"],  # Nodo_G se conecta a la IA_Central.
    "Nodo_H": [],  # Nodo_H no tiene conexiones.
    "IA_Central": []  # La IA_Central es el nodo objetivo.
}

# Función para simular el efecto de "hackeo" imprimiendo cada letra con un retraso.
# Esto da un efecto visual de que el hacker está escribiendo en tiempo real.
def efecto_hackeo(texto):
    for letra in texto:  # Recorre cada letra de la cadena de texto.
        print(letra, end="", flush=True)  # Imprime la letra sin salto de línea y con el buffer de salida forzado.
        time.sleep(0.02)  # Pausa de 0.02 segundos para darle el efecto de retraso.

    print()  # Salto de línea al final para que el texto siguiente empiece en una nueva línea.

# Función principal que realiza la búsqueda bidireccional entre el hacker y la IA.
def busqueda_bidireccional_cyberpunk(inicio, objetivo):
    if inicio == objetivo:  # Si el punto de inicio es igual al objetivo, se devuelve directamente el camino (solo el nodo).
        return [inicio]
    
    # 🧠 Dos frentes: uno desde el hacker y otro desde la IA
    frente_hacker = deque([inicio])  # Cola de nodos a explorar desde el hacker.
    frente_IA = deque([objetivo])  # Cola de nodos a explorar desde la IA.

    # Diccionarios para llevar el rastro de los nodos explorados por el hacker y la IA.
    rastreo_hacker = {inicio: None}  # Empieza con el nodo de inicio, y no tiene nodo anterior.
    rastreo_IA = {objetivo: None}  # Empieza con el objetivo, y no tiene nodo anterior.

    # Bucle que continúa mientras ambos frentes (hacker e IA) tengan nodos para explorar.
    while frente_hacker and frente_IA:
        
        # ▶️ Expansión del Hacker: Comienza con el hacker y explora sus vecinos.
        nodo = frente_hacker.popleft()  # Extrae el primer nodo de la cola de expansión del hacker.
        efecto_hackeo(f"💻 Hacker accediendo: {nodo}")  # Simula el hackeo visual.
        for vecino in cyber_red.get(nodo, []):  # Recorre los vecinos de este nodo.
            if vecino not in rastreo_hacker:  # Si el vecino aún no ha sido explorado por el hacker.
                rastreo_hacker[vecino] = nodo  # Guardamos el nodo anterior al vecino.
                frente_hacker.append(vecino)  # Añadimos el vecino a la cola del hacker para explorarlo más tarde.
                
                if vecino in rastreo_IA:  # Si el vecino ya ha sido explorado por la IA, ¡hemos encontrado el punto de encuentro!
                    return reconstruir_camino_cyberpunk(rastreo_hacker, rastreo_IA, vecino)  # Reconstruye el camino entre el hacker y la IA.

        # ▶️ Expansión de la IA: Ahora es el turno de la IA para explorar sus vecinos.
        nodo = frente_IA.popleft()  # Extrae el primer nodo de la cola de expansión de la IA.
        efecto_hackeo(f"🤖 IA rastreando desde: {nodo}")  # Simula el rastreo de la IA.
        for clave, vecinos in cyber_red.items():  # Recorre todos los nodos y sus conexiones.
            if nodo in vecinos:  # Si el nodo actual de la IA es vecino de este nodo.
                if clave not in rastreo_IA:  # Si este nodo aún no ha sido explorado por la IA.
                    rastreo_IA[clave] = nodo  # Guardamos el nodo anterior del nodo clave.
                    frente_IA.append(clave)  # Añadimos el nodo clave a la cola de la IA para explorar más tarde.
                    
                    if clave in rastreo_hacker:  # Si este nodo ya ha sido explorado por el hacker, ¡hemos encontrado la ruta!
                        return reconstruir_camino_cyberpunk(rastreo_hacker, rastreo_IA, clave)  # Reconstruye el camino entre el hacker y la IA.
    
    return None  # Si no encontramos la ruta, devolvemos None (sin conexión).

# Función para reconstruir el camino desde el hacker hasta la IA.
def reconstruir_camino_cyberpunk(r_hacker, r_IA, punto):
    camino = []  # Inicializamos una lista para el camino encontrado.

    # Camino desde el hacker hasta el punto de encuentro.
    nodo = punto
    while nodo is not None:  # Mientras haya un nodo válido.
        camino.append(nodo)  # Añadimos el nodo al camino.
        nodo = r_hacker[nodo]  # Retrocedemos al nodo anterior en el rastreo del hacker.
    camino.reverse()  # Invertimos el camino porque lo reconstruimos de atrás hacia adelante.

    # Camino desde el punto de encuentro hasta la IA.
    nodo = r_IA[punto]
    while nodo is not None:  # Mientras haya un nodo válido.
        camino.append(nodo)  # Añadimos el nodo al camino.
        nodo = r_IA[nodo]  # Retrocedemos al nodo anterior en el rastreo de la IA.

    return camino  # Retornamos el camino completo desde el hacker hasta la IA.

# 🚀 Ejecución principal del programa
camino = busqueda_bidireccional_cyberpunk("Terminal_Hacker", "IA_Central")  # Llamamos a la función de búsqueda bidireccional.

# 🧾 Mostrar resultado con estilo hacker.
if camino:  # Si se encontró un camino.
    efecto_hackeo("\n✅ ¡Conexión establecida entre el Hacker y la IA!")  # Imprime un mensaje de éxito.
    efecto_hackeo("🌐 Ruta de conexión: " + " -> ".join(camino))  # Imprime el camino encontrado.
else:  # Si no se encontró ningún camino.
    efecto_hackeo("\n❌ Conexión fallida. El rastro se ha perdido.")  # Imprime un mensaje de error.
