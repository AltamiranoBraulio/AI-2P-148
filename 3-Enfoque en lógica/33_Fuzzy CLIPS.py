# Importación de bibliotecas necesarias
import clips  # Biblioteca principal para integrar CLIPS (sistema experto) en Python
import numpy as np  # Para cálculos numéricos y manejo de arrays
import matplotlib.pyplot as plt  # Para visualización gráfica
from matplotlib import cm  # Mapas de color para visualizaciones
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D (no usado aquí pero incluido para extensiones futuras)

# ======================================================================
# 1. CONFIGURACIÓN DEL ENTORNO FUZZY CLIPS
# ======================================================================
# Crear un entorno CLIPS (el núcleo del sistema experto)
# Este objeto 'env' será nuestro contenedor para todas las reglas y hechos
env = clips.Environment()

# ======================================================================
# 2. DEFINICIÓN DE VARIABLES DIFUSAS (FUZZY SETS)
# ======================================================================
# Función para definir conjuntos difusos trapezoidales en CLIPS
def definir_conjunto_difuso(nombre, dominio_min, dominio_max, puntos):
    """
    Define un conjunto difuso trapezoidal en CLIPS.
    
    Args:
        nombre (str): Identificador del conjunto (ej: "fiebre-alta")
        dominio_min (float): Límite inferior del rango de valores
        dominio_max (float): Límite superior del rango de valores
        puntos (list): 4 puntos [a, b, c, d] que definen la forma trapezoidal:
                      a: inicio de la pendiente ascendente
                      b: fin de la pendiente ascendente
                      c: inicio de la pendiente descendente
                      d: fin de la pendiente descendente
    """
    # Construye el comando CLIPS para crear el conjunto difuso
    env.build(f"""
        (deffacts conjuntos-difusos
            (fuzzy-set (name {nombre})
                      (type trapezoidal)  # Forma trapezoidal
                      (params {puntos[0]} {puntos[1]} {puntos[2]} {puntos[3]})  # Puntos del trapezoide
                      (domain {dominio_min} {dominio_max}))  # Rango de valores posibles
    """)

# Definición de conjuntos difusos para síntomas médicos:

# Para fiebre (en grados Celsius)
definir_conjunto_difuso("fiebre-baja", 35, 42, [35, 35, 37, 38])  # 35-38°C
definir_conjunto_difuso("fiebre-moderada", 35, 42, [37, 38, 39, 40])  # 38-40°C
definir_conjunto_difuso("fiebre-alta", 35, 42, [39, 40, 42, 42])  # 40-42°C

# Para intensidad de tos (escala 0-10)
definir_conjunto_difuso("tos-leve", 0, 10, [0, 0, 3, 5])  # 0-5
definir_conjunto_difuso("tos-moderada", 0, 10, [3, 5, 7, 9])  # 5-9
definir_conjunto_difuso("tos-severa", 0, 10, [7, 9, 10, 10])  # 9-10

# Para intensidad de dolor (escala 0-10)
definir_conjunto_difuso("dolor-leve", 0, 10, [0, 0, 3, 5])  # 0-5
definir_conjunto_difuso("dolor-moderado", 0, 10, [3, 5, 7, 9])  # 5-9
definir_conjunto_difuso("dolor-severo", 0, 10, [7, 9, 10, 10])  # 9-10

# ======================================================================
# 3. REGLAS DIFUSAS (FUZZY RULES)
# ======================================================================
# Construcción de reglas de diagnóstico usando lógica difusa
env.build("""
    ;; Regla 1: Diagnóstico de gripe
    (defrule diagnostico-gripe
        (fuzzy-match fiebre-alta ?fiebre-certeza)  # Evalúa pertenencia a "fiebre-alta"
        (fuzzy-match tos-severa ?tos-certeza)      # Evalúa pertenencia a "tos-severa"
        =>
        (assert (enfermedad gripe (certainty (min ?fiebre-certeza ?tos-certeza))))
        # La certeza es el mínimo de las dos condiciones (AND difuso)
    
    ;; Regla 2: Diagnóstico de infección bacteriana
    (defrule diagnostico-infeccion
        (fuzzy-match fiebre-moderada ?fiebre-certeza)
        (fuzzy-match dolor-severo ?dolor-certeza)
        =>
        (assert (enfermedad infeccion-bacteriana (certainty (* ?fiebre-certeza ?dolor-certeza))))
        # Certeza como producto de las condiciones
    
    ;; Regla 3: Diagnóstico de resfriado común
    (defrule diagnostico-resfriado
        (fuzzy-match tos-moderada ?tos-certeza)
        (fuzzy-match dolor-leve ?dolor-certeza)
        =>
        (assert (enfermedad resfriado (certainty (/ (+ ?tos-certeza ?dolor-certeza) 2)))))
        # Certeza como promedio de las condiciones
""")

# ======================================================================
# 4. ENTRADA DE SÍNTOMAS DIFUSOS
# ======================================================================
def ingresar_sintomas():
    """Interfaz para ingresar valores de síntomas con lógica difusa"""
    print("\n** Ingreso de Síntomas **")
    # Solicitar valores al usuario
    fiebre = float(input("Temperatura corporal (35-42°C): "))  # Ej: 38.5
    tos = float(input("Intensidad de tos (0-10): "))          # Ej: 7.5
    dolor = float(input("Intensidad de dolor (0-10): "))      # Ej: 4.0
    
    # Convertir a hechos difusos en CLIPS
    env.assert_string(f"(fuzzy-value fiebre {fiebre})")  # Ej: (fuzzy-value fiebre 38.5)
    env.assert_string(f"(fuzzy-value tos {tos})")        # Ej: (fuzzy-value tos 7.5)
    env.assert_string(f"(fuzzy-value dolor {dolor})")    # Ej: (fuzzy-value dolor 4.0)

# ======================================================================
# 5. INFERENCIA DIFUSA Y RESULTADOS
# ======================================================================
def ejecutar_sistema():
    """Ejecuta el motor de inferencia y muestra resultados"""
    env.run()  # Dispara todas las reglas aplicables
    
    print("\n** Resultados del Diagnóstico **")
    enfermedades = []
    
    # Recorrer todos los hechos en la memoria de trabajo
    for fact in env.facts():
        if fact.template.name == "enfermedad":  # Filtrar hechos de diagnóstico
            nombre = fact[0]  # Nombre de la enfermedad (ej: "gripe")
            certeza = fact[1]  # Grado de certeza (ej: 0.75)
            enfermedades.append((nombre, certeza))
            print(f"- {nombre} (Certeza: {certeza:.2f})")  # Formateado a 2 decimales
    
    return enfermedades  # Lista de tuplas (enfermedad, certeza)

# ======================================================================
# 6. VISUALIZACIÓN DE CONJUNTOS DIFUSOS
# ======================================================================
def graficar_conjuntos_difusos():
    """Muestra gráficos de las funciones de pertenencia"""
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 3 subgráficos
    
    # Función trapezoidal para calcular grados de pertenencia
    def trapezoidal(x, a, b, c, d):
        """Calcula el grado de pertenencia para un valor x"""
        return np.maximum(0, np.minimum(np.minimum((x - a)/(b - a), 1), (d - x)/(d - c)))
    
    # Gráfico 1: Fiebre
    x = np.linspace(35, 42, 100)  # Rango de temperatura
    axs[0].plot(x, trapezoidal(x, 35, 35, 37, 38), label="Baja")
    axs[0].plot(x, trapezoidal(x, 37, 38, 39, 40), label="Moderada")
    axs[0].plot(x, trapezoidal(x, 39, 40, 42, 42), label="Alta")
    axs[0].set_title("Fiebre")
    axs[0].legend()
    
    # Gráfico 2: Tos
    x = np.linspace(0, 10, 100)  # Rango de intensidad
    axs[1].plot(x, trapezoidal(x, 0, 0, 3, 5), label="Leve")
    axs[1].plot(x, trapezoidal(x, 3, 5, 7, 9), label="Moderada")
    axs[1].plot(x, trapezoidal(x, 7, 9, 10, 10), label="Severa")
    axs[1].set_title("Tos")
    axs[1].legend()
    
    # Gráfico 3: Dolor
    axs[2].plot(x, trapezoidal(x, 0, 0, 3, 5), label="Leve")
    axs[2].plot(x, trapezoidal(x, 3, 5, 7, 9), label="Moderado")
    axs[2].plot(x, trapezoidal(x, 7, 9, 10, 10), label="Severo")
    axs[2].set_title("Dolor")
    axs[2].legend()
    
    plt.tight_layout()  # Ajuste automático de márgenes
    plt.show()  # Mostrar ventana con gráficos

# ======================================================================
# 7. SISTEMA DE RECOMENDACIÓN DIFUSA
# ======================================================================
def recomendar_tratamiento(enfermedades):
    """Genera recomendaciones basadas en diagnósticos"""
    if not enfermedades:
        print("No se detectaron enfermedades significativas.")
        return
    
    # Obtener enfermedad con mayor certeza
    enfermedad, certeza = max(enfermedades, key=lambda x: x[1])
    
    print(f"\n** Recomendación para {enfermedad} (Certeza: {certeza:.2f}) **")
    
    # Recomendaciones específicas por enfermedad
    if enfermedad == "gripe":
        print("- Reposo y líquidos")
        print("- Antivirales si es necesario")
    elif enfermedad == "infeccion-bacteriana":
        print("- Antibióticos recetados")
        print("- Analgésicos para el dolor")
    elif enfermedad == "resfriado":
        print("- Antihistamínicos")
        print("- Descanso adecuado")

# ======================================================================
# 8. INTERFAZ DE USUARIO PRINCIPAL
# ======================================================================
def main():
    # Banner ASCII art
    print("""
    ███████╗██╗   ██╗███████╗███████╗██╗   ██╗    ██████╗██╗     ██╗██████╗ ███████╗
    ██╔════╝╚██╗ ██╔╝╚══███╔╝╚══███╔╝╚██╗ ██╔╝   ██╔════╝██║     ██║██╔══██╗██╔════╝
    █████╗   ╚████╔╝   ███╔╝   ███╔╝  ╚████╔╝    ██║     ██║     ██║██████╔╝███████╗
    ██╔══╝    ╚██╔╝   ███╔╝   ███╔╝    ╚██╔╝     ██║     ██║     ██║██╔═══╝ ╚════██║
    ███████╗   ██║   ███████╗███████╗   ██║      ╚██████╗███████╗██║██║     ███████║
    ╚══════╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝       ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝
    """)
    
    # Bucle principal de la interfaz
    while True:
        print("\n=== **Sistema de Diagnóstico Difuso** ===")
        print("1. Ingresar síntomas")
        print("2. Ver conjuntos difusos")
        print("3. Ejecutar diagnóstico")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ingresar_sintomas()
        elif opcion == "2":
            graficar_conjuntos_difusos()
        elif opcion == "3":
            enfermedades = ejecutar_sistema()
            recomendar_tratamiento(enfermedades)
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

# Punto de entrada principal
if __name__ == "__main__":
    main()