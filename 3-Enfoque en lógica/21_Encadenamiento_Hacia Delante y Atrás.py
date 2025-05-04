# 💥 Motor de Diagnóstico Inteligente
# Usa Encadenamiento Hacia Adelante y Hacia Atrás
# Autor: ChatGPT para Babyarm 👑

# 📚 Base de Conocimiento (Hechos iniciales conocidos)
hechos_iniciales = {'tiene_fiebre', 'tiene_dolor_garganta', 'tiene_tos'}  # Estos son los síntomas que el paciente presenta al inicio

# 📚 Reglas del sistema experto
reglas = [
    (['tiene_fiebre', 'tiene_dolor_garganta'], 'tiene_infeccion'),  # Si tiene fiebre y dolor de garganta, entonces tiene infección
    (['tiene_tos', 'tiene_fiebre'], 'tiene_gripe'),  # Si tiene tos y fiebre, entonces tiene gripe
    (['tiene_infeccion'], 'necesita_antibiotico'),  # Si tiene infección, entonces necesita antibiótico
    (['tiene_gripe'], 'necesita_descanso'),  # Si tiene gripe, entonces necesita descanso
    (['tiene_gripe', 'tiene_infeccion'], 'caso_severo'),  # Si tiene gripe e infección, es un caso severo
]

# 🌐 Motor de encadenamiento hacia adelante (razonamiento directo)
def encadenamiento_adelante(hechos, reglas):
    nuevos_hechos = hechos.copy()  # Copiamos los hechos iniciales para no modificarlos directamente
    aplicado = True  # Variable bandera para controlar si seguimos aplicando reglas

    print("\n🚀 Encadenamiento Hacia Adelante (Descubriendo posibles diagnósticos...)")  # Mensaje de inicio
    while aplicado:  # Mientras se apliquen reglas nuevas, seguimos
        aplicado = False  # Suponemos que no aplicaremos reglas (hasta que lo hagamos)
        for premisas, conclusion in reglas:  # Recorremos cada regla: premisas => conclusión
            if all(p in nuevos_hechos for p in premisas):  # Si todas las premisas están en nuestros hechos
                if conclusion not in nuevos_hechos:  # Y la conclusión aún no está en los hechos
                    print(f"✅ Regla aplicada: {premisas} ➡️ {conclusion}")  # Informamos qué regla aplicamos
                    nuevos_hechos.add(conclusion)  # Añadimos la nueva conclusión como hecho
                    aplicado = True  # Marcamos que aplicamos al menos una regla
    print("🏁 Hechos finales descubiertos:", nuevos_hechos)  # Mostramos los hechos encontrados al final
    return nuevos_hechos  # Retornamos todos los hechos inferidos

# 🌐 Motor de encadenamiento hacia atrás (comprobación por metas)
def encadenamiento_atras(meta, hechos, reglas, profundidad=0):  # Profundidad nos ayuda a sangrar el texto para claridad
    sangria = "  " * profundidad  # Calculamos la sangría para cada nivel de recursión
    print(f"{sangria}🔍 ¿Es '{meta}' cierto?")  # Preguntamos si la meta es cierta

    if meta in hechos:  # Si la meta ya está en los hechos conocidos
        print(f"{sangria}✅ Sí, '{meta}' es un hecho conocido.")  # Confirmamos que es cierto
        return True  # Retornamos que sí es cierto

    for premisas, conclusion in reglas:  # Recorremos todas las reglas
        if conclusion == meta:  # Si la conclusión de la regla es nuestra meta
            print(f"{sangria}🔄 Probando regla: {premisas} ➡️ {conclusion}")  # Mostramos que probaremos esta regla
            # Comprobamos recursivamente si todas las premisas son verdaderas
            if all(encadenamiento_atras(p, hechos, reglas, profundidad + 1) for p in premisas):
                print(f"{sangria}✅ '{meta}' demostrado usando regla {premisas}")  # Si todas son ciertas, demostramos la meta
                return True  # Retornamos que es cierto

    print(f"{sangria}❌ No se pudo demostrar '{meta}'")  # Si ninguna regla nos lleva a la meta, fallamos
    return False  # Retornamos falso, no podemos probar la meta

# 🧪 Función creativa: Hacer Diagnóstico Automático usando hacia atrás
def hacer_diagnostico(hechos, reglas):
    print("\n🎯 Diagnóstico Personalizado")  # Mensaje de inicio
    posibles_diagnosticos = ['tiene_infeccion', 'tiene_gripe', 'caso_severo']  # Definimos las metas que queremos verificar
    for diag in posibles_diagnosticos:  # Recorremos cada diagnóstico posible
        print(f"\n🤔 Verificando si el diagnóstico es: {diag}")  # Informamos cuál estamos verificando
        resultado = encadenamiento_atras(diag, hechos, reglas)  # Usamos hacia atrás para comprobarlo
        if resultado:  # Si se puede demostrar
            print(f"🎉 Diagnóstico confirmado: {diag.upper()} ✅")  # Confirmamos el diagnóstico
        else:  # Si no
            print(f"🚫 No hay evidencia suficiente para: {diag}")  # Informamos que no se pudo comprobar

# 🩺 Función creativa: Recomendaciones Automáticas usando hacia adelante
def recomendar_tratamiento(hechos, reglas):
    print("\n💊 Recomendaciones Automáticas basadas en tus síntomas:")  # Mensaje de inicio
    hechos_finales = encadenamiento_adelante(hechos, reglas)  # Obtenemos todos los hechos posibles usando hacia adelante
    tratamientos = [h for h in hechos_finales if h.startswith('necesita')]  # Filtramos solo los hechos que son tratamientos
    if tratamientos:  # Si hay tratamientos encontrados
        for t in tratamientos:  # Recorremos cada uno
            print(f"✅ Recomendación: {t.replace('_', ' ').capitalize()}")  # Mostramos la recomendación de forma legible
    else:  # Si no hay tratamientos
        print("🚫 No se encontraron tratamientos recomendados.")  # Informamos que no encontramos nada

# === PRUEBAS ===
print("\n========================")  # Línea decorativa
print("🔬 Diagnóstico Inteligente (Modo Completo)")  # Título del modo completo
print("========================")  # Línea decorativa

# Paso 1: Diagnosticar usando Hacia Atrás
hacer_diagnostico(hechos_iniciales, reglas)  # Llamamos a la función de diagnóstico

# Paso 2: Recomendar Tratamientos usando Hacia Adelante
recomendar_tratamiento(hechos_iniciales, reglas)  # Llamamos a la función de recomendaciones
