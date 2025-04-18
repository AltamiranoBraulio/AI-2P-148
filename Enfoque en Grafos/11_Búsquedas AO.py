from typing import List, Optional, Tuple

class PasoReceta:
    """Representa un paso en la preparación de una receta"""
    
    def __init__(self, nombre: str, tipo: str, tiempo: int, descripcion: str):
        """
        Args:
            nombre: Nombre del paso (ej. 'Cortar verduras')
            tipo: 'AND' (obligatorio) o 'OR' (alternativas)
            tiempo: Minutos requeridos
            descripcion: Instrucciones detalladas
        """
        self.nombre = nombre
        self.tipo = tipo
        self.tiempo = tiempo
        self.descripcion = descripcion
        self.completado = False
        self.siguientes: List[List['PasoReceta']] = []
    
    def agregar_opciones(self, *opciones: List['PasoReceta']):
        """Añade posibles pasos siguientes"""
        self.siguientes.extend(opciones)
    
    def __repr__(self):
        return f"{self.nombre} ({self.tipo}) - ⏱️{self.tiempo}min"

def ao_cocina(inicio: PasoReceta, tiempo_max: int) -> Optional[List[PasoReceta]]:
    """
    Algoritmo AO* adaptado para planificación de recetas
    
    Args:
        inicio: Paso inicial de la receta
        tiempo_max: Tiempo máximo disponible en minutos
    
    Returns:
        Secuencia óptima de pasos o None si no es posible
    """
    mejor_plan = None
    menor_tiempo = float('inf')
    
    def buscar(paso_actual: PasoReceta, plan_actual: List[PasoReceta], tiempo_actual: int):
        nonlocal mejor_plan, menor_tiempo
        
        if tiempo_actual > tiempo_max:
            return
        
        if not paso_actual.siguientes:  # Fin de la receta
            if tiempo_actual < menor_tiempo:
                menor_tiempo = tiempo_actual
                mejor_plan = plan_actual.copy()
            return
        
        for opcion in paso_actual.siguientes:
            if paso_actual.tipo == 'AND':
                # Todos los pasos de esta opción son obligatorios
                nuevo_plan = plan_actual.copy()
                nuevo_tiempo = tiempo_actual
                posible = True
                
                for paso in opcion:
                    if nuevo_tiempo + paso.tiempo > tiempo_max:
                        posible = False
                        break
                    nuevo_plan.append(paso)
                    nuevo_tiempo += paso.tiempo
                
                if posible:
                    buscar(opcion[-1], nuevo_plan, nuevo_tiempo)
            else:
                # Elegir una de las alternativas (OR)
                for paso in opcion:
                    if tiempo_actual + paso.tiempo <= tiempo_max:
                        nuevo_plan = plan_actual.copy()
                        nuevo_plan.append(paso)
                        buscar(paso, nuevo_plan, tiempo_actual + paso.tiempo)
    
    buscar(inicio, [inicio], inicio.tiempo)
    return mejor_plan

# Creación de la receta
def crear_receta_compleja() -> PasoReceta:
    """Crea una receta con pasos AND/OR"""
    # Pasos iniciales (todos AND)
    inicio = PasoReceta("Preparar ingredientes", "AND", 10, "Reunir todos los ingredientes")
    calentar_horno = PasoReceta("Calentar horno", "AND", 15, "Precalentar a 180°C")
    preparar_molde = PasoReceta("Engrasar molde", "AND", 5, "Enmantecar y enharinar")
    
    # Opciones para la masa (OR)
    mezcla_tradicional = PasoReceta("Mezcla tradicional", "AND", 10, "Mezclar harina, huevos y leche")
    mezcla_light = PasoReceta("Mezcla light", "AND", 15, "Sustituir con ingredientes bajos en calorías")
    
    # Pasos finales (AND)
    hornear = PasoReceta("Hornear", "AND", 30, "Hornear hasta dorar")
    decorar = PasoReceta("Decorar", "OR", 10, "Agregar toppings")
    servir = PasoReceta("Servir", "AND", 5, "Presentar en plato")
    
    # Opciones de decoración (OR)
    frutas = PasoReceta("Con frutas", "AND", 8, "Agregar fresas y kiwi")
    chocolate = PasoReceta("Con chocolate", "AND", 7, "Bañar con salsa de chocolate")
    natural = PasoReceta("Natural", "AND", 2, "Servir sin decoración")
    
    # Estructurar la receta
    inicio.agregar_opciones([calentar_horno, preparar_molde])
    calentar_horno.agregar_opciones([mezcla_tradicional], [mezcla_light])
    mezcla_tradicional.agregar_opciones([hornear])
    mezcla_light.agregar_opciones([hornear])
    hornear.agregar_opciones([decorar])
    decorar.agregar_opciones([frutas], [chocolate], [natural])
    frutas.agregar_opciones([servir])
    chocolate.agregar_opciones([servir])
    natural.agregar_opciones([servir])
    
    return inicio

# Ejemplo de uso
if __name__ == "__main__":
    print("🍽️ PLANIFICADOR DE RECETAS CON AO* 🧑‍🍳")
    print("Este algoritmo te ayuda a encontrar la forma más rápida de preparar una receta compleja")
    
    receta = crear_receta_compleja()
    tiempo_disponible = 60  # minutos
    
    plan = ao_cocina(receta, tiempo_disponible)
    
    if plan:
        print(f"\n¡Receta completable en {sum(p.tiempo for p in plan)} minutos!")
        print("\nPasos a seguir:")
        for i, paso in enumerate(plan, 1):
            print(f"{i}. {paso.nombre} (⏱️{paso.tiempo}min)")
            print(f"   → {paso.descripcion}")
        
        print("\nOpciones elegidas:")
        for paso in plan:
            if paso.tipo == 'OR':
                print(f"- En lugar de otras alternativas, elegiste: {paso.nombre}")
    else:
        print(f"\nNo es posible completar la receta en {tiempo_disponible} minutos 😢")
        print("Prueba aumentando el tiempo o simplificando la receta")