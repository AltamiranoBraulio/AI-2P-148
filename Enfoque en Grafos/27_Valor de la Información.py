# Simulamos una decisión: ¿Invertir o no?
# Dos estados posibles: Mercado BUENO o MALO

# Sin información
prob_bueno = 0.6
prob_malo = 0.4

utilidad_invertir_bueno = 100
utilidad_invertir_malo = -50
utilidad_no_invertir = 0

# Utilidad esperada sin información (decisión racional)
UE_invertir = prob_bueno * utilidad_invertir_bueno + prob_malo * utilidad_invertir_malo
UE_no_invertir = utilidad_no_invertir

mejor_decision = "Invertir" if UE_invertir > UE_no_invertir else "No invertir"
UE_actual = max(UE_invertir, UE_no_invertir)

print("=== SIN INFORMACIÓN PERFECTA ===")
print(f"Utilidad esperada si se invierte: {UE_invertir}")
print(f"Utilidad esperada si no se invierte: {UE_no_invertir}")
print(f"Mejor decisión: {mejor_decision}")
print(f"Utilidad esperada actual: {UE_actual}\n")

# Con información perfecta (sabemos si el mercado será bueno o malo)
# Tomamos la mejor decisión en cada caso

UE_info_perfecta = prob_bueno * max(utilidad_invertir_bueno, utilidad_no_invertir) + \
                   prob_malo * max(utilidad_invertir_malo, utilidad_no_invertir)

valor_informacion = UE_info_perfecta - UE_actual

print("=== CON INFORMACIÓN PERFECTA ===")
print(f"Utilidad esperada con información perfecta: {UE_info_perfecta}")
print(f"Valor de la Información Perfecta (VOI): {valor_informacion}")
