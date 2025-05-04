# 👨‍💻 Agente Lógico Simple
# Un agente que utiliza inferencia lógica para tomar decisiones.
# Autor: ChatGPT para Babyarm 👑

# 📚 Definimos una clase para representar el Agente Lógico
class AgenteLogico:
    """
    Esta clase representa un Agente Lógico que tiene una base de conocimientos
    con hechos y reglas. El agente puede hacer inferencias utilizando encadenamiento hacia adelante.
    """

    def __init__(self, hechos_iniciales, reglas):
        """
        El constructor de la clase recibe los hechos iniciales y las reglas lógicas.

        :param hechos_iniciales: Un conjunto de hechos conocidos por el agente.
        :param reglas: Un conjunto de reglas lógicas que definen cómo el agente infiere nuevos hechos.
        """
        self.hechos = hechos_iniciales  # Conjunto de hechos que el agente conoce
        self.reglas = reglas  # Conjunto de reglas lógicas del agente

    def encadenamiento_adelante(self):
        """
        Esta función realiza el encadenamiento hacia adelante para inferir nuevos hechos
        utilizando las reglas y los hechos actuales del agente.

        El encadenamiento hacia adelante sigue las reglas y, cuando se aplican, agrega
        nuevos hechos a la base de conocimientos.
        """
        # Creamos una copia de los hechos actuales para no modificar el conjunto original
        nuevos_hechos = self.hechos.copy()
        aplicado = True

        # Continuamos aplicando reglas mientras haya hechos nuevos que agregar
        while aplicado:
            aplicado = False
            # Revisamos todas las reglas
            for premisas, conclusion in self.reglas:
                # Verificamos si todas las premisas de la regla están en los hechos conocidos
                if all(p in nuevos_hechos for p in premisas):
                    # Si la conclusión no está ya en los hechos, la agregamos
                    if conclusion not in nuevos_hechos:
                        print(f"✅ Regla aplicada: {premisas} ➡️ {conclusion}")
                        nuevos_hechos.add(conclusion)
                        aplicado = True  # Indicamos que se aplicó una regla
        # Actualizamos los hechos con los nuevos hechos inferidos
        self.hechos = nuevos_hechos
        print("🏁 Hechos finales del agente:", nuevos_hechos)

    def hacer_diagnostico(self):
        """
        Esta función simula el diagnóstico del agente basándose en los hechos inferidos.
        Después de ejecutar el encadenamiento hacia adelante, el agente toma decisiones lógicas.
        """
        print("\n🧠 Realizando diagnóstico del agente...")
        self.encadenamiento_adelante()  # Inferimos hechos utilizando el encadenamiento hacia adelante
        # En función de los hechos inferidos, el agente puede tomar decisiones.
        if 'necesita_antibiotico' in self.hechos:
            print("💊 Diagnóstico: El agente necesita antibiótico.")
        elif 'necesita_descanso' in self.hechos:
            print("🛌 Diagnóstico: El agente necesita descanso.")
        else:
            print("🤖 Diagnóstico: No se requiere tratamiento.")

    def recibir_nuevos_hechos(self, nuevos_hechos):
        """
        Esta función permite que el agente reciba nuevos hechos externos, los cuales
        se agregarán a la base de conocimientos del agente.

        :param nuevos_hechos: Un conjunto de hechos adicionales que el agente puede conocer.
        """
        print(f"\n📥 Nuevos hechos recibidos: {nuevos_hechos}")
        self.hechos.update(nuevos_hechos)  # Agregamos los nuevos hechos a la base de conocimientos
        print("🔄 Base de conocimientos actualizada.")

    def mostrar_hechos(self):
        """
        Muestra los hechos actuales en la base de conocimientos del agente.
        """
        print(f"\n📜 Hechos actuales del agente: {self.hechos}")


# 🧪 Ejemplo de uso del Agente Lógico

# 🔧 Definimos los hechos iniciales conocidos por el agente
hechos_iniciales = {'tiene_fiebre', 'tiene_dolor_garganta', 'tiene_tos'}

# 📝 Definimos las reglas lógicas que el agente usará para inferir nuevos hechos
reglas = [
    (['tiene_fiebre', 'tiene_dolor_garganta'], 'tiene_infeccion'),  # Si tiene fiebre y dolor de garganta, tiene una infección
    (['tiene_tos', 'tiene_fiebre'], 'tiene_gripe'),  # Si tiene tos y fiebre, tiene gripe
    (['tiene_infeccion'], 'necesita_antibiotico'),  # Si tiene infección, necesita antibiótico
    (['tiene_gripe'], 'necesita_descanso'),  # Si tiene gripe, necesita descanso
    (['tiene_gripe', 'tiene_infeccion'], 'caso_severo')  # Si tiene gripe e infección, el caso es severo
]

# 🧑‍💻 Creamos una instancia del Agente Lógico con los hechos iniciales y las reglas
agente = AgenteLogico(hechos_iniciales, reglas)

# 🧠 El agente realiza un diagnóstico basándose en los hechos y reglas
agente.hacer_diagnostico()

# 💥 El agente recibe nuevos hechos
nuevos_hechos = {'tiene_fatiga', 'tiene_dificultad_respiratoria'}
agente.recibir_nuevos_hechos(nuevos_hechos)

# 📜 Mostramos los hechos actuales del agente después de recibir nuevos hechos
agente.mostrar_hechos()

# 🧠 El agente realiza el diagnóstico nuevamente con los hechos actualizados
agente.hacer_diagnostico()
