from collections import deque
import random
import time

cyber_red={
     "Terminal_Hacker": ["Nodo_A", "Nodo_B"],
    "Nodo_A": ["Nodo_C", "Nodo_D"],
    "Nodo_B": ["Nodo_E"],
    "Nodo_C": ["Nodo_F"],
    "Nodo_D": [],
    "Nodo_E": ["Nodo_G", "Nodo_H"],
    "Nodo_F": [],
    "Nodo_G": ["IA_Central"],
    "Nodo_H": [],
    "IA_Central": []
}

def efecto_hackeo(texto):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(0.02)

    print()  # Salto de línea al final


def busqueda_bidireccional_cyberpunk(inicio, objetivo):
    if inicio == objetivo:
        return [inicio]
    
    # 🧠 Dos frentes: uno desde el hacker y otro desde la IA
    frente_hacker = deque([inicio])
    frente_IA = deque([objetivo])

    rastreo_hacker = {inicio: None}
    rastreo_IA = {objetivo: None}


    while frente_hacker and frente_IA:
        # ▶️ Expansión del Hacker
        nodo = frente_hacker.popleft()
        efecto_hackeo(f"💻 Hacker accediendo: {nodo}")
        for vecino in cyber_red.get(nodo, []):
            if vecino not in rastreo_hacker:
                rastreo_hacker[vecino] = nodo
                frente_hacker.append(vecino)
                if vecino in rastreo_IA:
                    return reconstruir_camino_cyberpunk(rastreo_hacker, rastreo_IA, vecino)

  # ▶️ Expansión de la IA
        nodo = frente_IA.popleft()
        efecto_hackeo(f"🤖 IA rastreando desde: {nodo}")
        for clave, vecinos in cyber_red.items():
            if nodo in vecinos:  # Conexiones inversas
                if clave not in rastreo_IA:
                    rastreo_IA[clave] = nodo
                    frente_IA.append(clave)
                    if clave in rastreo_hacker:
                        return reconstruir_camino_cyberpunk(rastreo_hacker, rastreo_IA, clave)
return None

# 🔁 Reconstrucción del camino final
def reconstruir_camino_cyberpunk(r_hacker, r_IA, punto):
    camino = []

    # Camino desde el hacker hasta el punto de encuentro
    nodo = punto
    while nodo is not None:
        camino.append(nodo)
        nodo = r_hacker[nodo]
    camino.reverse()


      # Camino desde el punto de encuentro hasta la IA
    nodo = r_IA[punto]
    while nodo is not None:
        camino.append(nodo)
        nodo = r_IA[nodo]

    return camino

# 🚀 Ejecución principal
camino = busqueda_bidireccional_cyberpunk("Terminal_Hacker", "IA_Central")

# 🧾 Mostrar resultado con estilo hacker
if camino:
    efecto_hackeo("\n✅ ¡Conexión establecida entre el Hacker y la IA!")
    efecto_hackeo("🌐 Ruta de conexión: " + " -> ".join(camino))
else:
    efecto_hackeo("\n❌ Conexión fallida. El rastro se ha perdido.")