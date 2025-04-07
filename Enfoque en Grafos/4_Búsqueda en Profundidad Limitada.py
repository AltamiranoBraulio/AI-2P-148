import time
import random

# Mapa del suelo: 'T'=tierra, 'N'=nutriente, 'P'=piedra, 'R'=raíz
suelo = [
    ['T', 'T', 'T', 'T', 'T'],
    ['T', 'P', 'T', 'N', 'T'],
    ['T', 'T', 'P', 'T', 'T'],
    ['T', 'N', 'T', 'P', 'T'],
    ['T', 'T', 'T', 'T', 'N']
]

# Posición inicial de la raíz (centro)
posicion_inicial = (2, 2)
suelo[posicion_inicial[0]][posicion_inicial[1]] = 'R'

def mostrar_suelo():
    """Muestra el estado actual del suelo de forma visual"""
    print("\nEstado del suelo:")
    for fila in suelo:
        print(" ".join(fila))
    print()
    time.sleep(1)