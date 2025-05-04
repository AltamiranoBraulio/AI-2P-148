"""
SISTEMA DE MARCOS PARA ACCIONES, SITUACIONES Y EVENTOS
----------------------------------------------------
Este sistema permite:
- Representar acciones complejas mediante marcos (frames)
- Modelar situaciones con participantes, ubicaciones y tiempos
- Relacionar eventos en secuencias temporales
- Inferir información implícita basada en esquemas predefinidos
"""

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum, auto
import json
from datetime import datetime

# ==================== ENUMERACIONES BÁSICAS ====================
class TipoEntidad(Enum):
    """Tipos de entidades en el sistema"""
    ACCION = auto()      # Ej: "Comer", "Caminar"
    OBJETO = auto()      # Ej: "Manzana", "Cuchillo"
    AGENTE = auto()      # Ej: "Persona", "Robot"
    LUGAR = auto()       # Ej: "Cocina", "Parque"
    TIEMPO = auto()      # Ej: "Mañana", "2023-10-15"

# ==================== ESTRUCTURAS PRINCIPALES ====================
@dataclass
class Slot:
    """
    Un 'slot' (ranura) en un marco que puede contener:
    - Un valor concreto
    - Una referencia a otro marco
    - Restricciones sobre valores permitidos
    """
    nombre: str
    tipo: Union[type, TipoEntidad, str]  # Tipo de dato esperado
    valor: Optional[Any] = None          # Valor actual (opcional)
    cardinalidad: str = "uno"            # "uno" o "muchos"
    restricciones: List[str] = field(default_factory=list)  # Reglas de validación

    def __str__(self):
        valor_str = f" = {self.valor}" if self.valor is not None else ""
        return f"{self.nombre}: {self.tipo}{valor_str} {'[' + ', '.join(self.restricciones) + ']' if self.restricciones else ''}"

@dataclass
class Marco:
    """
    Un 'marco' (frame) que representa una acción, situación o evento
    con múltiples slots (atributos/propiedades)
    """
    nombre: str
    tipo: TipoEntidad
    slots: Dict[str, Slot] = field(default_factory=dict)
    hijos: List['Marco'] = field(default_factory=list)  # Relaciones de subtipos

    def agregar_slot(self, slot: Slot):
        """Añade un nuevo slot al marco"""
        self.slots[slot.nombre] = slot

    def establecer_valor(self, nombre_slot: str, valor: Any):
        """Asigna un valor a un slot existente"""
        if nombre_slot in self.slots:
            # Validación básica de tipo (simplificada para el ejemplo)
            slot = self.slots[nombre_slot]
            if slot.tipo == TipoEntidad.OBJETO and not isinstance(valor, str):
                raise ValueError(f"Slot {nombre_slot} requiere un objeto (nombre)")
            self.slots[nombre_slot].valor = valor
        else:
            raise KeyError(f"Slot {nombre_slot} no existe")

    def inferir_valores(self, sistema: 'SistemaMarcos'):
        """
        Intenta inferir valores faltantes basándose en:
        - Valores por defecto
        - Relaciones con otros marcos
        - Reglas de inferencia del sistema
        """
        # Ejemplo simplificado: inferir 'duración' si hay 'hora_inicio' y 'hora_fin'
        if 'hora_inicio' in self.slots and 'hora_fin' in self.slots:
            if self.slots['hora_inicio'].valor and self.slots['hora_fin'].valor:
                inicio = datetime.fromisoformat(self.slots['hora_inicio'].valor)
                fin = datetime.fromisoformat(self.slots['hora_fin'].valor)
                duracion = fin - inicio
                if 'duracion' not in self.slots:
                    self.agregar_slot(Slot('duracion', str, restricciones=["positivo"]))
                self.slots['duracion'].valor = str(duracion)

    def __str__(self):
        slots_str = "\n    ".join(str(slot) for slot in self.slots.values())
        hijos_str = ", ".join(hijo.nombre for hijo in self.hijos) if self.hijos else "Ninguno"
        return (f"Marco: {self.nombre} ({self.tipo.name})\n"
                f"Slots:\n    {slots_str}\n"
                f"Subtipos: {hijos_str}")

# ==================== SISTEMA PRINCIPAL ====================
class SistemaMarcos:
    """
    Sistema completo que gestiona múltiples marcos y sus relaciones
    """
    def __init__(self):
        self.marcos: Dict[str, Marco] = {}  # Todos los marcos por nombre
        self.esquemas: Dict[str, Marco] = {}  # Plantillas para tipos comunes

    def registrar_esquema(self, nombre: str, tipo: TipoEntidad, slots: List[Slot]):
        """
        Registra un esquema (plantilla) para crear marcos similares
        Ej: Esquema "EventoComida" con slots ["participantes", "ubicacion", "alimentos"]
        """
        marco = Marco(nombre, tipo)
        for slot in slots:
            marco.agregar_slot(slot)
        self.esquemas[nombre] = marco

    def crear_marco(self, nombre: str, tipo: TipoEntidad, esquema: Optional[str] = None) -> Marco:
        """
        Crea un nuevo marco, opcionalmente basado en un esquema existente
        """
        if esquema and esquema in self.esquemas:
            nuevo_marco = Marco(nombre, tipo)
            # Copiar slots del esquema
            for nombre_slot, slot in self.esquemas[esquema].slots.items():
                nuevo_marco.agregar_slot(Slot(
                    nombre=slot.nombre,
                    tipo=slot.tipo,
                    cardinalidad=slot.cardinalidad,
                    restricciones=slot.restricciones.copy()
                ))
            self.marcos[nombre] = nuevo_marco
            return nuevo_marco
        else:
            marco = Marco(nombre, tipo)
            self.marcos[nombre] = marco
            return marco

    def relacionar_marcos(self, padre: str, hijo: str):
        """Establece una relación de subtipo entre marcos"""
        if padre in self.marcos and hijo in self.marcos:
            self.marcos[padre].hijos.append(self.marcos[hijo])
        else:
            raise KeyError("Uno o ambos marcos no existen")

    def exportar_json(self, archivo: str):
        """Exporta todos los marcos a un archivo JSON"""
        datos = {
            "marcos": {
                nombre: {
                    "tipo": marco.tipo.name,
                    "slots": {
                        nombre_slot: {
                            "tipo": str(slot.tipo),
                            "valor": slot.valor,
                            "cardinalidad": slot.cardinalidad,
                            "restricciones": slot.restricciones
                        } for nombre_slot, slot in marco.slots.items()
                    },
                    "hijos": [hijo.nombre for hijo in marco.hijos]
                } for nombre, marco in self.marcos.items()
            },
            "esquemas": {
                nombre: {
                    "tipo": esquema.tipo.name,
                    "slots": {
                        nombre_slot: {
                            "tipo": str(slot.tipo),
                            "cardinalidad": slot.cardinalidad,
                            "restricciones": slot.restricciones
                        } for nombre_slot, slot in esquema.slots.items()
                    }
                } for nombre, esquema in self.esquemas.items()
            }
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @classmethod
    def cargar_json(cls, archivo: str) -> 'SistemaMarcos':
        """Carga un sistema de marcos desde un archivo JSON"""
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        sistema = cls()
        
        # Cargar esquemas primero
        for nombre, info in datos.get("esquemas", {}).items():
            slots = [
                Slot(
                    nombre=nombre_slot,
                    tipo=eval(slot_info["tipo"]) if "TipoEntidad" not in slot_info["tipo"] else TipoEntidad[slot_info["tipo"].split(".")[-1]],
                    cardinalidad=slot_info["cardinalidad"],
                    restricciones=slot_info["restricciones"]
                ) for nombre_slot, slot_info in info["slots"].items()
            ]
            sistema.registrar_esquema(
                nombre,
                TipoEntidad[info["tipo"]],
                slots
            )
        
        # Cargar marcos
        for nombre, info in datos.get("marcos", {}).items():
            marco = sistema.crear_marco(nombre, TipoEntidad[info["tipo"]])
            for nombre_slot, slot_info in info["slots"].items():
                marco.agregar_slot(Slot(
                    nombre=nombre_slot,
                    tipo=eval(slot_info["tipo"]) if "TipoEntidad" not in slot_info["tipo"] else TipoEntidad[slot_info["tipo"].split(".")[-1]],
                    valor=slot_info["valor"],
                    cardinalidad=slot_info["cardinalidad"],
                    restricciones=slot_info["restricciones"]
                ))
        
        # Establecer relaciones de herencia
        for nombre, info in datos.get("marcos", {}).items():
            for hijo_nombre in info["hijos"]:
                sistema.relacionar_marcos(nombre, hijo_nombre)
        
        return sistema

    def __str__(self):
        """Representación legible del sistema"""
        marcos_str = "\n\n".join(str(marco) for marco in self.marcos.values())
        esquemas_str = "\n\n".join(f"Esquema: {nombre}\n{marco}" for nombre, marco in self.esquemas.items())
        return (f"Sistema de Marcos\n"
                f"=================\n"
                f"Marcos ({len(self.marcos)}):\n{marcos_str}\n\n"
                f"Esquemas ({len(self.esquemas)}):\n{esquemas_str}")

# ==================== EJEMPLO DE USO ====================
def configurar_sistema_ejemplo() -> SistemaMarcos:
    """Configura un sistema de ejemplo con marcos para eventos de cocina"""
    sistema = SistemaMarcos()
    
    # 1. Registrar esquemas básicos
    sistema.registrar_esquema(
        nombre="EventoConParticipantes",
        tipo=TipoEntidad.ACCION,
        slots=[
            Slot("participantes", TipoEntidad.AGENTE, cardinalidad="muchos"),
            Slot("ubicacion", TipoEntidad.LUGAR),
            Slot("hora_inicio", str),  # ISO format
            Slot("hora_fin", str)
        ]
    )
    
    sistema.registrar_esquema(
        nombre="EventoConObjetos",
        tipo=TipoEntidad.ACCION,
        slots=[
            Slot("objetos", TipoEntidad.OBJETO, cardinalidad="muchos"),
            Slot("objetivo", str)
        ]
    )
    
    # 2. Crear marcos específicos basados en esquemas
    evento_cocinar = sistema.crear_marco(
        nombre="CocinarPasta",
        tipo=TipoEntidad.ACCION,
        esquema="EventoConParticipantes"
    )
    
    # Añadir slots adicionales específicos
    evento_cocinar.agregar_slot(Slot("ingredientes", TipoEntidad.OBJETO, cardinalidad="muchos"))
    evento_cocinar.agregar_slot(Slot("receta", str))
    
    # 3. Establecer valores
    evento_cocinar.establecer_valor("participantes", ["Juan", "María"])
    evento_cocinar.establecer_valor("ubicacion", "Cocina")
    evento_cocinar.establecer_valor("hora_inicio", "2023-10-15T18:00:00")
    evento_cocinar.establecer_valor("hora_fin", "2023-10-15T19:30:00")
    evento_cocinar.establecer_valor("ingredientes", ["pasta", "salsa", "queso"])
    evento_cocinar.establecer_valor("receta", "Italiana")
    
    # 4. Inferir valores (ej: duración)
    evento_cocinar.inferir_valores(sistema)
    
    # 5. Crear marcos relacionados
    ingrediente_pasta = sistema.crear_marco("Pasta", TipoEntidad.OBJETO)
    ingrediente_pasta.agregar_slot(Slot("tipo", str, valor="espagueti"))
    ingrediente_pasta.agregar_slot(Slot("cantidad", str, valor="500g"))
    
    return sistema

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    # Crear y mostrar el sistema de ejemplo
    sistema = configurar_sistema_ejemplo()
    print(sistema)
    
    # Exportar a JSON
    sistema.exportar_json("sistema_marcos.json")
    print("\nSistema exportado a 'sistema_marcos.json'")
    
    # Ejemplo de carga
    sistema_cargado = SistemaMarcos.cargar_json("sistema_marcos.json")
    print("\nSistema cargado desde JSON:")
    print(sistema_cargado.marcos["CocinarPasta"])