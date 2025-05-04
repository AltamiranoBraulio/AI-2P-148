"""
SISTEMA DE MODELADO DE CREENCIAS Y OBJETOS MENTALES
--------------------------------------------------
Este sistema permite:
- Representar creencias de agentes (personas, IA)
- Modelar relaciones entre creencias, evidencias y fuentes
- Rastrear cambios en creencias a lo largo del tiempo
- Evaluar consistencia entre conjuntos de creencias
- Simular procesos de actualización de creencias
"""

from typing import Dict, List, Optional, Set, Union
from dataclass import dataclass, field
from enum import Enum, auto
from datetime import datetime
import json

# ==================== ENUMERACIONES BÁSICAS ====================
class GradoCertidumbre(Enum):
    """Niveles de certeza en una creencia"""
    DESCONOCIDO = 0     # No hay información
    DUDA_EXTREMA = 1    # 1-20% de certeza
    DUDA_MODERADA = 2   # 21-40%
    POSIBLE = 3         # 41-60%
    PROBABLE = 4        # 61-80%
    SEGURO = 5          # 81-100%

class TipoFuente(Enum):
    """Tipos de fuentes que originan creencias"""
    PERCEPCION = auto()     # Información sensorial directa
    TESTIMONIO = auto()     # Información de otros agentes
    INFERENCIA = auto()     # Derivada de razonamiento
    MEMORIA = auto()        # Recuperada de experiencias pasadas
    INTUICION = auto()      # Sin fuente explícita

# ==================== ESTRUCTURAS PRINCIPALES ====================
@dataclass
class Evidencia:
    """
    Unidad de información que soporta o contradice una creencia
    """
    id: str                          # Identificador único
    contenido: str                   # Descripción de la evidencia
    fuente: TipoFuente               # Cómo se obtuvo esta evidencia
    fecha: datetime                  # Cuándo se recopiló
    confiabilidad: float             # Valor entre 0 (no confiable) y 1 (totalmente confiable)
    relacionada_con: Set[str] = field(default_factory=set)  # IDs de creencias relacionadas

    def __str__(self):
        return (f"Evidencia[{self.id}]: '{self.contenido}'\n"
                f"  Fuente: {self.fuente.name}, Confiabilidad: {self.confiabilidad:.0%}\n"
                f"  Fecha: {self.fecha}, Relacionada con: {self.relacionada_con or 'Ninguna'}")

@dataclass
class Creencias:
    """
    Representa una creencia específica de un agente
    """
    id: str                          # Identificador único
    proposicion: str                 # Enunciado de la creencia (ej: "El cielo es azul")
    certidumbre: GradoCertidumbre    # Nivel de certeza actual
    evidencias: List[str] = field(default_factory=list)  # IDs de evidencias asociadas
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    dependencias: Set[str] = field(default_factory=set)  # IDs de creencias de las que depende

    def actualizar_certidumbre(self, nuevo_grado: GradoCertidumbre):
        """Actualiza el grado de certeza y registra la fecha"""
        self.certidumbre = nuevo_grado
        self.fecha_actualizacion = datetime.now()

    def agregar_evidencia(self, evidencia_id: str):
        """Vincula una evidencia a esta creencia"""
        if evidencia_id not in self.evidencias:
            self.evidencias.append(evidencia_id)

    def __str__(self):
        return (f"Creencias[{self.id}]: '{self.proposicion}'\n"
                f"  Certidumbre: {self.certidumbre.name} ({self.certidumbre.value * 20}%)\n"
                f"  Evidencias: {len(self.evidencias)}, Actualizado: {self.fecha_actualizacion}")

@dataclass
class Agente:
    """
    Entidad (persona, IA, sistema) que posee creencias
    """
    id: str                          # Identificador único
    nombre: str                      # Nombre descriptivo
    creencias: Dict[str, Creencias] = field(default_factory=dict)  # Creencias por ID
    evidencias: Dict[str, Evidencia] = field(default_factory=dict)  # Evidencias por ID

    def agregar_creencia(self, creencia: Creencias):
        """Registra una nueva creencia"""
        self.creencias[creencia.id] = creencia

    def agregar_evidencia(self, evidencia: Evidencia):
        """Registra una nueva evidencia"""
        self.evidencias[evidencia.id] = evidencia
        # Actualizar creencias relacionadas
        for creencia_id in evidencia.relacionada_con:
            if creencia_id in self.creencias:
                self.creencias[creencia_id].agregar_evidencia(evidencia.id)

    def evaluar_consistencia(self) -> List[str]:
        """
        Evalúa consistencia entre creencias
        Retorna lista de inconsistencias detectadas
        """
        inconsistencias = []
        # Ejemplo simplificado: detectar creencias contradictorias
        proposiciones = {}
        for creencia in self.creencias.values():
            if creencia.proposicion in proposiciones:
                otra_creencia = proposiciones[creencia.proposicion]
                if otra_creencia.certidumbre.value > 3 and creencia.certidumbre.value < 3:
                    inconsistencias.append(
                        f"Conflicto entre {creencia.id} ({creencia.certidumbre.name}) y "
                        f"{otra_creencia.id} ({otra_creencia.certidumbre.name}) sobre "
                        f"'{creencia.proposicion}'"
                    )
            else:
                proposiciones[creencia.proposicion] = creencia
        return inconsistencias

    def actualizar_creencias(self):
        """
        Recalcula certidumbres basándose en evidencia disponible
        (Versión simplificada para el ejemplo)
        """
        for creencia in self.creencias.values():
            if not creencia.evidencias:
                continue
            
            # Calcular nueva certidumbre basada en evidencia
            suma_confiabilidad = sum(
                self.evidencias[evid_id].confiabilidad
                for evid_id in creencia.evidencias
                if evid_id in self.evidencias
            )
            promedio = suma_confiabilidad / len(creencia.evidencias)
            
            # Mapear a GradoCertidumbre
            nuevo_grado = (
                GradoCertidumbre.SEGURO if promedio >= 0.8 else
                GradoCertidumbre.PROBABLE if promedio >= 0.6 else
                GradoCertidumbre.POSIBLE if promedio >= 0.4 else
                GradoCertidumbre.DUDA_MODERADA if promedio >= 0.2 else
                GradoCertidumbre.DUDA_EXTREMA
            )
            
            creencia.actualizar_certidumbre(nuevo_grado)

    def __str__(self):
        return (f"Agente: {self.nombre} ({self.id})\n"
                f"  Creencias: {len(self.creencias)}, Evidencias: {len(self.evidencias)}")

# ==================== SISTEMA PRINCIPAL ====================
class SistemaCreencias:
    """
    Sistema completo para gestionar múltiples agentes y sus creencias
    """
    def __init__(self):
        self.agentes: Dict[str, Agente] = {}  # Agentes registrados por ID
        self.historico: List[Dict] = []       # Registro de cambios importantes

    def registrar_agente(self, agente: Agente):
        """Añade un nuevo agente al sistema"""
        self.agentes[agente.id] = agente
        self._registrar_evento(f"Nuevo agente registrado: {agente.nombre}")

    def _registrar_evento(self, descripcion: str):
        """Registra un evento en el historial"""
        self.historico.append({
            "fecha": datetime.now().isoformat(),
            "evento": descripcion
        })

    def exportar_json(self, archivo: str):
        """Exporta todo el sistema a un archivo JSON"""
        datos = {
            "agentes": {
                agente_id: {
                    "nombre": agente.nombre,
                    "creencias": {
                        creencia_id: {
                            "proposicion": creencia.proposicion,
                            "certidumbre": creencia.certidumbre.name,
                            "evidencias": creencia.evidencias,
                            "fecha_creacion": creencia.fecha_creacion.isoformat(),
                            "fecha_actualizacion": creencia.fecha_actualizacion.isoformat(),
                            "dependencias": list(creencia.dependencias)
                        } for creencia_id, creencia in agente.creencias.items()
                    },
                    "evidencias": {
                        evidencia_id: {
                            "contenido": evidencia.contenido,
                            "fuente": evidencia.fuente.name,
                            "fecha": evidencia.fecha.isoformat(),
                            "confiabilidad": evidencia.confiabilidad,
                            "relacionada_con": list(evidencia.relacionada_con)
                        } for evidencia_id, evidencia in agente.evidencias.items()
                    }
                } for agente_id, agente in self.agentes.items()
            },
            "historico": self.historico
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @classmethod
    def cargar_json(cls, archivo: str) -> 'SistemaCreencias':
        """Carga un sistema desde archivo JSON"""
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        sistema = cls()
        
        # Cargar agentes
        for agente_id, info in datos["agentes"].items():
            agente = Agente(agente_id, info["nombre"])
            
            # Cargar evidencias primero
            for evidencia_id, evid_info in info["evidencias"].items():
                evidencia = Evidencia(
                    id=evidencia_id,
                    contenido=evid_info["contenido"],
                    fuente=TipoFuente[evid_info["fuente"]],
                    fecha=datetime.fromisoformat(evid_info["fecha"]),
                    confiabilidad=evid_info["confiabilidad"],
                    relacionada_con=set(evid_info["relacionada_con"])
                )
                agente.evidencias[evidencia_id] = evidencia
            
            # Cargar creencias
            for creencia_id, creencia_info in info["creencias"].items():
                creencia = Creencias(
                    id=creencia_id,
                    proposicion=creencia_info["proposicion"],
                    certidumbre=GradoCertidumbre[creencia_info["certidumbre"]],
                    evidencias=creencia_info["evidencias"],
                    fecha_creacion=datetime.fromisoformat(creencia_info["fecha_creacion"]),
                    fecha_actualizacion=datetime.fromisoformat(creencia_info["fecha_actualizacion"]),
                    dependencias=set(creencia_info["dependencias"])
                )
                agente.creencias[creencia_id] = creencia
            
            sistema.registrar_agente(agente)
        
        # Cargar histórico
        sistema.historico = datos.get("historico", [])
        
        return sistema

    def __str__(self):
        return (f"Sistema de Creencias\n"
                f"Agentes: {len(self.agentes)}\n"
                f"Eventos registrados: {len(self.historico)}")

# ==================== EJEMPLO DE USO ====================
def configurar_sistema_ejemplo() -> SistemaCreencias:
    """Configura un sistema de ejemplo con agentes y creencias"""
    sistema = SistemaCreencias()
    
    # Crear agentes
    agente_humano = Agente("ag1", "Juan Pérez")
    agente_ia = Agente("ag2", "Asistente Médico AI")
    
    # Evidencias para el agente humano
    evidencia1 = Evidencia(
        id="ev1",
        contenido="Ví manchas rojas en mi piel esta mañana",
        fuente=TipoFuente.PERCEPCION,
        fecha=datetime(2023, 10, 15, 8, 30),
        confiabilidad=0.9
    )
    
    evidencia2 = Evidencia(
        id="ev2",
        contenido="Mi médico dijo que podría ser alergia",
        fuente=TipoFuente.TESTIMONIO,
        fecha=datetime(2023, 10, 15, 14, 0),
        confiabilidad=0.7
    )
    
    # Creencias del agente humano
    creencia1 = Creencias(
        id="cr1",
        proposicion="Tengo una condición en la piel",
        certidumbre=GradoCertidumbre.PROBABLE,
        evidencias=["ev1", "ev2"]
    )
    
    creencia2 = Creencias(
        id="cr2",
        proposicion="Es probablemente una alergia",
        certidumbre=GradoCertidumbre.POSIBLE,
        evidencias=["ev2"],
        dependencias={"cr1"}
    )
    
    # Evidencia para la IA
    evidencia3 = Evidencia(
        id="ev3",
        contenido="Análisis de imagen muestra erupción alérgica típica",
        fuente=TipoFuente.INFERENCIA,
        fecha=datetime(2023, 10, 15, 15, 0),
        confiabilidad=0.85,
        relacionada_con={"cr3"}
    )
    
    # Creencia de la IA
    creencia3 = Creencias(
        id="cr3",
        proposicion="El paciente tiene dermatitis alérgica",
        certidumbre=GradoCertidumbre.PROBABLE,
        evidencias=["ev3"]
    )
    
    # Ensamblar todo
    agente_humano.agregar_evidencia(evidencia1)
    agente_humano.agregar_evidencia(evidencia2)
    agente_humano.agregar_creencia(creencia1)
    agente_humano.agregar_creencia(creencia2)
    
    agente_ia.agregar_evidencia(evidencia3)
    agente_ia.agregar_creencia(creencia3)
    
    sistema.registrar_agente(agente_humano)
    sistema.registrar_agente(agente_ia)
    
    return sistema

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    # Crear y mostrar el sistema de ejemplo
    sistema = configurar_sistema_ejemplo()
    print(sistema)
    
    # Mostrar detalles de agentes
    for agente in sistema.agentes.values():
        print("\n" + "="*50)
        print(agente)
        print("\nCreencias:")
        for creencia in agente.creencias.values():
            print(f"  - {creencia}")
        
        print("\nEvidencias:")
        for evidencia in agente.evidencias.values():
            print(f"  - {evidencia}")
        
        # Evaluar consistencia
        inconsistencias = agente.evaluar_consistencia()
        if inconsistencias:
            print("\n¡Inconsistencias encontradas!")
            for inc in inconsistencias:
                print(f"  * {inc}")
    
    # Exportar a JSON
    sistema.exportar_json("sistema_creencias.json")
    print("\nSistema exportado a 'sistema_creencias.json'")
    
    # Ejemplo de actualización de creencias
    print("\nActualizando creencias basadas en evidencia...")
    for agente in sistema.agentes.values():
        agente.actualizar_creencias()
    
    # Mostrar cambios
    print("\nEstado después de actualización:")
    for agente in sistema.agentes.values():
        print(f"\n{agente.nombre}:")
        for creencia in agente.creencias.values():
            print(f"  - {creencia.proposicion}: {creencia.certidumbre.name}")