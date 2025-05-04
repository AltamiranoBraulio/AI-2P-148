"""
SISTEMA DE GESTIÓN DE ONTOLOGÍAS MÉDICAS
---------------------------------------
Este sistema permite:
- Crear jerarquías de conceptos médicos (clases/subclases)
- Definir propiedades y relaciones entre conceptos
- Añadir individuos/instancias (ej: pacientes, enfermedades)
- Validar la consistencia de los datos
- Exportar/importar la ontología a formato JSON
"""

# Importación de módulos necesarios
from typing import Dict, List, Set, Optional, Union  # Para anotaciones de tipo
from dataclasses import dataclass, field  # Para crear clases de datos
import json  # Para manejar archivos JSON

@dataclass
class Propiedad:
    """
    Representa una propiedad en la ontología que puede ser:
    - Atributo (ej: 'edad': int)
    - Relación entre conceptos (ej: 'tieneSíntoma': 'Síntoma')
    """
    nombre: str  # Nombre de la propiedad (ej: "tieneSíntoma")
    tipo: str  # Tipo de dato ("int", "str") o clase relacionada ("Síntoma")
    cardinalidad: str  # "uno" (1:1) o "muchos" (1:N)
    inversa: Optional[str] = None  # Nombre de la propiedad inversa (opcional)

    def __str__(self):
        """Representación legible de la propiedad"""
        inversa_str = f", inversa: {self.inversa}" if self.inversa else ""
        return f"{self.nombre} ({self.tipo}, {self.cardinalidad}{inversa_str})"

@dataclass
class Concepto:
    """
    Representa un concepto/clase en la ontología (ej: 'Paciente', 'Enfermedad')
    """
    nombre: str  # Nombre del concepto
    descripcion: str = ""  # Descripción opcional
    superclases: Set[str] = field(default_factory=set)  # Clases padre (herencia)
    propiedades: Dict[str, Propiedad] = field(default_factory=dict)  # Propiedades del concepto
    individuos: Dict[str, Dict[str, Union[str, int, bool, List]]] = field(default_factory=dict)  # Instancias

    def agregar_superclase(self, superclase: str):
        """Añade una superclase (herencia)"""
        self.superclases.add(superclase)

    def agregar_propiedad(self, propiedad: Propiedad):
        """Añade una propiedad al concepto"""
        self.propiedades[propiedad.nombre] = propiedad

    def agregar_individuo(self, nombre: str, propiedades: Dict[str, Union[str, int, bool, List]]):
        """Añade una instancia/individuo al concepto"""
        self.individuos[nombre] = propiedades

    def obtener_todas_propiedades(self, ontologia: 'Ontologia') -> Dict[str, Propiedad]:
        """
        Obtiene todas las propiedades (propias + heredadas)
        ontologia: Referencia a la ontología completa para buscar superclases
        """
        todas_propiedades = self.propiedades.copy()
        
        # Recorrer superclases para heredar propiedades
        for superclase_nombre in self.superclases:
            if superclase_nombre in ontologia.conceptos:
                superclase = ontologia.conceptos[superclase_nombre]
                for prop_nombre, prop in superclase.obtener_todas_propiedades(ontologia).items():
                    if prop_nombre not in todas_propiedades:
                        todas_propiedades[prop_nombre] = prop
        
        return todas_propiedades

    def __str__(self):
        """Representación legible del concepto"""
        superclases_str = ", ".join(self.superclases) if self.superclases else "Ninguna"
        props_str = "\n    ".join(str(p) for p in self.propiedades.values())
        indiv_str = "\n    ".join(f"{n}: {p}" for n, p in self.individuos.items())
        return (f"Concepto: {self.nombre}\n"
                f"Descripción: {self.descripcion}\n"
                f"Superclases: {superclases_str}\n"
                f"Propiedades:\n    {props_str}\n"
                f"Individuos:\n    {indiv_str if indiv_str else 'Ninguno'}")

class Ontologia:
    """
    Clase principal que representa una ontología completa
    """
    def __init__(self, nombre: str, dominio: str = ""):
        self.nombre = nombre  # Nombre de la ontología
        self.dominio = dominio  # Dominio de aplicación (ej: "Medicina")
        self.conceptos: Dict[str, Concepto] = {}  # Diccionario de conceptos
        self.propiedades: Dict[str, Propiedad] = {}  # Propiedades globales

    def agregar_concepto(self, concepto: Concepto):
        """Añade un concepto a la ontología"""
        self.conceptos[concepto.nombre] = concepto

    def existe_concepto(self, nombre_concepto: str) -> bool:
        """Verifica si un concepto existe"""
        return nombre_concepto in self.conceptos

    def obtener_subclases(self, nombre_concepto: str) -> List[str]:
        """Obtiene subclases directas de un concepto"""
        return [nombre for nombre, concepto in self.conceptos.items() 
                if nombre_concepto in concepto.superclases]

    def obtener_todas_subclases(self, nombre_concepto: str) -> Set[str]:
        """Obtiene todas las subclases (directas e indirectas)"""
        subclases = set()
        for subclase_nombre in self.obtener_subclases(nombre_concepto):
            subclases.add(subclase_nombre)
            subclases.update(self.obtener_todas_subclases(subclase_nombre))
        return subclases

    def inferir_tipo(self, individuo_nombre: str) -> List[str]:
        """Infiere los tipos de un individuo basado en sus propiedades"""
        return [nombre for nombre, concepto in self.conceptos.items() 
                if individuo_nombre in concepto.individuos]

    def validar_individuo(self, individuo_nombre: str) -> List[str]:
        """Valida si un individuo cumple con las restricciones de la ontología"""
        errores = []
        tipos = self.inferir_tipo(individuo_nombre)
        
        if not tipos:
            return [f"Individuo {individuo_nombre} no encontrado"]
        
        for tipo in tipos:
            concepto = self.conceptos[tipo]
            individuo = concepto.individuos[individuo_nombre]
            propiedades = concepto.obtener_todas_propiedades(self)
            
            for prop_nombre, prop in propiedades.items():
                if prop_nombre not in individuo:
                    if prop.cardinalidad == "uno":
                        errores.append(f"Falta propiedad obligatoria: {prop_nombre}")
                    continue
                
                valor = individuo[prop_nombre]
                
                # Validar tipo de dato
                if prop.tipo in ["int", "str", "bool"]:
                    if not isinstance(valor, eval(prop.tipo)):
                        errores.append(f"Tipo incorrecto en {prop_nombre}: esperado {prop.tipo}")
                elif prop.tipo in self.conceptos:  # Es relación
                    if prop.cardinalidad == "uno":
                        if not self.existe_concepto(valor):
                            errores.append(f"Relación inválida: {prop_nombre} -> {valor}")
                    else:  # "muchos"
                        for item in valor:
                            if not self.existe_concepto(item):
                                errores.append(f"Relación inválida: {prop_nombre} -> {item}")
        
        return errores

    def exportar_json(self, archivo: str):
        """Exporta la ontología a un archivo JSON"""
        datos = {
            "nombre": self.nombre,
            "dominio": self.dominio,
            "conceptos": {
                nombre: {
                    "descripcion": c.descripcion,
                    "superclases": list(c.superclases),
                    "propiedades": {n: {"tipo": p.tipo, "cardinalidad": p.cardinalidad, "inversa": p.inversa} 
                                   for n, p in c.propiedades.items()},
                    "individuos": c.individuos
                } for nombre, c in self.conceptos.items()
            },
            "propiedades_globales": {
                n: {"tipo": p.tipo, "cardinalidad": p.cardinalidad, "inversa": p.inversa}
                for n, p in self.propiedades.items()
            }
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @classmethod
    def cargar_json(cls, archivo: str) -> 'Ontologia':
        """Carga una ontología desde un archivo JSON"""
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        ontologia = cls(datos["nombre"], datos["dominio"])
        
        # Crear conceptos básicos
        for nombre, info in datos["conceptos"].items():
            ontologia.agregar_concepto(Concepto(nombre, info["descripcion"]))
        
        # Añadir superclases y propiedades
        for nombre, info in datos["conceptos"].items():
            concepto = ontologia.conceptos[nombre]
            for superclase in info["superclases"]:
                concepto.agregar_superclase(superclase)
            
            for prop_nombre, prop_info in info["propiedades"].items():
                concepto.agregar_propiedad(Propiedad(
                    prop_nombre, prop_info["tipo"], prop_info["cardinalidad"], prop_info["inversa"]
                ))
            
            for ind_nombre, ind_props in info["individuos"].items():
                concepto.agregar_individuo(ind_nombre, ind_props)
        
        # Añadir propiedades globales
        for prop_nombre, prop_info in datos["propiedades_globales"].items():
            ontologia.propiedades[prop_nombre] = Propiedad(
                prop_nombre, prop_info["tipo"], prop_info["cardinalidad"], prop_info["inversa"]
            )
        
        return ontologia

    def __str__(self):
        """Representación legible de la ontología"""
        conceptos_str = "\n\n".join(str(c) for c in self.conceptos.values())
        return (f"Ontología: {self.nombre}\n"
                f"Dominio: {self.dominio}\n"
                f"Conceptos ({len(self.conceptos)}):\n{conceptos_str}")

# ---------------------------------------------------------------
# Ejemplo: Ontología Médica
# ---------------------------------------------------------------

def crear_ontologia_medica() -> Ontologia:
    """Crea y configura una ontología médica de ejemplo"""
    ontologia = Ontologia("Ontología Médica", "Diagnóstico de enfermedades")
    
    # Definir conceptos
    paciente = Concepto("Paciente", "Persona que recibe atención médica")
    sintoma = Concepto("Síntoma", "Manifestación clínica")
    enfermedad = Concepto("Enfermedad", "Condición médica anormal")
    tratamiento = Concepto("Tratamiento", "Intervención terapéutica")
    
    # Conceptos especializados
    enfermedad_infecciosa = Concepto("EnfermedadInfecciosa", "Causada por patógenos", {"Enfermedad"})
    virus = Concepto("Virus", "Agente infeccioso microscópico")
    
    # Propiedades
    tiene_sintoma = Propiedad("tieneSíntoma", "Síntoma", "muchos")
    tiene_tratamiento = Propiedad("tieneTratamiento", "Tratamiento", "muchos")
    causado_por = Propiedad("causadoPor", "Virus", "muchos")
    
    # Asignar propiedades
    paciente.agregar_propiedad(tiene_sintoma)
    enfermedad.agregar_propiedad(tiene_tratamiento)
    enfermedad_infecciosa.agregar_propiedad(causado_por)
    
    # Añadir a la ontología
    for concepto in [paciente, sintoma, enfermedad, tratamiento, enfermedad_infecciosa, virus]:
        ontologia.agregar_concepto(concepto)
    
    # Crear individuos/instancias
    sintoma.agregar_individuo("fiebre", {"intensidad": "alta"})
    sintoma.agregar_individuo("tos", {"intensidad": "moderada"})
    
    virus.agregar_individuo("influenza", {"familia": "Orthomyxoviridae"})
    
    enfermedad_infecciosa.agregar_individuo("gripe", {
        "tieneTratamiento": ["reposo", "antiviral"],
        "causadoPor": ["influenza"]
    })
    
    tratamiento.agregar_individuo("reposo", {})
    tratamiento.agregar_individuo("antiviral", {"tipo": "oseltamivir"})
    
    return ontologia

# ---------------------------------------------------------------
# Ejecución de demostración
# ---------------------------------------------------------------

if __name__ == "__main__":
    # Crear y mostrar la ontología
    ontologia = crear_ontologia_medica()
    print(ontologia)
    
    # Exportar a JSON
    ontologia.exportar_json("ontologia_medica.json")
    print("\nOntología exportada a 'ontologia_medica.json'")
    
    # Ejemplo de validación
    print("\nValidando individuo 'gripe':")
    errores = ontologia.validar_individuo("gripe")
    print("Errores encontrados:" if errores else "El individuo es válido")
    for error in errores:
        print(f"- {error}")