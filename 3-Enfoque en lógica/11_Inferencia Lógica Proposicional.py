# Motor de inferencia lógica proposicional creativo

# Base de hechos iniciales (los hechos que ya sabemos si son verdaderos o falsos)
hechos = {
    "P": True,    # Hecho 'P' es verdadero
    "Q": False,   # Hecho 'Q' es falso
}

# Reglas de inferencia
# Cada regla es una tupla: (lista de condiciones, conclusión)
# Por ejemplo: Si P y Q son verdaderos, entonces podemos concluir R
reglas = [
    (["P", "Q"], "R"),  # Regla 1: Si P y Q son verdaderos, entonces R es verdadero
    (["R"], "S"),       # Regla 2: Si R es verdadero, entonces S es verdadero
    (["P"], "T"),       # Regla 3: Si P es verdadero, entonces T es verdadero
]

# Función que aplica todas las reglas para inferir nuevos hechos
def inferir(hechos, reglas):
    nuevos = True  # Variable para saber si seguimos encontrando nuevos hechos
    while nuevos:  # Mientras sigamos infiriendo algo nuevo, seguimos el bucle
        nuevos = False  # Por defecto, no encontramos nada nuevo en esta ronda
        for condiciones, conclusion in reglas:  # Revisamos cada regla una por una
            # Verificamos si todas las condiciones de la regla son verdaderas
            if all(hechos.get(c, False) for c in condiciones):
                # Si la conclusión no está aún como verdadera, la inferimos
                if not hechos.get(conclusion, False):
                    hechos[conclusion] = True  # Añadimos la conclusión como hecho verdadero
                    print(f"✅ Nueva inferencia: '{conclusion}' es ahora VERDADERO")  # Mensaje para el usuario
                    nuevos = True  # Indicamos que encontramos algo nuevo, así que seguimos la próxima ronda
    return hechos  # Devolvemos la nueva base de hechos actualizada

# Función para consultar si un hecho/meta se puede inferir
def consultar(meta):
    # Si el hecho ya es verdadero en la base de hechos
    if hechos.get(meta, False):
        print(f"🔎 '{meta}' ya es un hecho conocido (VERDADERO).")
    else:  # Si no es conocido, tratamos de inferirlo usando reglas
        print(f"🤔 '{meta}' no es conocido aún. Vamos a inferir...")
        inferir(hechos, reglas)  # Aplicamos el motor de inferencias
        # Después de inferir, revisamos otra vez si ya podemos concluir el hecho
        if hechos.get(meta, False):
            print(f"🎯 ¡Éxito! '{meta}' ha sido inferido como VERDADERO.")
        else:
            print(f"❌ No se pudo inferir '{meta}'.")

# Bucle interactivo para que el usuario juegue con el sistema
while True:
    # Mostramos el menú de opciones
    print("\n===== MOTOR DE INFERENCIA LÓGICA =====")
    print("Hechos actuales:", hechos)  # Mostramos todos los hechos actuales
    print("Opciones:")
    print("1. Consultar inferencia")  # Opción 1: consultar si un hecho puede inferirse
    print("2. Agregar hecho")         # Opción 2: agregar un nuevo hecho verdadero
    print("3. Salir")                 # Opción 3: terminar el programa
    
    # Pedimos al usuario que elija una opción
    opcion = input("Elige una opción (1/2/3): ")
    
    # Si eligió la opción 1: quiere consultar algo
    if opcion == "1":
        meta = input("¿Qué quieres consultar?: ").strip()  # Pedimos qué hecho quiere consultar
        consultar(meta)  # Llamamos a la función consultar con lo que pidió el usuario
    # Si eligió la opción 2: quiere agregar un nuevo hecho
    elif opcion == "2":
        nuevo_hecho = input("Introduce el nuevo hecho (ejemplo: 'Q'): ").strip()  # Pedimos el nombre del hecho
        hechos[nuevo_hecho] = True  # Lo agregamos como verdadero en la base de hechos
        print(f"✅ Hecho '{nuevo_hecho}' agregado como VERDADERO.")  # Confirmamos al usuario
    # Si eligió la opción 3: salir del programa
    elif opcion == "3":
        print("¡Adiós! 👋")  # Mensaje de despedida
        break  # Salimos del bucle while y terminamos el programa
    # Si no eligió una opción válida
    else:
        print("Opción inválida, intenta de nuevo.")  # Le decimos que intente otra vez
