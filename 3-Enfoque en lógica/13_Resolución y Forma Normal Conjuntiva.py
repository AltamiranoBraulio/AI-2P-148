import re
from itertools import product
import matplotlib.pyplot as plt
import networkx as nx
from sympy.logic.boolalg import to_cnf, Or, And, Not
from sympy import symbols
from sympy.logic.inference import satisfiable

class LogicResolver:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.step_counter = 0
        self.node_labels = {}
        self.clause_history = []
        
    def parse_formula(self, formula_str):
        """Convierte una fórmula en string a una expresión sympy"""
        # Reemplazar conectores para compatibilidad con sympy
        formula_str = formula_str.replace('∧', '&').replace('∨', '|').replace('¬', '~')
        variables = sorted(set(re.findall(r'\b[A-Z]\b', formula_str)))
        var_symbols = symbols(' '.join(variables))
        if len(variables) == 1:
            var_symbols = (var_symbols,)  # Para manejar caso de una variable
        return eval(formula_str, {v: s for v, s in zip(variables, var_symbols)})
    
    def to_cnf_clauses(self, formula):
        """Convierte a FNC y extrae las cláusulas"""
        cnf = to_cnf(formula, simplify=True)
        if isinstance(cnf, And):
            return list(cnf.args)
        return [cnf]
    
    def draw_resolution_graph(self, title=""):
        plt.figure(figsize=(12, 8))
        pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph, pos, with_labels=True, labels=self.node_labels,
                node_size=2000, node_color='lightblue', font_size=10,
                arrowsize=20, arrowstyle='->')
        plt.title(title)
        plt.show()
    
    def add_graph_node(self, clause, prefix="C"):
        clause_str = self.clause_to_str(clause)
        node_id = f"{prefix}{self.step_counter}"
        self.graph.add_node(node_id)
        self.node_labels[node_id] = clause_str
        self.step_counter += 1
        return node_id
    
    def clause_to_str(self, clause):
        """Convierte una cláusula a string legible"""
        if isinstance(clause, Or):
            return " ∨ ".join(str(arg) for arg in clause.args)
        return str(clause)
    
    def find_complementary_pair(self, clause1, clause2):
        """Encuentra un par de literales complementarios entre dos cláusulas"""
        if not isinstance(clause1, Or):
            clause1 = Or(clause1)
        if not isinstance(clause2, Or):
            clause2 = Or(clause2)
            
        for lit1 in clause1.args:
            for lit2 in clause2.args:
                if lit1 == ~lit2 or ~lit1 == lit2:
                    return lit1, lit2
        return None
    
    def resolve_clauses(self, clause1, clause2, lit1, lit2):
        """Aplica la regla de resolución a dos cláusulas"""
        # Convertir a conjuntos para facilitar la manipulación
        set1 = set(clause1.args) if isinstance(clause1, Or) else {clause1}
        set2 = set(clause2.args) if isinstance(clause2, Or) else {clause2}
        
        # Eliminar los literales complementarios
        set1.discard(lit1)
        set2.discard(lit2 if lit2 in set2 else ~lit2)
        
        # Combinar las cláusulas
        resolved = set1.union(set2)
        
        if not resolved:
            return False  # Clausula vacía (contradicción)
        elif len(resolved) == 1:
            return resolved.pop()
        else:
            return Or(*resolved)
    
    def resolution(self, clauses, verbose=False, visualize=False):
        """Aplica el algoritmo de resolución"""
        self.graph = nx.DiGraph()
        self.node_labels = {}
        self.step_counter = 0
        self.clause_history = []
        
        # Agregar cláusulas iniciales al grafo
        node_ids = []
        for clause in clauses:
            node_id = self.add_graph_node(clause, "C")
            node_ids.append(node_id)
            self.clause_history.append((node_id, clause))
        
        if visualize:
            self.draw_resolution_graph("Cláusulas Iniciales")
        
        while True:
            new_clauses = []
            n = len(clauses)
            
            for i, j in product(range(n), repeat=2):
                if i >= j:  # Evitar comparar las mismas parejas dos veces
                    continue
                
                clause1 = clauses[i]
                clause2 = clauses[j]
                
                comp_pair = self.find_complementary_pair(clause1, clause2)
                if not comp_pair:
                    continue
                
                lit1, lit2 = comp_pair
                resolved = self.resolve_clauses(clause1, clause2, lit1, lit2)
                
                if resolved is False:
                    # Se encontró la cláusula vacía (contradicción)
                    node_id = self.add_graph_node("□", "R")
                    self.graph.add_edge(node_ids[i], node_id)
                    self.graph.add_edge(node_ids[j], node_id)
                    
                    if verbose:
                        print(f"Resolución entre {self.clause_to_str(clause1)} y {self.clause_to_str(clause2)}")
                        print("¡Se encontró la cláusula vacía (contradicción)!")
                    
                    if visualize:
                        self.draw_resolution_graph("Resolución - Contradicción Encontrada")
                    return False  # Insatisfactible
                
                # Verificar si la nueva cláusula ya existe
                if not any(resolved == c for c in clauses + new_clauses):
                    node_id = self.add_graph_node(resolved, "R")
                    new_clauses.append(resolved)
                    self.graph.add_edge(node_ids[i], node_id)
                    self.graph.add_edge(node_ids[j], node_id)
                    self.clause_history.append((node_id, resolved))
                    
                    if verbose:
                        print(f"Resolución entre {self.clause_to_str(clause1)} y {self.clause_to_str(clause2)}")
                        print(f"Nueva cláusula: {self.clause_to_str(resolved)}")
            
            if not new_clauses:
                if verbose:
                    print("No se pueden derivar más cláusulas nuevas")
                if visualize:
                    self.draw_resolution_graph("Resolución Completada - Sin Contradicción")
                return True  # Satisfactible
            
            if visualize:
                self.draw_resolution_graph("Paso de Resolución Intermedio")
            
            clauses.extend(new_clauses)
            node_ids.extend([f"R{self.step_counter - len(new_clauses) + i}" for i in range(len(new_clauses))])

# Ejemplo de uso interactivo
def interactive_resolution_example():
    print("""
    ██████╗ ███████╗███████╗ ██████╗ ██╗   ██╗██╗███████╗ █████╗ ██████╗ 
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║   ██║██║██╔════╝██╔══██╗██╔══██╗
    ██████╔╝█████╗  ███████╗██║   ██║██║   ██║██║███████╗███████║██████╔╝
    ██╔══██╗██╔══╝  ╚════██║██║   ██║╚██╗ ██╔╝██║╚════██║██╔══██║██╔═══╝ 
    ██║  ██║███████╗███████║╚██████╔╝ ╚████╔╝ ██║███████║██║  ██║██║     
    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝                                                                 
    """)
    
    resolver = LogicResolver()
    
    while True:
        print("\nOpciones:")
        print("1. Probar resolución con ejemplo predefinido")
        print("2. Ingresar fórmula manualmente")
        print("3. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            examples = {
                "1": "¬P ∨ Q, P, ¬Q",  # Contradicción
                "2": "P ∨ Q, ¬P ∨ R, ¬Q ∨ R, ¬R",  # Contradicción
                "3": "P ∨ Q, ¬P ∨ Q, P ∨ ¬Q, ¬P ∨ ¬Q",  # Contradicción
                "4": "P ∨ Q, ¬P ∨ R, ¬Q ∨ S",  # Satisfactible
                "5": "A ∨ B, ¬B ∨ C, ¬C ∨ D, ¬D ∨ E, ¬E"
            }
            
            print("\nEjemplos disponibles:")
            for k, v in examples.items():
                print(f"{k}. {v}")
            
            ex_choice = input("Seleccione un ejemplo (1-5): ")
            if ex_choice in examples:
                formula_str = examples[ex_choice]
                clauses = [resolver.parse_formula(f.strip()) for f in formula_str.split(',')]
            else:
                print("Opción no válida")
                continue
        elif choice == "2":
            formula_str = input("Ingrese fórmulas separadas por comas (ej: 'P ∨ Q, ¬P, ¬Q'): ")
            clauses = [resolver.parse_formula(f.strip()) for f in formula_str.split(',')]
        elif choice == "3":
            break
        else:
            print("Opción no válida")
            continue
        
        print("\nCláusulas en FNC:")
        for clause in clauses:
            print(f"- {resolver.clause_to_str(clause)}")
        
        print("\n¿Mostrar visualización paso a paso? (s/n)")
        visualize = input().lower() == 's'
        
        print("\n¿Mostrar detalles verbosos? (s/n)")
        verbose = input().lower() == 's'
        
        print("\nIniciando resolución...\n")
        result = resolver.resolution(clauses, verbose=verbose, visualize=visualize)
        
        if result:
            print("\nResultado: Las cláusulas son SATISFACTIBLES (no se encontró contradicción)")
        else:
            print("\nResultado: Las cláusulas son INSATISFACTIBLES (se encontró la cláusula vacía)")

if __name__ == "__main__":
    interactive_resolution_example()