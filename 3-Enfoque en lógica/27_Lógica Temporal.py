"""
Sistema de Monitoreo de Procesos Industriales con Lógica Temporal
Este código implementa un simulador de procesos industriales con capacidades de:
- Verificación de propiedades temporales (LTL)
- Monitoreo en tiempo real
- Análisis de patrones temporales
- Visualización de series temporales
"""
import random
import time
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class EstadoProceso(Enum):
    """Enumeración de estados posibles de un proceso industrial"""
    INACTIVO = 0
    INICIANDO = 1
    OPERANDO = 2
    ALERTA = 3
    DETENIDO = 4

class TemporalOperator(Enum):
    """Operadores temporales para fórmulas LTL"""
    GLOBALLY = "G"      # Siempre en el futuro
    EVENTUALLY = "F"    # En algún momento futuro
    NEXT = "X"          # En el siguiente estado
    UNTIL = "U"        # Hasta que ocurra
    RELEASE = "R"      # Liberación (dual de Until)

class ProcesoIndustrial:
    """Clase que simula un proceso industrial con estados temporales"""
    
    def __init__(self, nombre):
        """Inicializa el proceso con parámetros predeterminados"""
        self.nombre = nombre
        self.estado_actual = EstadoProceso.INACTIVO
        self.historial_estados = deque(maxlen=100)  # Historial circular
        self.historial_tiempos = deque(maxlen=100)
        self.temperatura = 25.0
        self.presion = 1.0
        self.umbral_alerta_temp = 90.0
        self.umbral_alerta_presion = 5.0
        self.tiempo_inicio = time.time()
        
        # Registrar estado inicial
        self._registrar_estado()
    
    def _registrar_estado(self):
        """Registra el estado actual en el historial con timestamp"""
        self.historial_estados.append(self.estado_actual)
        self.historial_tiempos.append(time.time() - self.tiempo_inicio)
    
    def actualizar(self):
        """Actualiza el estado del proceso según lógica de transición"""
        # Lógica de transición de estados con comportamiento pseudo-aleatorio
        if self.estado_actual == EstadoProceso.INACTIVO:
            if random.random() < 0.3:  # 30% de probabilidad de iniciar
                self.estado_actual = EstadoProceso.INICIANDO
        
        elif self.estado_actual == EstadoProceso.INICIANDO:
            # Simular aumento de temperatura y presión durante el inicio
            self.temperatura = min(self.temperatura + random.uniform(0.5, 2.0), 80.0)
            self.presion = min(self.presion + random.uniform(0.1, 0.3), 3.0)
            
            if self.temperatura > 60.0 and self.presion > 1.5:
                self.estado_actual = EstadoProceso.OPERANDO
        
        elif self.estado_actual == EstadoProceso.OPERANDO:
            # Fluctuaciones normales durante operación
            self.temperatura += random.uniform(-1.0, 1.5)
            self.presion += random.uniform(-0.2, 0.2)
            
            # Verificar condiciones de alerta
            if (self.temperatura > self.umbral_alerta_temp or 
                self.presion > self.umbral_alerta_presion):
                self.estado_actual = EstadoProceso.ALERTA
            elif random.random() < 0.05:  # 5% de probabilidad de detenerse
                self.estado_actual = EstadoProceso.DETENIDO
        
        elif self.estado_actual == EstadoProceso.ALERTA:
            # Intentar recuperación automática
            self.temperatura *= 0.95  # Reducir temperatura gradualmente
            self.presion *= 0.97      # Reducir presión gradualmente
            
            if (self.temperatura < 80.0 and self.presion < 4.0):
                self.estado_actual = EstadoProceso.OPERANDO
            elif random.random() < 0.2:  # 20% de probabilidad de detención
                self.estado_actual = EstadoProceso.DETENIDO
        
        elif self.estado_actual == EstadoProceso.DETENIDO:
            # Enfriamiento gradual
            self.temperatura = max(25.0, self.temperatura * 0.9)
            self.presion = max(1.0, self.presion * 0.9)
            
            if random.random() < 0.1:  # 10% de probabilidad de reiniciar
                self.estado_actual = EstadoProceso.INACTIVO
        
        # Registrar el nuevo estado
        self._registrar_estado()
    
    def verificar_propiedad_ltl(self, formula):
        """
        Verifica una propiedad LTL sobre el historial de estados
        Args:
            formula: Tupla (operador, estado) o (operador, formula1, formula2)
        Returns:
            bool: Si la propiedad se cumple en el historial
        """
        operador = formula[0]
        
        if operador == TemporalOperator.GLOBALLY:
            # G φ: φ debe cumplirse en todos los estados
            estado = formula[1]
            return all(s == estado for s in self.historial_estados)
        
        elif operador == TemporalOperator.EVENTUALLY:
            # F φ: φ debe cumplirse en al menos un estado
            estado = formula[1]
            return any(s == estado for s in self.historial_estados)
        
        elif operador == TemporalOperator.NEXT:
            # X φ: φ debe cumplirse en el siguiente estado
            estado = formula[1]
            if len(self.historial_estados) < 2:
                return False
            return self.historial_estados[1] == estado
        
        elif operador == TemporalOperator.UNTIL:
            # φ U ψ: φ debe cumplirse hasta que ψ se cumpla
            phi, psi = formula[1], formula[2]
            encontrado_psi = False
            
            for estado in self.historial_estados:
                if estado == psi:
                    encontrado_psi = True
                    break
                if estado != phi:
                    return False
            
            return encontrado_psi
        
        elif operador == TemporalOperator.RELEASE:
            # φ R ψ: ψ debe ser verdad hasta que φ sea verdad (dual de Until)
            phi, psi = formula[1], formula[2]
            encontrado_phi = False
            
            for estado in self.historial_estados:
                if estado == phi:
                    encontrado_phi = True
                    break
                if estado != psi:
                    return False
            
            return True
        
        return False

class MonitorTemporal:
    """Monitor de propiedades temporales en tiempo real"""
    
    def __init__(self, proceso):
        """Inicializa el monitor con un proceso a observar"""
        self.proceso = proceso
        self.propiedades = []
        self.alertas = []
    
    def agregar_propiedad(self, formula, descripcion):
        """Registra una propiedad LTL para monitorear"""
        self.propiedades.append((formula, descripcion))
    
    def verificar_propiedades(self):
        """Verifica todas las propiedades registradas"""
        resultados = []
        for formula, descripcion in self.propiedades:
            cumple = self.proceso.verificar_propiedad_ltl(formula)
            resultados.append((descripcion, cumple))
            
            if not cumple:
                self.alertas.append(f"Alerta: {descripcion} no se cumple")
        
        return resultados
    
    def obtener_alertas(self):
        """Devuelve las alertas generadas y limpia el buffer"""
        alertas = self.alertas.copy()
        self.alertas.clear()
        return alertas

def visualizar_proceso(proceso, monitor):
    """Crea una visualización animada del proceso y sus propiedades"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.5)
    
    # Configurar ejes
    ax1.set_title(f"Estado del proceso: {proceso.nombre}")
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_yticks(range(len(EstadoProceso)))
    ax1.set_yticklabels([e.name for e in EstadoProceso])
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel("Estado")
    
    ax2.set_title("Temperatura y Presión")
    ax2.set_xlabel("Tiempo (s)")
    ax2.set_ylabel("Valor")
    ax2.grid(True)
    
    # Datos iniciales
    tiempos = list(proceso.historial_tiempos)
    estados = [e.value for e in proceso.historial_estados]
    temps = [proceso.temperatura] * len(tiempos)
    presiones = [proceso.presion] * len(tiempos)
    
    # Líneas iniciales
    line_estado, = ax1.plot(tiempos, estados, 'b-')
    line_temp, = ax2.plot(tiempos, temps, 'r-', label='Temperatura (°C)')
    line_pres, = ax2.plot(tiempos, presiones, 'g-', label='Presión (atm)')
    ax2.legend()
    
    # Texto para propiedades
    prop_text = fig.text(0.1, 0.02, "", fontsize=10)
    
    def actualizar(frame):
        """Función de actualización para la animación"""
        # Actualizar proceso y monitor
        proceso.actualizar()
        resultados = monitor.verificar_propiedades()
        
        # Actualizar datos
        tiempos.append(proceso.historial_tiempos[-1])
        estados.append(proceso.historial_estados[-1].value)
        temps.append(proceso.temperatura)
        presiones.append(proceso.presion)
        
        # Mantener longitud fija
        if len(tiempos) > 50:
            tiempos.pop(0)
            estados.pop(0)
            temps.pop(0)
            presiones.pop(0)
        
        # Actualizar gráficos
        line_estado.set_data(tiempos, estados)
        line_temp.set_data(tiempos, temps)
        line_pres.set_data(tiempos, presiones)
        
        # Ajustar límites
        ax1.set_xlim(min(tiempos), max(tiempos))
        ax2.set_xlim(min(tiempos), max(tiempos))
        
        y_min_temp = min(temps) - 5 if temps else 0
        y_max_temp = max(temps) + 5 if temps else 100
        ax2.set_ylim(y_min_temp, y_max_temp)
        
        # Actualizar texto de propiedades
        prop_text.set_text("\n".join(
            f"{desc}: {'✔' if res else '✖'}" 
            for desc, res in resultados
        ))
        
        return line_estado, line_temp, line_pres, prop_text
    
    # Crear animación
    ani = FuncAnimation(fig, actualizar, frames=100, interval=500, blit=False)
    plt.close()
    return ani

def demostracion_logica_temporal():
    """Función de demostración del sistema de lógica temporal"""
    # Crear proceso industrial y monitor
    reactor = ProcesoIndustrial("Reactor Principal")
    monitor = MonitorTemporal(reactor)
    
    # Definir propiedades temporales a monitorear
    propiedades = [
        ((TemporalOperator.GLOBALLY, EstadoProceso.ALERTA), 
         "Nunca debe estar en estado ALERTA"),
        
        ((TemporalOperator.EVENTUALLY, EstadoProceso.OPERANDO), 
         "Debe llegar a OPERANDO eventualmente"),
        
        ((TemporalOperator.UNTIL, EstadoProceso.INICIANDO, EstadoProceso.OPERANDO), 
         "Debe estar INICIANDO hasta que pase a OPERANDO"),
        
        ((TemporalOperator.RELEASE, EstadoProceso.DETENIDO, EstadoProceso.INACTIVO), 
         "Debe estar INACTIVO hasta que pase a DETENIDO")
    ]
    
    for prop in propiedades:
        monitor.agregar_propiedad(*prop)
    
    # Configurar y mostrar animación
    print("Iniciando simulación de proceso industrial con monitoreo temporal...")
    print("Propiedades a monitorear:")
    for desc in [p[1] for p in propiedades]:
        print(f"- {desc}")
    
    ani = visualizar_proceso(reactor, monitor)
    return HTML(ani.to_jshtml())

if __name__ == "__main__":
    # Ejecutar demostración
    demostracion = demostracion_logica_temporal()
    display(demostracion)