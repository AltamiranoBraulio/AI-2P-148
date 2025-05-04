import subprocess
from pyswip import Prolog
import clips
import tkinter as tk
from tkinter import ttk, messagebox
import json

class SistemaExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto Médico Integrado")
        self.root.geometry("900x600")
        
        # Inicializar motores
        self.prolog = Prolog()
        self.prolog.consult("diagnostico_medico.pl")
        
        self.env = clips.Environment()
        self.env.load("reglas_clips.clp")
        
        # Interfaz gráfica
        self._setup_ui()
        
        # Cargar datos de ejemplo
        self._cargar_datos_ejemplo()

    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        # Panel de entrada de síntomas
        frame_sintomas = ttk.LabelFrame(self.root, text="Registrar Síntomas")
        frame_sintomas.pack(padx=10, pady=5, fill="x")
        
        self.sintomas_vars = {}
        sintomas = ["fiebre", "tos", "dolor_cabeza", "perdida_olfato", "dolor_garganta"]
        
        for i, sintoma in enumerate(sintomas):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame_sintomas, text=sintoma, variable=var)
            chk.grid(row=i//3, column=i%3, sticky="w", padx=5, pady=2)
            self.sintomas_vars[sintoma] = var
        
        # Botones de acción
        frame_acciones = ttk.Frame(self.root)
        frame_acciones.pack(pady=10, fill="x")
        
        btn_prolog = ttk.Button(frame_acciones, text="Diagnóstico con Prolog", command=self.ejecutar_prolog)
        btn_prolog.pack(side="left", padx=5)
        
        btn_clips = ttk.Button(frame_acciones, text="Diagnóstico con CLIPS", command=self.ejecutar_clips)
        btn_clips.pack(side="left", padx=5)
        
        btn_integrado = ttk.Button(frame_acciones, text="Diagnóstico Integrado", command=self.ejecutar_integrado)
        btn_integrado.pack(side="left", padx=5)
        
        # Panel de resultados
        frame_resultados = ttk.LabelFrame(self.root, text="Resultados del Diagnóstico")
        frame_resultados.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.tree = ttk.Treeview(frame_resultados, columns=("Sistema", "Enfermedad", "Tratamiento", "Detalles"), show="headings")
        self.tree.heading("Sistema", text="Sistema")
        self.tree.heading("Enfermedad", text="Enfermedad")
        self.tree.heading("Tratamiento", text="Tratamiento")
        self.tree.heading("Detalles", text="Detalles")
        self.tree.pack(fill="both", expand=True)
        
        # Panel de explicación
        frame_explicacion = ttk.LabelFrame(self.root, text="Explicación del Razonamiento")
        frame_explicacion.pack(padx=10, pady=5, fill="both")
        
        self.txt_explicacion = tk.Text(frame_explicacion, height=8, wrap="word")
        self.txt_explicacion.pack(fill="both", expand=True)
    
    def _cargar_datos_ejemplo(self):
        """Carga datos de ejemplo en los motores"""
        # Datos para Prolog
        subprocess.run(["swipl", "-g", "assertz(sintoma(paciente1, fiebre))", "-t", "halt", "diagnostico_medico.pl"])
        subprocess.run(["swipl", "-g", "assertz(sintoma(paciente1, tos))", "-t", "halt", "diagnostico_medico.pl"])
        
        # Datos para CLIPS
        self.env.assert_string('(sintoma (id-paciente "paciente1") (nombre "fiebre") (valor yes))')
        self.env.assert_string('(sintoma (id-paciente "paciente1") (nombre "tos") (valor yes))')
    
    def ejecutar_prolog(self):
        """Ejecuta el diagnóstico usando Prolog"""
        self.tree.delete(*self.tree.get_children())
        self.txt_explicacion.delete(1.0, tk.END)
        
        try:
            # Consultar diagnóstico en Prolog
            resultados = list(self.prolog.query("diagnostico_completo(paciente1, Enfermedad, Recomendacion, Medicamento, Dias)"))
            
            if resultados:
                for sol in resultados:
                    self.tree.insert("", "end", values=(
                        "Prolog",
                        sol["Enfermedad"],
                        sol["Medicamento"],
                        f"{sol['Recomendacion']} por {sol['Dias']} días"
                    ))
                
                explicacion = "Razonamiento Prolog:\n"
                explicacion += "1. Se verificaron los síntomas del paciente\n"
                explicacion += "2. Se aplicaron las reglas de diagnóstico\n"
                explicacion += f"3. Se encontró coincidencia con {resultados[0]['Enfermedad']}\n"
                explicacion += "4. Se recuperó el tratamiento correspondiente"
                
                self.txt_explicacion.insert(tk.END, explicacion)
            else:
                messagebox.showinfo("Resultado", "No se encontraron diagnósticos en Prolog")
        except Exception as e:
            messagebox.showerror("Error", f"Error en Prolog: {str(e)}")
    
    def ejecutar_clips(self):
        """Ejecuta el diagnóstico usando CLIPS"""
        self.tree.delete(*self.tree.get_children())
        self.txt_explicacion.delete(1.0, tk.END)
        
        try:
            # Actualizar síntomas en CLIPS según la interfaz
            for sintoma, var in self.sintomas_vars.items():
                valor = "yes" if var.get() else "no"
                self.env.assert_string(f'(sintoma (id-paciente "paciente1") (nombre "{sintoma}") (valor {valor}))')
            
            # Ejecutar el motor de reglas
            self.env.run()
            
            # Obtener resultados
            tratamientos = []
            for fact in self.env.facts():
                if fact.template.name == "tratamiento":
                    tratamientos.append({
                        "enfermedad": fact["enfermedad"],
                        "recomendacion": fact["recomendacion"],
                        "medicamento": fact["medicamento"],
                        "dias": fact["dias"]
                    })
            
            if tratamientos:
                for t in tratamientos:
                    self.tree.insert("", "end", values=(
                        "CLIPS",
                        t["enfermedad"],
                        t["medicamento"],
                        f"{t['recomendacion']} por {t['dias']} días"
                    ))
                
                explicacion = "Razonamiento CLIPS:\n"
                explicacion += "1. Se cargaron los síntomas del paciente\n"
                explicacion += "2. Se activaron las reglas de producción\n"
                explicacion += "3. Se aplicaron las reglas de diagnóstico\n"
                explicacion += f"4. Se generó el tratamiento para {tratamientos[0]['enfermedad']}"
                
                self.txt_explicacion.insert(tk.END, explicacion)
            else:
                messagebox.showinfo("Resultado", "No se encontraron diagnósticos en CLIPS")
        except Exception as e:
            messagebox.showerror("Error", f"Error en CLIPS: {str(e)}")
    
    def ejecutar_integrado(self):
        """Ejecuta diagnóstico combinando Prolog y CLIPS"""
        self.ejecutar_prolog()
        self.ejecutar_clips()
        
        # Comparar resultados
        prolog_results = set()
        clips_results = set()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if values[0] == "Prolog":
                prolog_results.add(values[1])
            elif values[0] == "CLIPS":
                clips_results.add(values[1])
        
        coincidencias = prolog_results & clips_results
        diferencias = prolog_results ^ clips_results
        
        explicacion = "\n\nAnálisis Integrado:\n"
        if coincidencias:
            explicacion += f"Coincidencias encontradas: {', '.join(coincidencias)}\n"
        if diferencias:
            explicacion += f"Diferencias: {', '.join(diferencias)}\n"
        
        self.txt_explicacion.insert(tk.END, explicacion)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExperto(root)
    root.mainloop()