# Primero, definimos una clase para representar los nodos en la Red Semántica
class NodoConcepto:
    def __init__(self, nombre):
        # El nombre es el identificador del concepto (ejemplo: "Perro")
        self.nombre = nombre
        # Las relaciones son un diccionario: {tipo_relacion: [otros_nodos]}
        # Ejemplo: {"es_un": ["Animal"], "tiene": ["Cola", "Patas"]}
        self.relaciones = {}

    def agregar_relacion(self, tipo, otro_nodo):
        # Este método permite agregar relaciones al nodo
        # tipo es el nombre de la relación (ejemplo: "es_un")
        # otro_nodo es otro NodoConcepto con el que está relacionado
        if tipo not in self.relaciones:
            self.relaciones[tipo] = []
        self.relaciones[tipo].append(otro_nodo)

    def mostrar_relaciones(self):
        # Este método muestra en pantalla todas las relaciones del nodo
        print(f"\nConcepto: {self.nombre}")
        for tipo, nodos in self.relaciones.items():
            nombres_nodos = [n.nombre for n in nodos]
            print(f"  {tipo} -> {', '.join(nombres_nodos)}")

# Clase para la Red Semántica completa
class RedSemantica:
    def __init__(self):
        # Un diccionario donde cada concepto se almacena por su nombre
        self.nodos = {}

    def agregar_concepto(self, nombre):
        # Método para agregar un nuevo concepto a la red
        if nombre not in self.nodos:
            self.nodos[nombre] = NodoConcepto(nombre)
        return self.nodos[nombre]

    def conectar(self, nombre_origen, tipo_relacion, nombre_destino):
        # Método para conectar dos conceptos con una relación
        origen = self.agregar_concepto(nombre_origen)
        destino = self.agregar_concepto(nombre_destino)
        origen.agregar_relacion(tipo_relacion, destino)

    def mostrar_red(self):
        # Muestra todas las relaciones de la red semántica
        print("\n--- Red Semántica ---")
        for nodo in self.nodos.values():
            nodo.mostrar_relaciones()

# Clase para representar Reglas en forma de lógica descriptiva
class Regla:
    def __init__(self, condicion, accion):
        # La condición es una función que recibe la red y devuelve True o False
        self.condicion = condicion
        # La acción es una función que se ejecuta si la condición es True
        self.accion = accion

    def evaluar(self, red):
        # Este método evalúa la regla en la red semántica
        if self.condicion(red):
            self.accion(red)

# ---------------------------
# Ejemplo completo del sistema
# ---------------------------

# 1) Creamos la red semántica
red = RedSemantica()

# 2) Agregamos conceptos y relaciones
# Por ejemplo: Un perro es un animal
red.conectar("Perro", "es_un", "Animal")
# Un gato también es un animal
red.conectar("Gato", "es_un", "Animal")
# Los animales tienen corazón
red.conectar("Animal", "tiene", "Corazón")

# 3) Mostramos la red actual
red.mostrar_red()

# 4) Definimos una regla lógica descriptiva
# La regla dice: 
# "Si un concepto es un 'Animal', entonces también 'tiene' un 'Corazón'"
def condicion_animales_sin_corazon(red):
    # Esta condición busca animales que aún NO tengan un corazón relacionado
    for nodo in red.nodos.values():
        # Revisa si el nodo tiene relación 'es_un' con 'Animal'
        if any(rel.nombre == "Animal" for rel in nodo.relaciones.get("es_un", [])):
            # Y revisa si NO tiene aún la relación 'tiene' con 'Corazón'
            if "tiene" not in nodo.relaciones or not any(rel.nombre == "Corazón" for rel in nodo.relaciones["tiene"]):
                return True  # Si encuentra al menos uno, la condición es True
    return False  # Si no encuentra ninguno, la condición es False

def accion_agregar_corazon(red):
    # Esta acción agrega la relación 'tiene' un 'Corazón' a los animales que no lo tienen aún
    corazon = red.agregar_concepto("Corazón")
    for nodo in red.nodos.values():
        if any(rel.nombre == "Animal" for rel in nodo.relaciones.get("es_un", [])):
            if "tiene" not in nodo.relaciones or not any(rel.nombre == "Corazón" for rel in nodo.relaciones["tiene"]):
                nodo.agregar_relacion("tiene", corazon)
                print(f"Regla aplicada: '{nodo.nombre}' ahora tiene un Corazón.")

# Creamos la regla con su condición y acción
regla_corazon = Regla(condicion_animales_sin_corazon, accion_agregar_corazon)

# 5) Evaluamos la regla en la red semántica
regla_corazon.evaluar(red)

# 6) Mostramos la red después de aplicar la regla
red.mostrar_red()
