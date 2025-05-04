from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from IPython.display import display, HTML
import pandas as pd

class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.ontology = defaultdict(list)  # Relaciones semánticas
        self.certainty_factors = {}  # Factores de certeza para hechos
        self.rule_strengths = {}  # Fortalezas de las reglas
        
    def add_fact(self, fact, certainty=1.0):
        """Añade un hecho con un factor de certeza opcional"""
        self.facts.add(fact)
        self.certainty_factors[fact] = certainty
        
    def add_rule(self, premises, conclusion, description="", strength=1.0):
        """Añade una regla con premisas, conclusión y fortaleza"""
        rule = {'premises': set(premises), 
                'conclusion': conclusion,
                'description': description}
        self.rules.append(rule)
        self.rule_strengths[len(self.rules)-1] = strength
        
    def add_ontology_relation(self, concept1, relation, concept2):
        """Establece relaciones semánticas entre conceptos"""
        self.ontology[concept1].append((relation, concept2))
        
    def query(self, goal, inference_type='forward', visualize=False):
        """Consulta el sistema experto"""
        if inference_type == 'forward':
            return self.forward_chain(goal, visualize)
        elif inference_type == 'backward':
            return self.backward_chain(goal, visualize)
        else:
            raise ValueError("Tipo de inferencia no válido")
            
    def forward_chain(self, goal=None, visualize=False):
        """Encadenamiento hacia adelante con factores de certeza"""
        agenda = list(self.facts)
        new_facts = set(self.facts)
        inferred_facts = set()
        derivation_graph = nx.DiGraph()
        
        if visualize:
            self._init_visualization()
        
        while agenda:
            current_fact = agenda.pop(0)
            
            for i, rule in enumerate(self.rules):
                if current_fact in rule['premises'] and rule['premises'].issubset(new_facts):
                    conclusion = rule['conclusion']
                    
                    # Calcular factor de certeza de la conclusión
                    min_premise_cf = min(self.certainty_factors[p] for p in rule['premises'])
                    conclusion_cf = min_premise_cf * self.rule_strengths[i]
                    
                    if conclusion not in new_facts.union(inferred_facts):
                        inferred_facts.add(conclusion)
                        agenda.append(conclusion)
                        self.certainty_factors[conclusion] = conclusion_cf
                        
                        # Registrar para visualización
                        if visualize:
                            derivation_graph.add_node(current_fact, type='fact')
                            derivation_graph.add_node(conclusion, type='fact')
                            derivation_graph.add_node(i, type='rule', label=rule['description'])
                            derivation_graph.add_edge(current_fact, i)
                            derivation_graph.add_edge(i, conclusion)
                        
                    elif conclusion_cf > self.certainty_factors[conclusion]:
                        # Actualizar si encontramos un camino más confiable
                        self.certainty_factors[conclusion] = conclusion_cf
            
            new_facts.add(current_fact)
            
            if goal and goal in new_facts:
                break
        
        if visualize:
            self._visualize_derivation(derivation_graph)
            
        if goal:
            return goal in new_facts, self.certainty_factors.get(goal, 0)
        return new_facts, {fact: self.certainty_factors[fact] for fact in new_facts}
    
    def backward_chain(self, goal, visited=None, visualize=False):
        """Encadenamiento hacia atrás con explicación"""
        if visited is None:
            visited = set()
            if visualize:
                self.explanation_graph = nx.DiGraph()
                self.explanation_graph.add_node(goal, type='goal')
        
        if goal in self.facts:
            if visualize:
                self.explanation_graph.nodes[goal]['type'] = 'known_fact'
            return True, self.certainty_factors.get(goal, 0)
        
        if goal in visited:
            return False, 0
        
        visited.add(goal)
        max_cf = 0
        best_rule = None
        
        for i, rule in enumerate(self.rules):
            if rule['conclusion'] == goal:
                all_premises_proven = True
                total_rule_cf = self.rule_strengths[i]
                min_premise_cf = 1.0
                
                if visualize:
                    self.explanation_graph.add_node(i, type='rule', label=rule['description'])
                    self.explanation_graph.add_edge(i, goal)
                
                for premise in rule['premises']:
                    proven, premise_cf = self.backward_chain(premise, visited, visualize)
                    if not proven:
                        all_premises_proven = False
                        break
                    min_premise_cf = min(min_premise_cf, premise_cf)
                    
                    if visualize:
                        self.explanation_graph.add_edge(premise, i)
                
                if all_premises_proven:
                    current_cf = min_premise_cf * total_rule_cf
                    if current_cf > max_cf:
                        max_cf = current_cf
                        best_rule = rule
        
        if max_cf > 0:
            self.certainty_factors[goal] = max_cf
            if visualize:
                self.explanation_graph.nodes[goal]['cf'] = f"CF: {max_cf:.2f}"
            return True, max_cf
        
        return False, 0
    
    def _visualize_derivation(self, graph):
        """Visualiza el proceso de inferencia"""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph, seed=42)
        
        node_colors = []
        node_sizes = []
        labels = {}
        
        for node in graph.nodes():
            if graph.nodes[node].get('type') == 'fact':
                node_colors.append('lightgreen')
                node_sizes.append(2000)
                labels[node] = f"{node}\nCF: {self.certainty_factors.get(node, 0):.2f}"
            elif graph.nodes[node].get('type') == 'rule':
                node_colors.append('lightblue')
                node_sizes.append(3000)
                labels[node] = graph.nodes[node].get('label', f"Regla {node}")
            else:
                node_colors.append('lightcoral')
                node_sizes.append(2500)
                labels[node] = str(node)
        
        nx.draw(graph, pos, with_labels=True, labels=labels, node_size=node_sizes,
                node_color=node_colors, font_size=10, arrowsize=20)
        plt.title("Proceso de Inferencia")
        plt.show()
    
    def explain(self, goal):
        """Genera una explicación de cómo se llegó a una conclusión"""
        self.explanation_graph = nx.DiGraph()
        proven, cf = self.backward_chain(goal, visualize=True)
        
        if not proven:
            return f"No se pudo probar {goal}"
        
        explanation = [f"Conclusión: {goal} (CF: {cf:.2f})"]
        
        # Recorrer el grafo de explicación para construir la narrativa
        for node in nx.topological_sort(self.explanation_graph):
            if self.explanation_graph.nodes[node].get('type') == 'rule':
                rule_desc = self.explanation_graph.nodes[node].get('label', '')
                premises = []
                for pred in self.explanation_graph.predecessors(node):
                    premises.append(f"{pred} (CF: {self.certainty_factors.get(pred, 0):.2f})")
                explanation.append(f"\nRegla: {rule_desc}")
                explanation.append(f"Premisas: {', '.join(premises)}")
        
        return "\n".join(explanation)
    
    def to_dataframe(self):
        """Representa la base de conocimiento como DataFrame"""
        rules_data = []
        for i, rule in enumerate(self.rules):
            rules_data.append({
                'Regla': f"R{i}",
                'Premisas': " ∧ ".join(rule['premises']),
                'Conclusión': rule['conclusion'],
                'Descripción': rule['description'],
                'Fortaleza': self.rule_strengths.get(i, 1.0)
            })
        
        facts_data = [{'Hecho': fact, 'CF': cf} for fact, cf in self.certainty_factors.items()]
        
        return {
            'Reglas': pd.DataFrame(rules_data),
            'Hechos': pd.DataFrame(facts_data)
        }

# Ejemplo: Sistema Experto Médico
def build_medical_knowledge_base():
    kb = KnowledgeBase()
    
    # Sintomas y hechos iniciales
    kb.add_fact("fiebre", 0.9)
    kb.add_fact("dolor_cabeza", 0.8)
    kb.add_fact("dolor_garganta", 0.7)
    kb.add_fact("congestion_nasal", 0.6)
    kb.add_fact("tos", 0.7)
    
    # Reglas de diagnóstico
    kb.add_rule(["fiebre", "dolor_cabeza", "congestion_nasal"], "gripe",
               "Fiebre con dolor de cabeza y congestión sugiere gripe", 0.8)
    kb.add_rule(["fiebre", "dolor_garganta"], "amigdalitis",
               "Fiebre con dolor de garganta sugiere amigdalitis", 0.9)
    kb.add_rule(["tos", "congestion_nasal"], "resfriado",
               "Tos con congestión sugiere resfriado común", 0.7)
    kb.add_rule(["gripe"], "reposo_fluidos",
               "Para gripe se recomienda reposo y fluidos", 0.95)
    kb.add_rule(["amigdalitis"], "antibioticos",
               "Para amigdalitis se necesitan antibióticos", 0.85)
    kb.add_rule(["resfriado"], "antihistaminicos",
               "Para resfriado se recomiendan antihistamínicos", 0.75)
    
    # Ontología médica
    kb.add_ontology_relation("gripe", "es_un", "enfermedad_viral")
    kb.add_ontology_relation("amigdalitis", "es_un", "infeccion_bacteriana")
    kb.add_ontology_relation("resfriado", "es_un", "enfermedad_viral")
    kb.add_ontology_relation("antibioticos", "trata", "infeccion_bacteriana")
    kb.add_ontology_relation("antihistaminicos", "alivia", "sintomas_resfriado")
    
    return kb

# Interfaz interactiva
def expert_system_demo():
    kb = build_medical_knowledge_base()
    
    print("""
    ███████╗██╗  ██╗███████╗██████╗ ████████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
    ██╔════╝╚██╗██╔╝██╔════╝██╔══██╗╚══██╔══╝    ██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║
    █████╗   ╚███╔╝ █████╗  ██████╔╝   ██║       █████╗  ██║   ██║███████╗   ██║   █████╗  ██╔████╔██║
    ██╔══╝   ██╔██╗ ██╔══╝  ██╔═══╝    ██║       ██╔══╝  ██║   ██║╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
    ███████╗██╔╝ ██╗███████╗██║        ██║       ██║     ╚██████╔╝███████║   ██║   ███████╗██║ ╚═╝ ██║
    ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝        ╚═╝       ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
    """)
    
    while True:
        print("\nMenu del Sistema Experto Médico:")
        print("1. Consultar diagnóstico")
        print("2. Ver explicación de diagnóstico")
        print("3. Mostrar base de conocimiento")
        print("4. Añadir nuevo síntoma")
        print("5. Salir")
        
        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            symptoms = input("Ingrese síntomas (separados por comas): ").split(',')
            for symptom in symptoms:
                symptom = symptom.strip()
                if symptom:
                    kb.add_fact(symptom, 0.8)  # Asumir CF de 0.8 para nuevos síntomas
            
            print("\nRealizando diagnóstico...")
            result, cf = kb.forward_chain()
            
            print("\nPosibles diagnósticos:")
            for diagnosis in ["gripe", "amigdalitis", "resfriado"]:
                if diagnosis in result:
                    print(f"- {diagnosis} (CF: {cf[diagnosis]:.2f})")
            
            treatments = []
            for treatment in ["reposo_fluidos", "antibioticos", "antihistaminicos"]:
                if treatment in result:
                    treatments.append((treatment, cf[treatment]))
            
            if treatments:
                print("\nTratamientos recomendados:")
                for treatment, treatment_cf in treatments:
                    print(f"- {treatment} (CF: {treatment_cf:.2f})")
            else:
                print("\nNo se encontraron tratamientos recomendados")
        
        elif choice == "2":
            diagnosis = input("Ingrese el diagnóstico a explicar: ").strip()
            explanation = kb.explain(diagnosis)
            print(f"\nExplicación para {diagnosis}:\n{explanation}")
            
            # Visualización del grafo de explicación
            if hasattr(kb, 'explanation_graph'):
                plt.figure(figsize=(10, 8))
                pos = nx.spring_layout(kb.explanation_graph, seed=42)
                
                node_colors = []
                labels = {}
                for node in kb.explanation_graph.nodes():
                    node_type = kb.explanation_graph.nodes[node].get('type', '')
                    if node_type == 'goal':
                        node_colors.append('red')
                        labels[node] = f"Meta: {node}"
                    elif node_type == 'known_fact':
                        node_colors.append('green')
                        labels[node] = f"Hecho: {node}"
                    elif node_type == 'rule':
                        node_colors.append('blue')
                        labels[node] = kb.explanation_graph.nodes[node].get('label', node)
                    else:
                        node_colors.append('gray')
                        labels[node] = str(node)
                
                nx.draw(kb.explanation_graph, pos, with_labels=True, labels=labels,
                        node_color=node_colors, font_size=10, node_size=2500)
                plt.title(f"Grafo de Explicación para {diagnosis}")
                plt.show()
        
        elif choice == "3":
            data = kb.to_dataframe()
            print("\nHechos conocidos:")
            display(data['Hechos'])
            print("\nReglas:")
            display(data['Reglas'])
        
        elif choice == "4":
            symptom = input("Nuevo síntoma: ").strip()
            cf = float(input("Factor de certeza (0-1): "))
            kb.add_fact(symptom, cf)
            print(f"Síntoma '{symptom}' añadido con CF={cf:.2f}")
        
        elif choice == "5":
            break
        
        else:
            print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    expert_system_demo()