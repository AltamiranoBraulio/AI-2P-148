# Importamos el módulo random para generar elecciones aleatorias basadas en probabilidades
import random
# Importamos defaultdict de collections para crear diccionarios con valores por defecto
from collections import defaultdict

class EvolucionLenguajeMarkov:
    def __init__(self, palabra_inicial):
        """
        Constructor de la clase. Inicializa el simulador de evolución lingüística.
        
        Args:
            palabra_inicial (str): La palabra ancestral que servirá como punto de partida
                                   para la simulación de evolución.
        """
        # Convertimos la palabra inicial a minúsculas para uniformidad en el procesamiento
        self.palabra_actual = palabra_inicial.lower()
        
        # Inicializamos el historial de evolución con la palabra inicial
        self.historial = [self.palabra_actual]
        
        # Definimos las reglas de transición fonética como un diccionario de diccionarios:
        # - La clave exterior es el fonema actual
        # - El valor es otro diccionario donde:
        #   - Claves: posibles fonemas resultantes
        #   - Valores: probabilidades de transición (deben sumar ~1.0)
        self.reglas_transicion = {
            # Consonantes bilabiales y sus posibles cambios
            'b': {'p': 0.3, 'v': 0.4, 'b': 0.3},  # 'b' puede cambiar a 'p' (30%), 'v' (40%) o permanecer (30%)
            'p': {'b': 0.3, 'f': 0.2, 'p': 0.5},  # 'p' puede cambiar a 'b' (30%), 'f' (20%) o permanecer (50%)
            'v': {'b': 0.4, 'f': 0.3, 'v': 0.3},  # 'v' puede cambiar a 'b' (40%), 'f' (30%) o permanecer (30%)
            'f': {'p': 0.3, 'v': 0.2, 'f': 0.5},  # 'f' puede cambiar a 'p' (30%), 'v' (20%) o permanecer (50%)
            
            # Consonantes dentales y sus cambios
            'd': {'t': 0.4, 'd': 0.6},  # 'd' puede cambiar a 't' (40%) o permanecer (60%)
            't': {'d': 0.3, 's': 0.2, 't': 0.5},  # 't' puede cambiar a 'd' (30%), 's' (20%) o permanecer (50%)
            
            # Vocales y sus transformaciones
            'a': {'e': 0.3, 'o': 0.2, 'a': 0.5},  # 'a' puede cambiar a 'e' (30%), 'o' (20%) o permanecer (50%)
            'e': {'i': 0.3, 'a': 0.2, 'e': 0.5},  # 'e' puede cambiar a 'i' (30%), 'a' (20%) o permanecer (50%)
            'i': {'e': 0.4, 'i': 0.6},  # 'i' puede cambiar a 'e' (40%) o permanecer (60%)
            'o': {'u': 0.3, 'o': 0.7},  # 'o' puede cambiar a 'u' (30%) o permanecer (70%)
            'u': {'o': 0.4, 'u': 0.6},  # 'u' puede cambiar a 'o' (40%) o permanecer (60%)
            
            # Caracteres especiales que no cambian
            ' ': {' ': 1.0},  # El espacio siempre se mantiene
            "'": {"'": 1.0},  # El apóstrofe siempre se mantiene
            '-': {'-': 1.0}   # El guión siempre se mantiene
        }
        
        # Conjunto de caracteres que nunca deben cambiar durante la evolución
        self.caracteres_inmutables = {' ', "'", '-', '.', ','}

    def _aplicar_cambio_markoviano(self, caracter):
        """
        Aplica la hipótesis de Markov para evolucionar un solo caracter.
        La evolución depende SOLO del caracter actual (propiedad markoviana).
        
        Args:
            caracter (str): El caracter a evolucionar.
            
        Returns:
            str: El caracter evolucionado según las reglas de transición.
        """
        # Si el caracter está en los inmutables, lo devolvemos sin cambios
        if caracter in self.caracteres_inmutables:
            return caracter
            
        # Verificamos si el caracter tiene reglas de transición definidas
        if caracter in self.reglas_transicion:
            # Obtenemos las posibles opciones de evolución
            opciones = list(self.reglas_transicion[caracter].keys())
            # Obtenemos los pesos (probabilidades) asociados a cada opción
            pesos = list(self.reglas_transicion[caracter].values())
            # Usamos random.choices para seleccionar una opción basada en los pesos
            return random.choices(opciones, weights=pesos)[0]
        else:
            # Si no hay reglas definidas, el caracter permanece igual
            return caracter

    def evolucionar_palabra(self, generaciones=1):
        """
        Evoluciona la palabra a través de una o más generaciones lingüísticas.
        
        Args:
            generaciones (int): Número de veces que se aplicará el proceso evolutivo.
        """
        # Iteramos para cada generación solicitada
        for _ in range(generaciones):
            # Lista para almacenar la nueva palabra evolucionada
            nueva_palabra = []
            
            # Procesamos cada letra de la palabra actual
            for letra in self.palabra_actual:
                # Aplicamos el cambio markoviano a la letra
                nueva_letra = self._aplicar_cambio_markoviano(letra)
                # Añadimos la letra evolucionada a la nueva palabra
                nueva_palabra.append(nueva_letra)
            
            # Unimos las letras para formar la nueva palabra
            self.palabra_actual = ''.join(nueva_palabra)
            # Añadimos la nueva palabra al historial de evolución
            self.historial.append(self.palabra_actual)

    def mostrar_historial(self):
        """Muestra el historial completo de evolución de la palabra."""
        print("\nEvolución de la palabra:")
        # Iteramos sobre cada generación en el historial
        for i, palabra in enumerate(self.historial):
            # Mostramos el número de generación y la palabra correspondiente
            print(f"Generación {i}: {palabra}")

    def simular_evolucion(self, generaciones=10):
        """
        Ejecuta y muestra una simulación completa de evolución lingüística.
        
        Args:
            generaciones (int): Número total de generaciones a simular.
        """
        # Mostramos el encabezado de la simulación
        print(f"\n🔠 Simulador de Evolución Lingüística (Procesos de Markov)")
        print(f"Palabra ancestral: '{self.historial[0]}'")
        print("=" * 50)
        
        # Iteramos a través de cada generación
        for gen in range(1, generaciones + 1):
            # Aplicamos una generación de evolución
            self.evolucionar_palabra()
            
            # Mostramos el resultado cada 2 generaciones o en la última
            if gen % 2 == 0 or gen == generaciones:
                print(f"Gen {gen}: {self.palabra_actual}")
        
        # Mostramos el resumen completo al final
        print("\n🔍 Resumen de cambios:")
        self.mostrar_historial()

# Ejemplo de uso con palabras protoindoeuropeas reconstruidas
if __name__ == "__main__":
    # Lista de palabras ancestrales hipotéticas
    palabras_ancestrales = [
        "bhrater",  # hermano (protoindoeuropeo reconstruido)
        "ped",      # pie
        "wed",      # agua
        "kwon",     # perro
        "dwo",      # dos
        "treyes",   # tres
        "mehter",   # madre
        "swesor"    # hermana
    ]
    
    # Seleccionamos una palabra inicial aleatoria
    palabra_inicial = random.choice(palabras_ancestrales)
    
    # Creamos una instancia del simulador con la palabra inicial
    simulador = EvolucionLenguajeMarkov(palabra_inicial)
    
    # Ejecutamos la simulación por 12 generaciones
    simulador.simular_evolucion(generaciones=12)