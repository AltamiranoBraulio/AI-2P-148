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
    