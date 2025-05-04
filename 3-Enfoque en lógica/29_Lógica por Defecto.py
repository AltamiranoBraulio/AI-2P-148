"""
Sistema de Lógica por Defecto que implementa:
- Reglas con conclusiones por defecto
- Mecanismo de justificación de creencias
- Soporte para excepciones
- Jerarquía de reglas por especificidad
"""

class Hecho:
    """
    Representa un hecho en la base de conocimiento, que puede ser:
    - Un hecho positivo (afirmación)
    - Un hecho negativo (negación)
    - Un hecho por defecto (asumido a menos que se pruebe lo contrario)
    """
    def __init__(self, nombre, valor=None, por_defecto=False, justificacion=None):
        self.nombre = nombre  # Nombre del hecho (ej: "vuela")
        self.valor = valor  # Valor actual (True/False/None)
        self.por_defecto = por_defecto  # Si es una presunción por defecto
        self.justificacion = justificacion  # Reglas que lo justifican
        self.excepciones = set()  # Hechos que pueden invalidarlo

    def agregar_excepcion(self, excepcion):
        """Añade una excepción a este hecho"""
        self.excepciones.add(excepcion)

    def __str__(self):
        estado = "Positivo" if self.valor else "Negativo" if self.valor is False else "Desconocido"
        return f"{self.nombre}: {estado} {'(por defecto)' if self.por_defecto else ''}"


class ReglaPorDefecto:
    """
    Representa una regla con conclusiones por defecto de la forma:
    Si [premisas] y no hay excepciones, entonces [conclusiones] (por defecto)
    """
    def __init__(self, nombre, premisas, conclusiones, excepciones=None, especificidad=0):
        self.nombre = nombre  # Identificador de la regla
        self.premisas = premisas  # Lista de premisas requeridas
        self.conclusiones = conclusiones  # Hechos que concluye
        self.excepciones = excepciones if excepciones else []  # Condiciones que invalidan la regla
        self.especificidad = especificidad  # Nivel de especificidad (para resolver conflictos)

    def puede_aplicar(self, hechos):
        """Verifica si la regla puede aplicarse dados los hechos conocidos"""
        # Verificar que todas las premisas sean verdaderas
        premisas_cumplidas = all(
            any(h.nombre == p and h.valor for h in hechos.values()) 
            for p in self.premisas
        )
        
        # Verificar que no haya excepciones aplicables
        excepciones_aplicables = any(
            any(h.nombre == e and h.valor for h in hechos.values()) 
            for e in self.excepciones
        )
        
        return premisas_cumplidas and not excepciones_aplicables

    def __str__(self):
        return f"{self.nombre}: Si {', '.join(self.premisas)} y no {', '.join(self.excepciones)} entonces {', '.join(self.conclusiones)} (por defecto)"


class MotorPorDefecto:
    """
    Motor de razonamiento por defecto que:
    - Mantiene una base de hechos
    - Aplica reglas por defecto
    - Maneja excepciones
    - Resuelve conflictos por especificidad
    """
    def __init__(self):
        self.hechos = {}  # Diccionario de hechos por nombre
        self.reglas = []  # Lista de reglas por defecto
        self.registro = []  # Historial de inferencias

    def agregar_hecho(self, hecho):
        """Añade un hecho a la base de conocimiento"""
        self.hechos[hecho.nombre] = hecho

    def agregar_regla(self, regla):
        """Añade una regla al sistema"""
        self.reglas.append(regla)
        # Ordenar reglas por especificidad (mayor primero)
        self.reglas.sort(key=lambda r: r.especificidad, reverse=True)

    def evaluar_hecho(self, nombre_hecho):
        """Evalúa un hecho considerando razonamiento por defecto"""
        # Si el hecho ya está determinado, retornar su valor
        if nombre_hecho in self.hechos and self.hechos[nombre_hecho].valor is not None:
            return self.hechos[nombre_hecho].valor
        
        # Buscar reglas aplicables que concluyan este hecho
        reglas_aplicables = [
            r for r in self.reglas 
            if nombre_hecho in r.conclusiones and r.puede_aplicar(self.hechos)
        ]
        
        # Si hay reglas aplicables, usar la más específica (ya están ordenadas)
        if reglas_aplicables:
            regla_elegida = reglas_aplicables[0]
            
            # Verificar si hay excepciones más específicas
            for regla in reglas_aplicables[1:]:
                if regla.especificidad > regla_elegida.especificidad:
                    regla_elegida = regla
            
            # Aplicar la regla (asumir el hecho por defecto)
            hecho = Hecho(
                nombre_hecho, 
                valor=True, 
                por_defecto=True, 
                justificacion=regla_elegida.nombre
            )
            
            # Registrar la inferencia
            self.registro.append(f"Inferido por defecto: {nombre_hecho} (por {regla_elegida.nombre})")
            
            # Añadir excepciones de la regla al hecho
            for excepcion in regla_elegida.excepciones:
                hecho.agregar_excepcion(excepcion)
            
            self.agregar_hecho(hecho)
            return True
        
        # Si no hay reglas aplicables, el hecho es desconocido
        return None

    def verificar_consistencia(self, nombre_hecho):
        """Verifica si un hecho por defecto sigue siendo válido"""
        if nombre_hecho in self.hechos and self.hechos[nombre_hecho].por_defecto:
            # Verificar si alguna excepción se ha hecho verdadera
            for excepcion in self.hechos[nombre_hecho].excepciones:
                if excepcion in self.hechos and self.hechos[excepcion].valor:
                    # La excepción se cumple, retractar el hecho por defecto
                    self.registro.append(f"Retractado: {nombre_hecho} por excepción {excepcion}")
                    self.hechos[nombre_hecho].valor = False
                    self.hechos[nombre_hecho].justificacion = f"Excepción: {excepcion}"
                    return False
        return True

    def consultar(self, nombre_hecho):
        """Consulta el valor de un hecho con razonamiento por defecto"""
        # Primero evaluar el hecho
        self.evaluar_hecho(nombre_hecho)
        
        # Luego verificar consistencia
        self.verificar_consistencia(nombre_hecho)
        
        # Retornar el estado actual
        if nombre_hecho in self.hechos:
            return self.hechos[nombre_hecho].valor
        return None

    def __str__(self):
        """Muestra el estado actual del sistema"""
        resultado = []
        resultado.append("\nBase de Hechos:")
        for hecho in self.hechos.values():
            resultado.append(f" - {hecho}")
        
        resultado.append("\nReglas por Defecto:")
        for regla in self.reglas:
            resultado.append(f" - {regla}")
        
        resultado.append("\nRegistro de Inferencias:")
        for entrada in self.registro[-5:]:  # Mostrar solo las últimas 5
            resultado.append(f" - {entrada}")
        
        return "\n".join(resultado)


# ---------------------------------------------------------------
# Ejemplo: Sistema de Diagnóstico Médico con Razonamiento por Defecto
# ---------------------------------------------------------------

def configurar_sistema_diagnostico():
    """Configura un sistema de diagnóstico médico con reglas por defecto"""
    sistema = MotorPorDefecto()
    
    # Hechos básicos (no por defecto)
    sistema.agregar_hecho(Hecho("fiebre", valor=False))
    sistema.agregar_hecho(Hecho("tos", valor=False))
    sistema.agregar_hecho(Hecho("dolor_cabeza", valor=False))
    sistema.agregar_hecho(Hecho("contacto_covid", valor=False))
    sistema.agregar_hecho(Hecho("test_covid_positivo", valor=False))
    sistema.agregar_hecho(Hecho("vacunado", valor=False))
    
    # Reglas por defecto para diagnóstico
    sistema.agregar_regla(ReglaPorDefecto(
        nombre="R1",
        premisas=["fiebre", "tos"],
        conclusiones=["gripe"],
        excepciones=["test_covid_positivo"],
        especificidad=1
    ))
    
    sistema.agregar_regla(ReglaPorDefecto(
        nombre="R2",
        premisas=["fiebre", "tos", "contacto_covid"],
        conclusiones=["covid"],
        excepciones=["test_covid_negativo"],
        especificidad=2  # Más específica que R1
    ))
    
    sistema.agregar_regla(ReglaPorDefecto(
        nombre="R3",
        premisas=["vacunado"],
        conclusiones=["protegido"],
        excepciones=["variante_nueva"],
        especificidad=1
    ))
    
    # Regla por defecto sobre tratamiento
    sistema.agregar_regla(ReglaPorDefecto(
        nombre="R4",
        premisas=["gripe"],
        conclusiones=["tratamiento_antiviral"],
        excepciones=["alergia_antivirales"],
        especificidad=1
    ))
    
    return sistema


def demostracion_diagnostico():
    """Demuestra el sistema de diagnóstico médico con razonamiento por defecto"""
    print("\nSISTEMA DE DIAGNÓSTICO MÉDICO CON LÓGICA POR DEFECTO")
    print("---------------------------------------------------")
    
    sistema = configurar_sistema_diagnostico()
    
    # Caso 1: Síntomas de gripe sin excepciones
    print("\nCaso 1: Paciente con fiebre y tos")
    sistema.hechos["fiebre"].valor = True
    sistema.hechos["tos"].valor = True
    
    print("\nEstado inicial:")
    print(sistema)
    
    print("\nConsultando diagnóstico...")
    diagnostico = sistema.consultar("gripe")
    print(f"¿Tiene gripe? {diagnostico}")
    
    print("\nConsultando tratamiento...")
    tratamiento = sistema.consultar("tratamiento_antiviral")
    print(f"¿Necesita antiviral? {tratamiento}")
    
    print("\nEstado después de las consultas:")
    print(sistema)
    
    # Caso 2: Añadiendo una excepción (contacto con COVID)
    print("\nCaso 2: Mismo paciente tuvo contacto con COVID")
    sistema.hechos["contacto_covid"].valor = True
    
    print("\nConsultando diagnóstico...")
    diagnostico = sistema.consultar("gripe")
    covid = sistema.consultar("covid")
    print(f"¿Tiene gripe? {diagnostico}")
    print(f"¿Tiene COVID? {covid}")
    
    print("\nEstado después de las consultas:")
    print(sistema)
    
    # Caso 3: Añadiendo información que invalida el diagnóstico por defecto
    print("\nCaso 3: Resultado de test COVID positivo")
    sistema.hechos["test_covid_positivo"].valor = True
    
    print("\nConsultando diagnóstico...")
    diagnostico = sistema.consultar("gripe")
    covid = sistema.consultar("covid")
    print(f"¿Tiene gripe? {diagnostico}")
    print(f"¿Tiene COVID? {covid}")
    
    print("\nEstado final:")
    print(sistema)


# ---------------------------------------------------------------
# Interfaz interactiva para experimentar con el sistema
# ---------------------------------------------------------------

def interfaz_interactiva():
    """Interfaz para interactuar con el sistema de lógica por defecto"""
    sistema = configurar_sistema_diagnostico()
    
    while True:
        print("\nOpciones:")
        print("1. Mostrar estado del sistema")
        print("2. Establecer síntoma (fiebre/tos/dolor_cabeza)")
        print("3. Establecer condición (contacto_covid/vacunado)")
        print("4. Establecer resultado de test (test_covid_positivo)")
        print("5. Consultar diagnóstico")
        print("6. Reiniciar sistema")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print(sistema)
            
        elif opcion == "2":
            sintoma = input("¿Qué síntoma? (fiebre/tos/dolor_cabeza): ")
            valor = input("¿Valor? (True/False): ").lower() == "true"
            if sintoma in sistema.hechos:
                sistema.hechos[sintoma].valor = valor
                print(f"{sintoma} establecido a {valor}")
            else:
                print("Síntoma no válido")
                
        elif opcion == "3":
            condicion = input("¿Qué condición? (contacto_covid/vacunado): ")
            valor = input("¿Valor? (True/False): ").lower() == "true"
            if condicion in sistema.hechos:
                sistema.hechos[condicion].valor = valor
                print(f"{condicion} establecido a {valor}")
            else:
                print("Condición no válida")
                
        elif opcion == "4":
            test = input("¿Test COVID positivo? (True/False): ").lower() == "true"
            sistema.hechos["test_covid_positivo"].valor = test
            print(f"Test COVID positivo establecido a {test}")
            
        elif opcion == "5":
            print("\nConsultando diagnóstico...")
            gripe = sistema.consultar("gripe")
            covid = sistema.consultar("covid")
            tratamiento = sistema.consultar("tratamiento_antiviral")
            
            print(f"\nResultados:")
            print(f" - Gripe: {gripe}")
            print(f" - COVID: {covid}")
            print(f" - Tratamiento antiviral recomendado: {tratamiento}")
            
        elif opcion == "6":
            sistema = configurar_sistema_diagnostico()
            print("Sistema reiniciado")
            
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
            
        else:
            print("Opción no válida")


if __name__ == "__main__":
    # Ejecutar demostración automática
    demostracion_diagnostico()
    
    # Opcional: Ejecutar interfaz interactiva
    # interfaz_interactiva()