# Implementación de Lógica No Monotónica en Python

class RazonadorNoMonotonico:
    """
    Esta clase simula un razonador no monotónico basado en reglas por defecto.
    El sistema comienza con un conjunto de hechos y reglas, y puede actualizar sus conclusiones 
    a medida que se añaden nuevos hechos.
    """
    
    def __init__(self):
        """
        Inicializa el razonador con un conjunto vacío de hechos y reglas por defecto.
        """
        self.hechos = set()  # Conjunto de hechos conocidos
        self.reglas = []     # Lista de reglas por defecto
        self.conclusiones = set()  # Conjunto de conclusiones inferidas

    def agregar_hecho(self, hecho):
        """
        Agrega un nuevo hecho al conjunto de hechos conocidos.
        
        :param hecho: Hecho que se va a agregar.
        """
        print(f"Agregando el hecho: {hecho}")
        self.hechos.add(hecho)
        self.actualizar_conclusiones()  # Recalcular las conclusiones con los nuevos hechos

    def agregar_regla(self, antecedente, consecuente, por_defecto=False):
        """
        Agrega una nueva regla al sistema. Las reglas por defecto son aplicadas 
        solo si el antecedente es conocido y no hay evidencia en contra.
        
        :param antecedente: La premisa de la regla (lo que debe ser verdadero).
        :param consecuente: La conclusión de la regla (lo que se infiere si el antecedente es verdadero).
        :param por_defecto: Indica si la regla es por defecto. Si es por defecto, 
                             la conclusión solo se aplicará si no hay evidencia en contra.
        """
        print(f"Agregando la regla: Si {antecedente}, entonces {consecuente}")
        self.reglas.append((antecedente, consecuente, por_defecto))

    def actualizar_conclusiones(self):
        """
        Actualiza el conjunto de conclusiones inferidas en función de los hechos y reglas.
        """
        nuevas_conclusiones = set()
        
        # Evaluar las reglas
        for antecedente, consecuente, por_defecto in self.reglas:
            # Verifica si el antecedente está en los hechos conocidos
            if antecedente in self.hechos:
                nuevas_conclusiones.add(consecuente)
            elif por_defecto:
                # Si la regla es por defecto, la aplicamos solo si no hay evidencia en contra
                if consecuente not in self.hechos:
                    nuevas_conclusiones.add(consecuente)
        
        # Actualiza las conclusiones
        self.conclusiones.update(nuevas_conclusiones)

    def mostrar_estado(self):
        """
        Muestra el estado actual de los hechos, conclusiones y reglas.
        """
        print("\nEstado actual:")
        print(f"Hechos conocidos: {self.hechos}")
        print(f"Reglas activas: {self.reglas}")
        print(f"Conclusiones inferidas: {self.conclusiones}")
        

# Ejemplo de uso del sistema de razonamiento no monotónico

# Inicializamos el razonador no monotónico
razonador = RazonadorNoMonotonico()

# Agregamos algunas reglas al razonador
razonador.agregar_regla("llueve", "necesito_paraguas", por_defecto=True)  # Regla por defecto
razonador.agregar_regla("hace_frio", "necesito_abrigo", por_defecto=True)  # Regla por defecto
razonador.agregar_regla("necesito_paraguas", "salgo_de_casa")  # Regla de inferencia directa

# Agregamos hechos conocidos
razonador.agregar_hecho("llueve")  # Agregamos el hecho de que está lloviendo
razonador.agregar_hecho("hace_frio")  # Agregamos el hecho de que hace frío

# Mostramos el estado actual
razonador.mostrar_estado()

# Ahora agregamos un nuevo hecho que puede contradecir las conclusiones anteriores
razonador.agregar_hecho("no_hace_frio")  # Ahora sabemos que ya no hace frío

# Mostramos el estado actualizado
razonador.mostrar_estado()
