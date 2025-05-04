class FirstOrderLogicEngine:
    def __init__(self, domain):
        self.domain = domain  # Lista de elementos del dominio (ej: [1, 2, 3, "Sócrates", ...])
        self.predicates = {}  # Diccionario de predicados: {"Humano": lambda x: x == "Sócrates", ...}

    def add_predicate(self, name, condition):
        """Añade un predicado personalizado."""
        self.predicates[name] = condition

    def evaluate_quantifier(self, quantifier, variable, formula):
        """Evalúa ∀ (para todo) o ∃ (existe) sobre el dominio."""
        results = []
        for element in self.domain:
            # Asigna el elemento a la variable en la fórmula
            local_vars = {variable: element}
            result = self.evaluate_formula(formula, local_vars)
            results.append(result)

        if quantifier == "∀":
            return all(results)  # True si TODOS cumplen la fórmula
        elif quantifier == "∃":
            return any(results)  # True si AL MENOS UNO cumple la fórmula
        else:
            raise ValueError("Cuantificador no válido. Usa '∀' o '∃'.")

    def evaluate_formula(self, formula, local_vars=None):
        """Evalúa una fórmula lógica con variables/predicados."""
        if local_vars is None:
            local_vars = {}

        if isinstance(formula, tuple):
            operator, *args = formula
            if operator in ["∧", "∨", "→", "¬"]:  # Conectivas lógicas
                if operator == "¬":
                    return not self.evaluate_formula(args[0], local_vars)
                a, b = [self.evaluate_formula(arg, local_vars) for arg in args]
                return {
                    "∧": lambda x, y: x and y,
                    "∨": lambda x, y: x or y,
                    "→": lambda x, y: (not x) or y,
                }[operator](a, b)
            elif operator in ["∀", "∃"]:  # Cuantificadores
                variable, subformula = args
                return self.evaluate_quantifier(operator, variable, subformula)
            elif operator in self.predicates:  # Predicados definidos
                arg = local_vars.get(args[0], args[0])
                return self.predicates[operator](arg)
            else:
                raise ValueError(f"Operador '{operator}' no reconocido.")
        else:
            return local_vars.get(formula, formula)  # Valor concreto (ej: 5, "Sócrates")

# =====================================
# Ejemplo 1: "Todos los humanos son mortales"
# =====================================
engine = FirstOrderLogicEngine(["Sócrates", "Platón", "Perro"])

# Definimos los predicados:
engine.add_predicate("Humano", lambda x: x in ["Sócrates", "Platón"])
engine.add_predicate("Mortal", lambda x: x != "Perro")

# Fórmula: ∀x (Humano(x) → Mortal(x))
formula = ("∀", "x", ("→", ("Humano", "x"), ("Mortal", "x")))
result = engine.evaluate_formula(formula)
print("\nEjemplo 1:")
print("¿Todos los humanos son mortales?", result)  # True (Sócrates y Platón son mortales)

# =====================================
# Ejemplo 2: "Existe un número par mayor que 10"
# =====================================
engine_numbers = FirstOrderLogicEngine([2, 5, 11, 12, 13])

# Definimos predicados:
engine_numbers.add_predicate("Par", lambda x: x % 2 == 0)
engine_numbers.add_predicate(">10", lambda x: x > 10)

# Fórmula: ∃x (Par(x) ∧ >10(x))
formula2 = ("∃", "x", ("∧", ("Par", "x"), (">10", "x")))
result2 = engine_numbers.evaluate_formula(formula2)
print("\nEjemplo 2:")
print("¿Existe un número par > 10?", result2)  # True (el 12 cumple)

# =====================================
# Ejemplo 3: "No todos los pájaros vuelan" (¬∀x (Pájaro(x) → Vuela(x)))
# =====================================
engine_birds = FirstOrderLogicEngine(["Pingüino", "Águila", "Kiwi"])

engine_birds.add_predicate("Pájaro", lambda x: True)  # Todos son pájaros
engine_birds.add_predicate("Vuela", lambda x: x != "Pingüino" and x != "Kiwi")

formula3 = ("¬", ("∀", "x", ("→", ("Pájaro", "x"), ("Vuela", "x"))))
result3 = engine_birds.evaluate_formula(formula3)
print("\nEjemplo 3:")
print("¿No todos los pájaros vuelan?", result3)  # True (el pingüino y el kiwi no vuelan)