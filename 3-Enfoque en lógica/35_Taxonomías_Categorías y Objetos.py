# 🚀 Taxonomías: Categorías y Objetos
# 👑 Autor: ChatGPT para Babyarm
# 📚 Objetivo: Crear y manipular una taxonomía de animales usando categorías y objetos.

# ✅ Creamos una clase general llamada "Categoria"
class Categoria:
    # 🔥 El constructor (__init__) recibe el nombre de la categoría y opcionalmente su categoría padre.
    def __init__(self, nombre, padre=None):
        self.nombre = nombre  # 📝 Guardamos el nombre de la categoría (ejemplo: "Mamífero")
        self.padre = padre    # 📝 Guardamos la categoría padre (ejemplo: "Animal")

    # ✅ Método para obtener la lista de categorías desde la más específica hasta la raíz
    def obtener_taxonomia(self):
        # 🚀 Si tiene padre, devuelve la lista concatenando la propia categoría con las de su padre
        if self.padre:
            return [self.nombre] + self.padre.obtener_taxonomia()
        else:
            # 🏁 Si no tiene padre, es la raíz
            return [self.nombre]

    # ✅ Método para mostrar la jerarquía completa
    def mostrar_taxonomia(self):
        print(f"🔎 Taxonomía para {self.nombre}: {' ➔ '.join(self.obtener_taxonomia())}")

# ✅ Clase para representar un Objeto que pertenece a una categoría
class Objeto:
    # 🔥 Constructor recibe el nombre del objeto y su categoría asociada
    def __init__(self, nombre, categoria):
        self.nombre = nombre          # 📝 Nombre del objeto (ejemplo: "León")
        self.categoria = categoria    # 📝 La categoría a la que pertenece (ejemplo: "Mamífero")

    # ✅ Método para mostrar a qué categorías pertenece este objeto
    def mostrar_clasificacion(self):
        print(f"🦁 Objeto: {self.nombre}")
        print(f"📚 Clasificación: {' ➔ '.join(self.categoria.obtener_taxonomia())}")

# === 🚀 DEFINIMOS NUESTRAS CATEGORÍAS ===

# 🟢 Categoría raíz
animal = Categoria("Animal")  # "Animal" es la categoría más general

# 🔵 Subcategorías directas de "Animal"
mamifero = Categoria("Mamífero", animal)  # "Mamífero" es hijo de "Animal"
ave = Categoria("Ave", animal)           # "Ave" es hijo de "Animal"

# 🟣 Subcategorías más específicas
felino = Categoria("Felino", mamifero)   # "Felino" es un tipo de "Mamífero"
canino = Categoria("Canino", mamifero)   # "Canino" es otro tipo de "Mamífero"
rapaz = Categoria("Ave rapaz", ave)      # "Ave rapaz" es tipo de "Ave"

# === 🚀 DEFINIMOS OBJETOS ===

# 🦁 Un león es un "Felino"
leon = Objeto("León", felino)

# 🐺 Un lobo es un "Canino"
lobo = Objeto("Lobo", canino)

# 🦅 Un águila es un "Ave rapaz"
aguila = Objeto("Águila", rapaz)

# === 🚀 MOSTRAMOS LA TAXONOMÍA DE LAS CATEGORÍAS ===

# 🔎 Mostramos cómo están organizadas las categorías
animal.mostrar_taxonomia()   # Muestra solo "Animal"
mamifero.mostrar_taxonomia() # Muestra "Mamífero ➔ Animal"
felino.mostrar_taxonomia()   # Muestra "Felino ➔ Mamífero ➔ Animal"

# === 🚀 MOSTRAMOS CLASIFICACIÓN DE LOS OBJETOS ===

# 🦁 Clasificación completa del león
leon.mostrar_clasificacion()  # Debería mostrar: León ➔ Felino ➔ Mamífero ➔ Animal

# 🐺 Clasificación del lobo
lobo.mostrar_clasificacion()

# 🦅 Clasificación del águila
aguila.mostrar_clasificacion()
