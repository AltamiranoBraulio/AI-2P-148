# --- Eliminación de Variables: Detección de Fraude en Tarjetas de Crédito --- #

def eliminacion_variables_fraude():
    # --- 1. Definir las probabilidades base del modelo --- #
    
    # Probabilidad previa (prior) de que exista o no fraude
    P_F = {
        'Sí': 0.02,  # Solo un 2% de las transacciones son fraude
        'No': 0.98   # El 98% de las transacciones no son fraude
    }
    
    # Probabilidad de ubicación sospechosa dado que es fraude o no
    P_L_dado_F = {
        'Sí': {'Sí': 0.9, 'No': 0.1},  # Si es fraude, alta probabilidad de ubicación rara
        'No': {'Sí': 0.2, 'No': 0.8}   # Si no es fraude, baja probabilidad de ubicación rara
    }
    
    # Probabilidad de monto alto dado que es fraude o no
    P_T_dado_F = {
        'Sí': {'Sí': 0.8, 'No': 0.2},  # Si es fraude, alta probabilidad de monto alto
        'No': {'Sí': 0.1, 'No': 0.9}   # Si no es fraude, baja probabilidad de monto alto
    }
    
    # --- 2. Establecer la evidencia observada --- #
    evidencia_ubicacion = 'Sí'  # Se detectó una ubicación sospechosa
    evidencia_monto = 'Sí'      # Se detectó un monto de transacción alto
    
    # --- 3. Calcular los numeradores para cada posible valor de "Fraude" --- #
    numerador = {}
    
    # Para cada estado posible de "Fraude" ('Sí' o 'No')
    for fraude in ['Sí', 'No']:
        # Multiplicamos:
        # - La probabilidad de que ocurra el fraude (o no),
        # - La probabilidad de ver esa ubicación dado el estado de fraude,
        # - La probabilidad de ver ese monto dado el estado de fraude.
        
        prob_fraude = P_F[fraude]
        prob_ubicacion = P_L_dado_F[fraude][evidencia_ubicacion]
        prob_monto = P_T_dado_F[fraude][evidencia_monto]
        
        # Guardamos el producto en el numerador
        numerador[fraude] = prob_fraude * prob_ubicacion * prob_monto

    # --- 4. Sumar todos los numeradores para calcular el denominador --- #
    # Esto sirve para normalizar las probabilidades
    total = sum(numerador.values())
    
    # --- 5. Normalizar: dividir cada numerador entre el total --- #
    # Así obtenemos la probabilidad real condicionada
    probabilidad_final = {
        fraude: numerador[fraude] / total for fraude in numerador
    }
    
    # --- 6. Mostrar resultados finales --- #
    print("\n🔎 Resultado de Inferencia:")
    print("Probabilidad de que haya sido fraude dado ubicación sospechosa y monto alto:")
    for estado, prob in probabilidad_final.items():
        print(f"P(Fraude = {estado} | Ubicación=Sí, Monto=Sí) = {prob:.4f}")

# Ejecutar el modelo
eliminacion_variables_fraude()
