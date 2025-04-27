import random

# Probabilidades diarias de subida, bajada o estabilidad
# NOTA: ¡no suman 1!, hay incertidumbre
probabilidad_subida = 0.4
probabilidad_bajada = 0.4
probabilidad_estable = 0.1

# Precio inicial de la criptomoneda
precio_actual = 100.0

# Tu capital
dinero = 1000.0
criptos = 0.0

# Número de días a simular
dias = 30

# Función para decidir qué hacer cada día
def decidir():
    decision = random.choice(["comprar", "vender", "esperar"])
    return decision

# Función para simular el movimiento del mercado
def movimiento_mercado(precio):
    r = random.random()
    if r < probabilidad_subida:
        cambio = random.uniform(1.01, 1.10)  # Sube entre 1% y 10%
        return precio * cambio
    elif r < probabilidad_subida + probabilidad_bajada:
        cambio = random.uniform(0.90, 0.99)  # Baja entre 1% y 10%
        return precio * cambio
    else:
        return precio  # Se mantiene

# Simulación día a día
for dia in range(1, dias + 1):
    print(f"\n📅 Día {dia}")
    print(f"Precio actual de la cripto: ${precio_actual:.2f}")
    decision = decidir()
    
    if decision == "comprar" and dinero >= precio_actual:
        # Compra la máxima cantidad posible
        cantidad_comprada = dinero // precio_actual
        criptos += cantidad_comprada
        dinero -= cantidad_comprada * precio_actual
        print(f"💰 Compraste {cantidad_comprada:.2f} criptos")
    elif decision == "vender" and criptos > 0:
        # Vende todo lo que tienes
        dinero += criptos * precio_actual
        print(f"🤑 Vendiste {criptos:.2f} criptos")
        criptos = 0
    else:
        print(f"🤔 Decidiste esperar")

    # El mercado se mueve
    precio_actual = movimiento_mercado(precio_actual)

# Al final del período
valor_final = dinero + (criptos * precio_actual)

print("\n📈📉 RESULTADOS FINALES 📈📉")
print(f"Dinero en efectivo: ${dinero:.2f}")
print(f"Criptomonedas en posesión: {criptos:.2f}")
print(f"Valor total final: ${valor_final:.2f}")
