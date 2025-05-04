# Importar las clases necesarias de la librería python-constraint
# Problem: Para definir el problema CSP
# AllDifferentConstraint: Para implementar restricciones de "todos diferentes"
from constraint import Problem, AllDifferentConstraint

# Definir la función principal que asignará tareas usando CSP
def asignar_tareas_familia():
    """Asigna tareas domésticas a familiares usando CSP (Problema de Satisfacción de Restricciones)"""
    
    # 1. Crear una instancia del problema CSP
    # Esto inicializa un nuevo problema de satisfacción de restricciones vacío
    problema = Problem()
    
    # 2. Definir las variables del problema (los familiares)
    # Cada familiar es una variable que debe recibir una tarea
    familiares = ["Papá", "Mamá", "Hijo", "Hija", "Abuelo"]
    
    # 3. Definir los dominios (valores posibles para cada variable)
    # Lista de todas las tareas domésticas posibles que pueden asignarse
    tareas = [
        "Cocinar", "Lavar platos", "Limpiar baño", 
        "Aspirar", "Hacer compras", "Lavar ropa",
        "Regar plantas", "Pasear al perro"
    ]
    
    # 4. Agregar cada variable al problema con su dominio
    # Para cada familiar, el dominio es la lista completa de tareas
    for familiar in familiares:
        problema.addVariable(familiar, tareas)  # Asocia cada familiar con todas las tareas posibles
    
    # 5. Agregar restricciones al problema
    
    # a) Restricción global: Todos deben tener tareas diferentes
    # Usa AllDifferentConstraint para asegurar que ninguna tarea se repita
    problema.addConstraint(AllDifferentConstraint(), familiares)
    
    # b) Restricciones individuales basadas en preferencias
    
    # El abuelo no quiere limpiar el baño (función lambda que filtra "Limpiar baño")
    problema.addConstraint(lambda t: t != "Limpiar baño", ["Abuelo"])
    
    # Mamá solo quiere cocinar o hacer compras (función lambda que filtra esas opciones)
    problema.addConstraint(lambda t: t in ["Cocinar", "Hacer compras"], ["Mamá"])
    
    # Hijo solo puede aspirar o pasear al perro (función lambda que filtra esas opciones)
    problema.addConstraint(lambda t: t in ["Aspirar", "Pasear al perro"], ["Hijo"])
    
    # Papá se niega a lavar platos (función lambda que excluye esa opción)
    problema.addConstraint(lambda t: t != "Lavar platos", ["Papá"])
    
    # Hija prefiere regar plantas o lavar ropa (función lambda que filtra esas opciones)
    problema.addConstraint(lambda t: t in ["Regar plantas", "Lavar ropa"], ["Hija"])
    
    # c) Restricciones entre familiares (relaciones)
    
    # Si papá cocina, entonces el hijo debe lavar platos
    # La función lambda implementa esta lógica condicional
    problema.addConstraint(
        lambda t1, t2: t1 != "Cocinar" or t2 == "Lavar platos",  # Si t1 es Cocinar, t2 debe ser Lavar platos
        ["Papá", "Hijo"]  # Aplica esta restricción entre Papá e Hijo
    )
    
    # 6. Obtener todas las soluciones posibles que satisfacen las restricciones
    # getSolutions() retorna una lista de diccionarios con todas las asignaciones válidas
    soluciones = problema.getSolutions()
    
    # 7. Mostrar los resultados obtenidos
    
    # Imprimir cuántas soluciones válidas se encontraron
    print("💡 Soluciones encontradas:", len(soluciones))
    
    # Mostrar una solución específica (la primera de la lista)
    print("\n✨ Una solución posible:")
    for familiar, tarea in soluciones[0].items():  # Iterar sobre el primer diccionario de solución
        print(f"{familiar}: {tarea}")  # Imprimir cada familiar con su tarea asignada
    
    # 8. Visualización creativa de la distribución de tareas
    
    print("\n📊 Distribución de tareas:")
    # Convertir los valores del diccionario (tareas) a una lista
    tareas_asignadas = list(soluciones[0].values())
    
    # Para cada tarea única en la solución
    for tarea in set(tareas_asignadas):
        # Contar cuántas veces aparece la tarea (en este caso siempre será 1 por AllDifferentConstraint)
        count = tareas_asignadas.count(tarea)
        # Imprimir la tarea con emojis de estrella (⭐) según el conteo
        print(f"{tarea}: {'⭐' * count}")

# Bloque principal que se ejecuta cuando el script es llamado directamente
if __name__ == "__main__":
    # Mostrar título del programa
    print("🏠 ASIGNACIÓN INTELIGENTE DE TAREAS DOMÉSTICAS 🏠")
    print("Resolviendo con Satisfacción de Restricciones...\n")
    
    # Llamar a la función principal
    asignar_tareas_familia()