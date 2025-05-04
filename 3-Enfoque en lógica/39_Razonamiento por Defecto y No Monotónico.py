# --------------------------------------------
# Ejemplo de Razonamiento por Defecto y No Monotónico
# Tema: Clasificación de animales usando reglas por defecto
# Autor: ChatGPT
# --------------------------------------------

# Definimos una clase para representar nuestro sistema experto
class AnimalReasoner:
    def __init__(self):
        # Base de conocimientos donde almacenamos hechos conocidos
        self.facts = {}
    
    # Método para agregar un nuevo hecho (dato confirmado)
    def add_fact(self, fact, value=True):
        self.facts[fact] = value  # Guardamos el hecho como verdadero (o falso si value=False)
    
    # Método para consultar si algo es verdad en nuestra base
    def is_fact(self, fact):
        return self.facts.get(fact, False)  # Si no está, consideramos que es falso por defecto
    
    # Método principal para inferir si un animal es un "ave"
    def is_bird(self):
        # Por defecto, si el animal vuela y no sabemos que no es un ave, asumimos que es un ave
        if self.is_fact("flies") and not self.is_fact("not_bird"):
            return True
        return False  # Si no vuela o sabemos que no es un ave, no es ave
    
    # Método para inferir si el animal es un pingüino
    def is_penguin(self):
        # Si sabemos que es un pingüino, entonces es un pingüino
        return self.is_fact("penguin")
    
    # Método para inferir si el animal puede volar
    def can_fly(self):
        # Por defecto, si es un ave, asumimos que vuela
        if self.is_bird():
            # Pero si sabemos que es un pingüino, se rompe la regla (no monotónico)
            if self.is_penguin():
                return False  # Pingüinos no vuelan, anulan la inferencia por defecto
            return True  # Aves normales vuelan
        return self.is_fact("flies")  # Si no es ave, tomamos el hecho directo

# ----------------------
# Uso del sistema experto
# ----------------------

# Creamos una instancia del razonador
reasoner = AnimalReasoner()

# Agregamos el hecho de que nuestro animal vuela
reasoner.add_fact("flies")

# Primera inferencia
print("¿Es un ave?:", reasoner.is_bird())      # Esperado: True (vuela y no sabemos que no sea ave)
print("¿Puede volar?:", reasoner.can_fly())    # Esperado: True (asumimos que es un ave normal)

# Ahora agregamos un nuevo hecho: es un pingüino
reasoner.add_fact("penguin")      # Ahora sabemos algo nuevo

# Dado que es pingüino, agregamos también que no es un ave que vuela
reasoner.add_fact("not_bird")     # Contradicción que rompe la inferencia por defecto

# Segunda inferencia después de nueva información
print("\n[Después de saber que es pingüino]")
print("¿Es un ave?:", reasoner.is_bird())      # Esperado: False (porque agregamos "not_bird")
print("¿Es pingüino?:", reasoner.is_penguin()) # Esperado: True
print("¿Puede volar?:", reasoner.can_fly())    # Esperado: False (pingüinos no vuelan)
