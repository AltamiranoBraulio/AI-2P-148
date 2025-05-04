# Importación de librerías necesarias
from collections import deque  # Estructura de datos eficiente para la cola
import networkx as nx  # Para manejo y visualización de grafos
import matplotlib.pyplot as plt  # Para visualizaciones gráficas
import time  # Para medir tiempos de ejecución

class Rule:
    def __init__(self, premises, conclusion, description=""):
        """Inicializa una regla con premisas, conclusión y descripción opcional"""
        self.premises = set(premises)  # Usamos set para eliminar duplicados
        self.conclusion = conclusion
        self.description = description
    
    def __repr__(self):
        """Representación legible de la regla"""
        return f"{' ∧ '.join(self.premises)} ⇒ {self.conclusion}"

class KnowledgeEngine:
    def __init__(self):
        """Inicializa el motor de conocimiento"""
        self.rules = []  # Lista de todas las reglas
        self.facts = set()  # Conjunto de hechos conocidos
        self.graph = nx.DiGraph()  # Grafo para visualización
        self.rule_applications = []  # Historial de reglas aplicadas
        self.visualization_steps = []  # Pasos para visualización
    
    def add_rule(self, premises, conclusion, description=""):
        """Añade una nueva regla al sistema"""
        rule = Rule(premises, conclusion, description)
        self.rules.append(rule)
        return rule
    
    def add_fact(self, fact):
        """Añade un hecho a la base de conocimiento"""
        self.facts.add(fact)
    
    def reset(self):
        """Reinicia el sistema a su estado inicial"""
        self.facts.clear()
        self.rule_applications.clear()
        self.visualization_steps.clear()
    
    def forward_chaining(self, goal=None, visualize=False):
        """Encadenamiento hacia adelante"""
        self.rule_applications = []
        agenda = deque(self.facts)  # Hechos por procesar
        new_facts = set(self.facts)  # Hechos conocidos
        inferred = set()  # Hechos recién derivados
        
        if visualize:
            self._init_visualization()
        
        while agenda:
            current_fact = agenda.popleft()
            
            if visualize:
                self._add_visualization_step(f"Procesando hecho: {current_fact}")
            
            for rule in self.rules:
                if current_fact in rule.premises and rule.premises.issubset(new_facts):
                    if rule.conclusion not in new_facts.union(inferred):
                        inferred.add(rule.conclusion)
                        agenda.append(rule.conclusion)
                        self.rule_applications.append(rule)
                        
                        if visualize:
                            self._add_visualization_step(
                                f"Aplicando regla: {rule.description or rule}",
                                f"Derivado nuevo hecho: {rule.conclusion}"
                            )
            
            new_facts.add(current_fact)
            
            if goal and goal in new_facts:
                if visualize:
                    self._add_visualization_step(f"¡Meta alcanzada: {goal}!")
                return True
        
        return goal in new_facts if goal else new_facts
    
    def backward_chaining(self, goal, visited=None, depth=0, visualize=False):
        """Encadenamiento hacia atrás"""
        if visited is None:
            visited = set()
            if visualize:
                self._init_visualization()
                self._add_visualization_step(f"Iniciando búsqueda para: {goal}")
        
        if goal in self.facts:
            if visualize:
                self._add_visualization_step(f"Hecho conocido: {goal}")
            return True
        
        if goal in visited:
            if visualize:
                self._add_visualization_step(f"Ciclo detectado en: {goal}")
            return False
        
        visited.add(goal)
        
        if visualize:
            self._add_visualization_step(f"Explorando formas de probar: {goal}")
        
        for rule in self.rules:
            if rule.conclusion == goal:
                if visualize:
                    self._add_visualization_step(
                        f"Considerando regla: {rule.description or rule}",
                        f"Para probar: {goal}"
                    )
                
                all_premises_proven = True
                for premise in rule.premises:
                    if visualize:
                        self._add_visualization_step(f"Intentando probar premisa: {premise}")
                    
                    if not self.backward_chaining(premise, visited, depth+1, visualize):
                        all_premises_proven = False
                        if visualize:
                            self._add_visualization_step(f"Fallo al probar premisa: {premise}")
                        break
                
                if all_premises_proven:
                    if visualize:
                        self._add_visualization_step(f"¡Todas las premisas probadas para: {goal}!")
                    return True
        
        if visualize:
            self._add_visualization_step(f"No se pudo probar: {goal}")
        return False
    
    def _init_visualization(self):
        """Inicializa los pasos de visualización"""
        self.visualization_steps = []
    
    def _add_visualization_step(self, *messages):
        """Añade un paso de visualización"""
        step = "\n".join(messages)
        self.visualization_steps.append(step)
        print(step)
    
    def visualize_search(self, engine_type):
        """Genera visualización del proceso de búsqueda"""
        plt.figure(figsize=(12, 8))
        
        if engine_type == "forward":
            self._visualize_forward_chaining()
        elif engine_type == "backward":
            self._visualize_backward_chaining()
        
        plt.show()
    
    def _visualize_forward_chaining(self):
        """Visualización para encadenamiento hacia adelante"""
        G = nx.DiGraph()
        node_counter = 0
        node_ids = {}
        
        # Añadir hechos iniciales
        for fact in self.facts:
            node_id = f"F{node_counter}"
            G.add_node(node_id, label=fact, type="initial")
            node_ids[fact] = node_id
            node_counter += 1
        
        # Añadir reglas y hechos derivados
        for i, rule in enumerate(self.rule_applications):
            rule_node = f"R{i}"
            G.add_node(rule_node, label=str(rule), type="rule")
            
            # Conectar premisas a regla
            for premise in rule.premises:
                if premise in node_ids:
                    G.add_edge(node_ids[premise], rule_node)
            
            # Añadir conclusión
            concl_node = f"C{i}"
            G.add_node(concl_node, label=rule.conclusion, type="derived")
            G.add_edge(rule_node, concl_node)
            node_ids[rule.conclusion] = concl_node
        
        # Asignar colores
        color_map = []
        for node in G.nodes():
            node_type = G.nodes[node]["type"]
            color_map.append("lightgreen" if node_type == "initial" else 
                           "lightblue" if node_type == "rule" else 
                           "lightcoral")
        
        pos = nx.spring_layout(G, seed=42)  # Diseño consistente
        labels = {n: G.nodes[n]["label"] for n in G.nodes()}
        
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=2500,
                node_color=color_map, font_size=10, arrowsize=20)
        plt.title("Encadenamiento Hacia Adelante - Proceso de Inferencia")
    
    def _visualize_backward_chaining(self):
        """Visualización para encadenamiento hacia atrás"""
        G = nx.DiGraph()
        current_parent = None
        parent_stack = []
        
        for step in self.visualization_steps:
            if step.startswith("Intentando probar premisa:"):
                premise = step.split(":")[1].strip()
                G.add_edge(current_parent, premise)
                parent_stack.append(current_parent)
                current_parent = premise
            elif step.startswith(("Fallo al probar premisa:", "Hecho conocido:")):
                current_parent = parent_stack.pop() if parent_stack else None
        
        pos = nx.spring_layout(G, seed=42)  # Diseño consistente
        nx.draw(G, pos, with_labels=True, node_size=2000, 
               node_color="lightyellow", font_size=10, arrowsize=20)
        plt.title("Encadenamiento Hacia Atrás - Árbol de Búsqueda")

    def interactive_demo(self):
        """Interfaz interactiva para el sistema"""
        print("""
        ███████╗███╗   ██╗ ██████╗ ██████╗ ███████╗██████╗ ███████╗
        ██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔════╝██╔══██╗██╔════╝
        █████╗  ██╔██╗ ██║██║  ███╗██████╔╝█████╗  ██████╔╝███████╗
        ██╔══╝  ██║╚██╗██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗╚════██║
        ███████╗██║ ╚████║╚██████╔╝██║  ██║███████╗██║  ██║███████║
        ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
        """)
        
        while True:
            print("\nMenu Principal:")
            print("1. Configurar Sistema Experto")
            print("2. Encadenamiento Hacia Adelante")
            print("3. Encadenamiento Hacia Atrás")
            print("4. Mostrar Base de Conocimiento")
            print("5. Salir")
            
            choice = input("Seleccione una opción: ")
            
            if choice == "1":
                self._setup_knowledge()
            elif choice == "2":
                self._run_forward_chaining()
            elif choice == "3":
                self._run_backward_chaining()
            elif choice == "4":
                self._show_knowledge()
            elif choice == "5":
                break
            else:
                print("Opción no válida, intente nuevamente.")
    
    def _setup_knowledge(self):
        """Configura la base de conocimiento"""
        print("\nConfiguración del Sistema Experto")
        self.reset()
        
        print("\nIngrese hechos iniciales (separados por comas):")
        facts_input = input("Ej: hecho1, hecho2, hecho3\n> ")
        for fact in [f.strip() for f in facts_input.split(",") if f.strip()]:
            self.add_fact(fact)
        
        print("\nIngrese reglas (una por línea), formato: premisa1 ∧ premisa2 ⇒ conclusión")
        print("Escriba 'fin' para terminar")
        while True:
            rule_input = input("Regla> ")
            if rule_input.lower() == 'fin':
                break
            
            try:
                parts = rule_input.split("⇒")
                premises = [p.strip() for p in parts[0].split("∧")]
                conclusion = parts[1].strip()
                desc = input("Descripción (opcional): ")
                self.add_rule(premises, conclusion, desc)
                print("Regla añadida!")
            except:
                print("Formato incorrecto. Use: premisa1 ∧ premisa2 ⇒ conclusión")
    
    def _run_forward_chaining(self):
        """Ejecuta encadenamiento hacia adelante"""
        print("\nEncadenamiento Hacia Adelante")
        goal = input("Meta a verificar (opcional): ")
        visualize = input("¿Mostrar visualización? (s/n): ").lower() == 's'
        
        start_time = time.time()
        
        if goal:
            result = self.forward_chaining(goal=goal, visualize=visualize)
            print(f"\nResultado: La meta '{goal}' es {'alcanzable' if result else 'no alcanzable'}")
        else:
            derived_facts = self.forward_chaining(visualize=visualize)
            print("\nHechos derivados:")
            for fact in derived_facts:
                print(f"- {fact}")
        
        print(f"\nTiempo: {time.time() - start_time:.2f} segundos")
        
        if visualize:
            self.visualize_search("forward")
    
    def _run_backward_chaining(self):
        """Ejecuta encadenamiento hacia atrás"""
        print("\nEncadenamiento Hacia Atrás")
        goal = input("Meta a verificar: ").strip()
        if not goal:
            print("Debe especificar una meta")
            return
        
        visualize = input("¿Mostrar visualización? (s/n): ").lower() == 's'
        
        start_time = time.time()
        
        result = self.backward_chaining(goal, visualize=visualize)
        print(f"\nResultado: La meta '{goal}' es {'demostrable' if result else 'no demostrable'}")
        
        print(f"\nTiempo: {time.time() - start_time:.2f} segundos")
        
        if visualize:
            self.visualize_search("backward")
    
    def _show_knowledge(self):
        """Muestra la base de conocimiento actual"""
        print("\nBase de Conocimiento:")
        
        print("\nHechos iniciales:")
        for fact in self.facts:
            print(f"- {fact}")
        
        print("\nReglas:")
        for i, rule in enumerate(self.rules, 1):
            print(f"{i}. {rule.description or rule}")

if __name__ == "__main__":
    engine = KnowledgeEngine()
    
    # Ejemplo predeterminado
    engine.add_fact("fiebre")
    engine.add_fact("dolor_de_cabeza")
    
    engine.add_rule(["fiebre", "dolor_de_cabeza"], "gripe", 
                   "Fiebre + dolor de cabeza → gripe")
    engine.add_rule(["fiebre", "dolor_de_garganta"], "amigdalitis",
                   "Fiebre + dolor de garganta → amigdalitis")
    engine.add_rule(["gripe"], "reposo", "Gripe → reposo")
    engine.add_rule(["amigdalitis"], "antibioticos", "Amigdalitis → antibióticos")
    
    engine.interactive_demo()