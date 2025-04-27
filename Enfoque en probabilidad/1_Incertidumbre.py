import random  # Librería para generar números aleatorios

# --- Parámetros de la simulación ---

# Probabilidades de cómo se moverá el mercado cada día:
# OJO: No suman exactamente 1 para simular incertidumbre real
probabilidad_subida = 0.4  # 40% de chances de que el precio suba
probabilidad_bajada = 0.4  # 40% de chances de que el precio baje
probabilidad_estable = 0.1  # 10% de chances de que el precio no cambie

# Precio inicial de la criptomoneda
precio_actual = 100.0  # En dólares

# Capital inicial del inversionista
dinero = 1000.0  # Tienes $1000 para empezar
criptos = 0.0  # Al principio no posees ninguna criptomoneda

# Número total de días que vamos a simular
dias = 30  # Simularemos 30 días de "trading"

# --- Funciones principales ---

# Función para decidir qué acción tomar cada día (comprar, vender o esperar)
def decidir():
    # Se elige aleatoriamente entre "comprar", "vender" o "esperar"
    decision = random.choice(["comprar", "vender", "esperar"])
    return decision

# Función para simular el movimiento del precio en el mercado
def movimiento_mercado(precio):
    r = random.random()  # Número aleatorio entre 0 y 1
    if r < probabilidad_subida:
        # El precio sube: multiplicamos el precio por un factor entre 1.01 y 1.10 (subida entre 1% y 10%)
        cambio = random.uniform(1.01, 1.10)
        return precio * cambio
    elif r < probabilidad_subida + probabilidad_bajada:
        # El precio baja: multiplicamos el precio por un factor entre 0.90 y 0.99 (bajada entre 1% y 10%)
        cambio = random.uniform(0.90, 0.99)
        return precio * cambio
    else:
        # El precio se mantiene igual
        return precio

# --- Comienza la simulación día por día ---

for dia in range(1, dias + 1):
    # Mostramos el día actual
    print(f"\n📅 Día {dia}")
    
    # Mostramos el precio actual de la criptomoneda
    print(f"Precio actual de la cripto: ${precio_actual:.2f}")
    
    # Decidimos qué acción tomar hoy
    decision = decidir()
    
    # --- Ejecutamos la acción elegida ---
    
    if decision == "comprar" and dinero >= precio_actual:
        # Si decidimos comprar y tenemos suficiente dinero
        
        # Calculamos cuántas criptomonedas podemos comprar (sin fracciones, es compra entera)
        cantidad_comprada = dinero // precio_actual
        
        # Aumentamos nuestra cantidad de criptomonedas
        criptos += cantidad_comprada
        
        # Disminuimos nuestro dinero en función de la compra
        dinero -= cantidad_comprada * precio_actual
        
        # Mostramos la acción realizada
        print(f"💰 Compraste {cantidad_comprada:.2f} criptos")
        
    elif decision == "vender" and criptos > 0:
        # Si decidimos vender y tenemos criptomonedas
        
        # Aumentamos nuestro dinero según el precio actual y la cantidad de criptos
        dinero += criptos * precio_actual
        
        # Mostramos la acción realizada
        print(f"🤑 Vendiste {criptos:.2f} criptos")
        
        # Nos quedamos sin criptomonedas
        criptos = 0
        
    else:
        # Si decidimos esperar o no pudimos comprar/vender
        print(f"🤔 Decidiste esperar")
    
    # --- Movimiento del mercado al final del día ---
    
    # El precio de la criptomoneda cambia para el próximo día
    precio_actual = movimiento_mercado(precio_actual)

# --- Fin de la simulación: mostramos resultados ---

# Calculamos el valor final (dinero + valor de criptomonedas que tengamos)
valor_final = dinero + (criptos * precio_actual)

# Mostramos los resultados finales
print("\n📈📉 RESULTADOS FINALES 📈📉")
print(f"Dinero en efectivo: ${dinero:.2f}")
print(f"Criptomonedas en posesión: {criptos:.2f}")
print(f"Valor total final: ${valor_final:.2f}")
