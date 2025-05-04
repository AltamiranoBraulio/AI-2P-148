# Importación de librerías necesarias
import tkinter as tk  # Para la interfaz gráfica básica
from tkinter import ttk, messagebox  # Widgets mejorados y cuadros de mensaje
from pgmpy.models import BayesianNetwork  # Para crear redes bayesianas
from pgmpy.factors.discrete import TabularCPD  # Para tablas de probabilidad condicional
from pgmpy.inference import VariableElimination  # Para hacer inferencia probabilística

class DiagnosticCausalSystem:
    def __init__(self, root):
        """Constructor de la clase principal.
        root: ventana principal de tkinter donde se añadirán los componentes"""
        self.root = root
        self.root.title("Sistema de Diagnóstico y Causalidad")  # Título de la ventana
        
        # Base de conocimientos inicial para diagnóstico médico
        # Cada regla contiene síntomas, diagnóstico asociado y certeza (0-1)
        self.diagnostic_rules = [
            {"symptoms": ["fiebre", "tos"], "diagnosis": "gripe", "certainty": 0.7},
            {"symptoms": ["dolor_cabeza", "náuseas"], "diagnosis": "migraña", "certainty": 0.8},
            {"symptoms": ["dolor_pecho", "dificultad_respirar"], "diagnosis": "ataque_cardíaco", "certainty": 0.9}
        ]
        
        # Construcción de la red bayesiana para relaciones causales
        self.causal_network = self._build_causal_network()
        
        # Configuración de la interfaz de usuario
        self._setup_ui()

    def _build_causal_network(self):
        """Construye y retorna una red bayesiana para modelar relaciones causales.
        En este caso, modela cómo fumar y la contaminación afectan la probabilidad de cáncer."""
        
        # Creación del modelo con dos causas (Fumar y Contaminación) y un efecto (Cáncer)
        model = BayesianNetwork([("Fumar", "Cáncer"), ("Contaminación", "Cáncer")])
        
        # Tablas de Probabilidad Condicional (CPD) para cada nodo:
        
        # 1. Probabilidad marginal de Fumar (30% fuma, 70% no)
        cpd_fumar = TabularCPD(
            variable="Fumar", 
            variable_card=2,  # 2 valores posibles (0: No, 1: Sí)
            values=[[0.7], [0.3]]  # 70% no fuma, 30% sí
        )
        
        # 2. Probabilidad marginal de Contaminación (60% baja, 40% alta)
        cpd_cont = TabularCPD(
            variable="Contaminación", 
            variable_card=2, 
            values=[[0.6], [0.4]]  # 60% baja, 40% alta
        )
        
        # 3. Probabilidad condicional de Cáncer dado Fumar y Contaminación
        # La tabla representa P(Cáncer | Fumar, Contaminación)
        cpd_cancer = TabularCPD(
            variable="Cáncer", 
            variable_card=2,  # 2 valores (0: No cáncer, 1: Cáncer)
            values=[
                # Probabilidades para NO cáncer (fila 0)
                [0.99, 0.85, 0.80, 0.60],  # Combinaciones:
                # [No fuma + Baja cont, No fuma + Alta cont, Fuma + Baja cont, Fuma + Alta cont]
                
                # Probabilidades para SÍ cáncer (fila 1)
                [0.01, 0.15, 0.20, 0.40]   # Mismas combinaciones
            ],
            evidence=["Fumar", "Contaminación"],  # Variables de las que depende
            evidence_card=[2, 2]  # Ambas tienen 2 valores posibles
        )
        
        # Añadir las CPDs al modelo
        model.add_cpds(cpd_fumar, cpd_cont, cpd_cancer)
        return model

    def _setup_ui(self):
        """Configura todos los componentes de la interfaz gráfica."""
        
        # ========== Frame para Diagnóstico Médico ==========
        frame_diagnosis = ttk.LabelFrame(self.root, text="Diagnóstico Médico")
        frame_diagnosis.pack(padx=10, pady=10, fill="both")
        
        # Título y lista de síntomas con checkboxes
        ttk.Label(frame_diagnosis, text="Selecciona síntomas:").pack()
        
        # Diccionario para almacenar variables BooleanVar de los checkboxes
        self.symptoms_vars = {}
        
        # Lista de síntomas disponibles
        symptoms = ["fiebre", "tos", "dolor_cabeza", "náuseas", "dolor_pecho", "dificultad_respirar"]
        
        # Crear un checkbox por cada síntoma
        for symptom in symptoms:
            var = tk.BooleanVar()  # Variable para almacenar estado (True/False)
            # Checkbutton con el texto del síntoma, vinculado a la variable
            tk.Checkbutton(frame_diagnosis, text=symptom, variable=var).pack(anchor="w")
            self.symptoms_vars[symptom] = var  # Guardar referencia
        
        # Botón para ejecutar diagnóstico
        ttk.Button(
            frame_diagnosis, 
            text="Diagnosticar", 
            command=self.run_diagnosis  # Método que se ejecutará al hacer clic
        ).pack(pady=5)
        
        # ========== Frame para Modelo Causal ==========
        frame_causal = ttk.LabelFrame(self.root, text="Modelo Causal (Red Bayesiana)")
        frame_causal.pack(padx=10, pady=10, fill="both")
        
        # Combobox para seleccionar si el paciente fuma
        ttk.Label(frame_causal, text="¿Fuma el paciente?").pack()
        self.smoking_var = tk.StringVar(value="No")  # Valor por defecto
        ttk.Combobox(
            frame_causal, 
            textvariable=self.smoking_var, 
            values=["No", "Sí"]  # Opciones disponibles
        ).pack()
        
        # Combobox para nivel de contaminación
        ttk.Label(frame_causal, text="Nivel de contaminación:").pack()
        self.pollution_var = tk.StringVar(value="Baja")  # Valor por defecto
        ttk.Combobox(
            frame_causal, 
            textvariable=self.pollution_var, 
            values=["Baja", "Alta"]
        ).pack()
        
        # Botón para calcular riesgo de cáncer
        ttk.Button(
            frame_causal, 
            text="Calcular riesgo de cáncer", 
            command=self.run_causal_inference  # Método asociado
        ).pack(pady=5)
        
        # ========== Área de Resultados ==========
        # Widget Text para mostrar resultados diagnósticos y causales
        self.result_text = tk.Text(
            self.root, 
            height=10,  # Altura en líneas de texto
            wrap="word"  # Ajuste de líneas por palabras
        )
        self.result_text.pack(padx=10, pady=10, fill="both")

    def run_diagnosis(self):
        """Ejecuta el motor de diagnóstico basado en reglas."""
        # Obtener síntomas seleccionados (donde el checkbox está marcado)
        observed_symptoms = [symptom for symptom, var in self.symptoms_vars.items() if var.get()]
        
        # Validar que se haya seleccionado al menos un síntoma
        if not observed_symptoms:
            messagebox.showwarning("Error", "¡Selecciona al menos un síntoma!")
            return
        
        # Lista para almacenar diagnósticos posibles
        possible_diagnoses = []
        
        # Recorrer todas las reglas de diagnóstico
        for rule in self.diagnostic_rules:
            # Verificar si TODOS los síntomas de la regla están presentes
            if all(symptom in observed_symptoms for symptom in rule["symptoms"]):
                # Añadir diagnóstico y su certeza
                possible_diagnoses.append((rule["diagnosis"], rule["certainty"]))
        
        # Ordenar diagnósticos por certeza (de mayor a menor)
        possible_diagnoses.sort(key=lambda x: x[1], reverse=True)
        
        # Mostrar resultados en el área de texto
        self.result_text.delete(1.0, tk.END)  # Limpiar contenido previo
        
        if possible_diagnoses:
            self.result_text.insert(tk.END, "🔍 Resultados del diagnóstico:\n")
            for diagnosis, certainty in possible_diagnoses:
                # Mostrar cada diagnóstico con su certeza en porcentaje
                self.result_text.insert(tk.END, f"- {diagnosis} (Certeza: {certainty*100:.1f}%)\n")
        else:
            self.result_text.insert(tk.END, "⚠️ No se encontraron diagnósticos para los síntomas seleccionados.\n")

    def run_causal_inference(self):
        """Ejecuta inferencia en la red bayesiana para calcular probabilidad de cáncer."""
        # Convertir respuestas a valores numéricos (1: Sí/True, 0: No/False)
        smoking = 1 if self.smoking_var.get() == "Sí" else 0
        pollution = 1 if self.pollution_var.get() == "Alta" else 0
        
        # Crear objeto para hacer inferencia por eliminación de variables
        infer = VariableElimination(self.causal_network)
        
        # Consultar la probabilidad de cáncer dados los valores de Fumar y Contaminación
        result = infer.query(
            variables=["Cáncer"],  # Variable de interés
            evidence={
                "Fumar": smoking, 
                "Contaminación": pollution
            }  # Evidencia observada
        )
        
        # Obtener probabilidad de cáncer (valores[1] corresponde a "Sí cáncer")
        prob_cancer = result.values[1]
        
        # Mostrar resultados
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "📊 Resultado del modelo causal:\n")
        self.result_text.insert(tk.END, f"- Probabilidad de cáncer: {prob_cancer*100:.1f}%\n")
        self.result_text.insert(tk.END, f"- Factores: Fumar={self.smoking_var.get()}, Contaminación={self.pollution_var.get()}\n")

# Punto de entrada principal
if __name__ == "__main__":
    root = tk.Tk()  # Crear ventana principal
    app = DiagnosticCausalSystem(root)  # Instanciar nuestra aplicación
    root.mainloop()  # Iniciar el bucle principal de la interfaz