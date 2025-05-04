"""
Sistema de demostración de Lógica Modal que implementa:
- Operadores modales: □ (necesidad) y ◇ (posibilidad)
- Semántica de mundos posibles con relaciones de accesibilidad
- Evaluación de fórmulas modales complejas
- Aplicación práctica en modelado de conocimiento y creencias
"""

class Mundo:
    """
    Representa un mundo posible en la semántica de Kripke.
    Cada mundo contiene:
    - Un nombre identificador
    - Proposiciones verdaderas en ese mundo
    - Mundos accesibles desde este mundo
    """
    def __init__(self, nombre):
        self.nombre = nombre  # Identificador único del mundo
        self.proposiciones = set()  # Conjunto de proposiciones verdaderas
        self.accesibles = set()  # Conjunto de mundos accesibles

    def agregar_proposicion(self, prop):
        """Añade una proposición verdadera en este mundo"""
        self.proposiciones.add(prop)

    def agregar_accesible(self, mundo):
        """Establece una relación de accesibilidad a otro mundo"""
        self.accesibles.add(mundo)

    def verificar_proposicion(self, prop):
        """Verifica si una proposición es verdadera en este mundo"""
        return prop in self.proposiciones

    def __str__(self):
        return f"Mundo {self.nombre}: {', '.join(self.proposiciones)}"


class ModeloKripke:
    """
    Estructura de Kripke que contiene:
    - Conjunto de mundos posibles
    - Relaciones de accesibilidad entre mundos
    - Mundo actual (punto de evaluación)
    """
    def __init__(self):
        self.mundos = {}  # Diccionario de mundos por nombre
        self.mundo_actual = None  # Mundo de evaluación actual

    def agregar_mundo(self, nombre, proposiciones=None):
        """Crea y añade un nuevo mundo al modelo"""
        nuevo_mundo = Mundo(nombre)
        if proposiciones:
            for prop in proposiciones:
                nuevo_mundo.agregar_proposicion(prop)
        self.mundos[nombre] = nuevo_mundo
        return nuevo_mundo

    def establecer_accesibilidad(self, origen, destino):
        """Crea una relación de accesibilidad entre mundos"""
        mundo_origen = self.mundos.get(origen)
        mundo_destino = self.mundos.get(destino)
        if mundo_origen and mundo_destino:
            mundo_origen.agregar_accesible(mundo_destino)

    def establecer_mundo_actual(self, nombre):
        """Fija el mundo actual para evaluación"""
        self.mundo_actual = self.mundos.get(nombre)

    def evaluar(self, formula):
        """
        Evalúa una fórmula modal en el mundo actual.
        Soporta:
        - Proposiciones atómicas: 'p', 'q', etc.
        - Conectivos lógicos: ¬, ∧, ∨, →, ↔
        - Operadores modales: □ (necesario), ◇ (posible)
        """
        # Eliminamos espacios para facilitar el parsing
        formula = formula.replace(" ", "")
        
        # Llamamos al evaluador recursivo
        return self._evaluar_recursivo(formula)

    def _evaluar_recursivo(self, formula):
        """Evaluador recursivo de fórmulas modales"""
        
        # Caso base: proposición atómica
        if len(formula) == 1 and formula.isalpha():
            return self.mundo_actual.verificar_proposicion(formula)
        
        # Negación: ¬φ
        if formula.startswith("¬"):
            return not self._evaluar_recursivo(formula[1:])
        
        # Operador necesario: □φ
        if formula.startswith("□"):
            subformula = formula[1:]
            # □φ es verdadero si φ es verdadero en todos los mundos accesibles
            for mundo in self.mundo_actual.accesibles:
                mundo_original = self.mundo_actual
                self.mundo_actual = mundo
                if not self._evaluar_recursivo(subformula):
                    self.mundo_actual = mundo_original
                    return False
                self.mundo_actual = mundo_original
            return True
        
        # Operador posible: ◇φ
        if formula.startswith("◇"):
            subformula = formula[1:]
            # ◇φ es verdadero si φ es verdadero en algún mundo accesible
            for mundo in self.mundo_actual.accesibles:
                mundo_original = self.mundo_actual
                self.mundo_actual = mundo
                if self._evaluar_recursivo(subformula):
                    self.mundo_actual = mundo_original
                    return True
                self.mundo_actual = mundo_original
            return False
        
        # Conectivos binarios: detectamos el operador principal
        # Usamos paréntesis para agrupar adecuadamente
        if formula.startswith("(") and formula.endswith(")"):
            # Eliminamos paréntesis exteriores
            return self._evaluar_recursivo(formula[1:-1])
        
        # Buscamos el operador binario principal (no dentro de paréntesis)
        nivel_parentesis = 0
        for i, char in enumerate(formula):
            if char == "(":
                nivel_parentesis += 1
            elif char == ")":
                nivel_parentesis -= 1
            elif nivel_parentesis == 0:
                if char == "∧":  # Conjunción: φ ∧ ψ
                    left = formula[:i]
                    right = formula[i+1:]
                    return self._evaluar_recursivo(left) and self._evaluar_recursivo(right)
                elif char == "∨":  # Disyunción: φ ∨ ψ
                    left = formula[:i]
                    right = formula[i+1:]
                    return self._evaluar_recursivo(left) or self._evaluar_recursivo(right)
                elif char == "→":  # Implicación: φ → ψ
                    left = formula[:i]
                    right = formula[i+1:]
                    return (not self._evaluar_recursivo(left)) or self._evaluar_recursivo(right)
                elif char == "↔":  # Bicondicional: φ ↔ ψ
                    left = formula[:i]
                    right = formula[i+1:]
                    return self._evaluar_recursivo(left) == self._evaluar_recursivo(right)
        
        # Si llegamos aquí, la fórmula no es válida
        raise ValueError(f"Fórmula modal no válida: {formula}")

    def __str__(self):
        """Representación textual del modelo"""
        result = []
        for nombre, mundo in self.mundos.items():
            accesibles = ", ".join(m.nombre for m in mundo.accesibles)
            props = ", ".join(mundo.proposiciones)
            result.append(f"{nombre} [Accesibles: {accesibles}] -> {props}")
        return "\n".join(result)


# ---------------------------------------------------------------
# Ejemplo práctico: Sistema de modelado de conocimiento y creencias
# ---------------------------------------------------------------

def construir_ejemplo_conocimiento():
    """
    Construye un modelo de Kripke para ejemplificar:
    - □p: p es conocido (verdadero en todos los mundos accesibles)
    - ◇q: q es creíble (verdadero en al menos un mundo accesible)
    """
    modelo = ModeloKripke()
    
    # Creamos tres mundos posibles
    mundo1 = modelo.agregar_mundo("w1", ["p", "q"])
    mundo2 = modelo.agregar_mundo("w2", ["p"])
    mundo3 = modelo.agregar_mundo("w3", ["q"])
    
    # Establecemos relaciones de accesibilidad (simétrica para este ejemplo)
    modelo.establecer_accesibilidad("w1", "w2")
    modelo.establecer_accesibilidad("w1", "w3")
    modelo.establecer_accesibilidad("w2", "w1")
    modelo.establecer_accesibilidad("w3", "w1")
    
    # Fijamos w1 como mundo actual
    modelo.establecer_mundo_actual("w1")
    
    return modelo


def demostracion_logica_modal():
    """Demostración interactiva de lógica modal"""
    print("\nDEMOSTRACIÓN DE LÓGICA MODAL")
    print("---------------------------")
    
    # Construimos el modelo de ejemplo
    modelo = construir_ejemplo_conocimiento()
    print("\nModelo de Kripke creado:")
    print(modelo)
    
    # Fórmulas para evaluar
    formulas = [
        "p",                # p es verdadero en w1
        "q",                # q es verdadero en w1
        "¬q",               # ¬q es falso en w1
        "□p",               # p es necesario (verdadero en todos los mundos accesibles)
        "◇q",               # q es posible (verdadero en al menos un mundo accesible)
        "□q",               # q no es necesario (falso en w2)
        "◇¬p",              # ¬p es posible (falso en todos los mundos accesibles)
        "p ∧ q",            # Conjunción verdadera en w1
        "□p → ◇q",          # Si p es necesario, entonces q es posible
        "◇(p ∧ q)",         # p ∧ q es posible (verdadero en w1)
        "□(p ∨ q)"          # p ∨ q es necesario (verdadero en todos los mundos)
    ]
    
    # Evaluamos cada fórmula
    print("\nEvaluación de fórmulas modales en w1:")
    for formula in formulas:
        resultado = modelo.evaluar(formula)
        print(f"  {formula:<15} -> {'Verdadero' if resultado else 'Falso'}")
    
    # Cambiamos al mundo w2 y evaluamos algunas fórmulas
    modelo.establecer_mundo_actual("w2")
    print("\nEvaluación en w2:")
    formulas_w2 = ["p", "q", "□p", "◇q"]
    for formula in formulas_w2:
        resultado = modelo.evaluar(formula)
        print(f"  {formula:<15} -> {'Verdadero' if resultado else 'Falso'}")


# ---------------------------------------------------------------
# Interfaz de usuario simple para experimentar con el sistema
# ---------------------------------------------------------------

def interfaz_usuario():
    """Interfaz simple para crear y evaluar modelos modales"""
    print("SISTEMA DE LÓGICA MODAL INTERACTIVO")
    print("----------------------------------")
    
    modelo = ModeloKripke()
    
    while True:
        print("\nOpciones:")
        print("1. Crear nuevo mundo")
        print("2. Establecer proposiciones en un mundo")
        print("3. Establecer relación de accesibilidad")
        print("4. Seleccionar mundo actual")
        print("5. Evaluar fórmula modal")
        print("6. Mostrar modelo completo")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del nuevo mundo: ")
            modelo.agregar_mundo(nombre)
            print(f"Mundo {nombre} creado.")
            
        elif opcion == "2":
            mundo = input("Nombre del mundo: ")
            if mundo in modelo.mundos:
                props = input("Proposiciones (separadas por comas): ").split(",")
                for prop in props:
                    modelo.mundos[mundo].agregar_proposicion(prop.strip())
                print(f"Proposiciones añadidas a {mundo}.")
            else:
                print("Mundo no encontrado.")
                
        elif opcion == "3":
            origen = input("Mundo origen: ")
            destino = input("Mundo destino: ")
            if origen in modelo.mundos and destino in modelo.mundos:
                modelo.establecer_accesibilidad(origen, destino)
                print(f"Accesibilidad establecida: {origen} -> {destino}")
            else:
                print("Uno o ambos mundos no existen.")
                
        elif opcion == "4":
            mundo = input("Mundo actual: ")
            if mundo in modelo.mundos:
                modelo.establecer_mundo_actual(mundo)
                print(f"Mundo actual establecido a {mundo}")
            else:
                print("Mundo no encontrado.")
                
        elif opcion == "5":
            if modelo.mundo_actual:
                formula = input("Fórmula modal a evaluar: ")
                try:
                    resultado = modelo.evaluar(formula)
                    print(f"Resultado: {'Verdadero' if resultado else 'Falso'}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Primero seleccione un mundo actual.")
                
        elif opcion == "6":
            print("\nModelo actual:")
            print(modelo)
            
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
            
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    # Ejecutar demostración automática
    demostracion_logica_modal()
    
    # Opcional: Ejecutar interfaz interactiva
    # interfaz_usuario()