import itertools
import random

# 🧠 Lista de puertas en el laboratorio
puertas = ["P1", "P2", "P3", "P4", "P5", "P6"]

# 🔑 Cada puerta acepta códigos del 1 al 5
dominio = [1, 2, 3, 4, 5]

# ⚠️ Algunas combinaciones activan la alarma (no se pueden usar juntas)
# Esto simula una tabla de conflictos
conflictos = {
    ("P1", 3, "P2", 2),
    ("P3", 4, "P4", 4),
    ("P5", 1, "P6", 1),
    ("P1", 5, "P6", 2),
    ("P2", 1, "P4", 1),
}

# 🪓 Elegimos las puertas más conectadas como "cutset"
cutset = ["P1", "P3"]  # Puedes probar con otros valores

# 🔍 El resto se resolverá con búsqueda tras acondicionar el corte
resto_puertas = [p for p in puertas if p not in cutset]

# ✅ Valida una combinación completa
def combinacion_valida(asignacion):
    for (p1, v1, p2, v2) in conflictos:
        if p1 in asignacion and p2 in asignacion:
            if asignacion[p1] == v1 and asignacion[p2] == v2:
                return False
    return True

# 🧮 Búsqueda simple (backtracking) en el resto
def resolver_restantes(asignacion_parcial):
    if len(asignacion_parcial) == len(puertas):
        return asignacion_parcial if combinacion_valida(asignacion_parcial) else None

    siguiente = [p for p in puertas if p not in asignacion_parcial][0]

    for valor in dominio:
        asignacion_parcial[siguiente] = valor
        if combinacion_valida(asignacion_parcial):
            resultado = resolver_restantes(asignacion_parcial.copy())
            if resultado:
                return resultado
        del asignacion_parcial[siguiente]

    return None

# 🎰 Probamos todas las combinaciones posibles del cutset
for valores in itertools.product(dominio, repeat=len(cutset)):
    asignacion = {cutset[i]: valores[i] for i in range(len(cutset))}
    if combinacion_valida(asignacion):
        resultado = resolver_restantes(asignacion.copy())
        if resultado:
            print("\n🗝️ ¡Puertas desbloqueadas con éxito!")
            for puerta in puertas:
                print(f"🚪 {puerta} ➡️ Código {resultado[puerta]}")
            break
else:
    print("❌ No se pudo encontrar una combinación válida. Quedaste atrapado 💀")
