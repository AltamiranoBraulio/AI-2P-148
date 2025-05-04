"""
====================================================
ANALIZADOR SINTÁCTICO (PARSER DESCENDENTE RECURSIVO)
====================================================
Objetivo: Validar la estructura sintáctica de un programa según una gramática
definida y construir un Árbol de Sintaxis Abstracta (AST).

Gramática de ejemplo:
program        → statement*
statement     → expr_stmt | if_stmt | while_stmt | block
expr_stmt     → expression ";"
if_stmt       → "if" "(" expression ")" block ("else" block)?
while_stmt    → "while" "(" expression ")" block
block         → "{" statement* "}"
expression    → assignment
assignment    → IDENTIFIER "=" assignment | logic_or
logic_or      → logic_and ("||" logic_and)*
logic_and     → equality ("&&" equality)*
equality      → comparison (("!=" | "==") comparison)*
comparison    → term ((">" | ">=" | "<" | "<=") term)*
term          → factor (("+" | "-") factor)*
factor        → unary (("*" | "/") unary)*
unary         → ("!" | "-") unary | primary
primary       → NUMBER | STRING | IDENTIFIER | "(" expression ")" | "true" | "false"
"""

# ======================
# 1. DEFINICIÓN DE CLASES PARA EL AST
# ======================
class NodoAST:
    """Clase base para todos los nodos del Árbol de Sintaxis Abstracta"""
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class Programa(NodoAST):
    """Representa un programa completo (lista de statements)"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Programa({self.statements})"

class ExpresionDeclaracion(NodoAST):
    """Representa una declaración que contiene una expresión (ej: 'x = 5;')"""
    def __init__(self, expresion):
        self.expresion = expresion
    
    def __repr__(self):
        return f"ExpresionDeclaracion({self.expresion})"

class IfDeclaracion(NodoAST):
    """Representa una declaración if (condicional)"""
    def __init__(self, condicion, bloque_if, bloque_else=None):
        self.condicion = condicion
        self.bloque_if = bloque_if
        self.bloque_else = bloque_else
    
    def __repr__(self):
        return f"IfDeclaracion({self.condicion}, {self.bloque_if}, else={self.bloque_else})"

class WhileDeclaracion(NodoAST):
    """Representa una declaración while (bucle)"""
    def __init__(self, condicion, bloque):
        self.condicion = condicion
        self.bloque = bloque
    
    def __repr__(self):
        return f"WhileDeclaracion({self.condicion}, {self.bloque})"

class Bloque(NodoAST):
    """Representa un bloque de código entre llaves"""
    def __init__(self, declaraciones):
        self.declaraciones = declaraciones
    
    def __repr__(self):
        return f"Bloque({self.declaraciones})"

# Clases para expresiones
class Asignacion(NodoAST):
    """Representa una asignación de variable (ej: 'x = 5')"""
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor
    
    def __repr__(self):
        return f"Asignacion({self.nombre}, {self.valor})"

class Binaria(NodoAST):
    """Representa una operación binaria (ej: '5 + 3')"""
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha
    
    def __repr__(self):
        return f"Binaria({self.izquierda}, '{self.operador}', {self.derecha})"

class Unaria(NodoAST):
    """Representa una operación unaria (ej: '-5' o '!true')"""
    def __init__(self, operador, derecha):
        self.operador = operador
        self.derecha = derecha
    
    def __repr__(self):
        return f"Unaria('{self.operador}', {self.derecha})"

class Literal(NodoAST):
    """Representa un valor literal (número, string, booleano)"""
    def __init__(self, valor):
        self.valor = valor
    
    def __repr__(self):
        return f"Literal({self.valor})"

class Variable(NodoAST):
    """Representa una variable (identificador)"""
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __repr__(self):
        return f"Variable('{self.nombre}')"

# ======================
# 2. CLASE DEL PARSER
# ======================
class Parser:
    def __init__(self, tokens):
        """
        Inicializa el parser con la lista de tokens a analizar.
        
        Args:
            tokens (list): Lista de tokens generados por el lexer
        """
        self.tokens = tokens
        self.posicion_actual = 0
        self.token_actual = self.tokens[0] if tokens else None
    
    def _avanzar(self):
        """Avanza al siguiente token en la lista"""
        self.posicion_actual += 1
        if self.posicion_actual < len(self.tokens):
            self.token_actual = self.tokens[self.posicion_actual]
        else:
            self.token_actual = None
    
    def _consumir(self, tipo_token, mensaje_error):
        """
        Verifica que el token actual sea del tipo esperado y avanza.
        Si no coincide, lanza un error de sintaxis.
        
        Args:
            tipo_token (str): Tipo de token esperado
            mensaje_error (str): Mensaje a mostrar si hay error
        """
        if self.token_actual and self.token_actual['tipo'] == tipo_token:
            token = self.token_actual
            self._avanzar()
            return token
        else:
            linea = self.token_actual['linea'] if self.token_actual else "EOF"
            columna = self.token_actual['columna'] if self.token_actual else "EOF"
            raise SyntaxError(f"Error de sintaxis en línea {linea}, columna {columna}: {mensaje_error}")
    
    def _coincide(self, *tipos):
        """
        Verifica si el token actual coincide con alguno de los tipos dados.
        
        Args:
            *tipos: Tipos de token a verificar
            
        Returns:
            bool: True si coincide, False en caso contrario
        """
        if not self.token_actual:
            return False
        return self.token_actual['tipo'] in tipos
    
    # ======================
    # 3. MÉTODOS DE PARSING (DESCENDENTE RECURSIVO)
    # ======================
    def parsear(self):
        """
        Inicia el análisis sintáctico y construye el AST.
        
        Returns:
            Programa: Nodo raíz del AST
        """
        declaraciones = []
        while not self._coincide('EOF'):
            declaraciones.append(self._declaracion())
        return Programa(declaraciones)
    
    def _declaracion(self):
        """Parsear una declaración (statement)"""
        if self._coincide('IF'):
            return self._declaracion_if()
        elif self._coincide('WHILE'):
            return self._declaracion_while()
        elif self._coincide('LLAVE_IZQ'):
            return self._bloque()
        else:
            return self._declaracion_expresion()
    
    def _declaracion_expresion(self):
        """Parsear una declaración de expresión (ej: 'x = 5;')"""
        expr = self._expresion()
        self._consumir('PUNTO_Y_COMA', "Se esperaba ';' después de la expresión")
        return ExpresionDeclaracion(expr)
    
    def _declaracion_if(self):
        """Parsear una declaración if"""
        self._consumir('IF', "Se esperaba 'if'")
        self._consumir('PARENTESIS_IZQ', "Se esperaba '(' después de 'if'")
        condicion = self._expresion()
        self._consumir('PARENTESIS_DER', "Se esperaba ')' después de la condición")
        bloque_if = self._bloque()
        
        bloque_else = None
        if self._coincide('ELSE'):
            self._avanzar()
            bloque_else = self._bloque()
        
        return IfDeclaracion(condicion, bloque_if, bloque_else)
    
    def _declaracion_while(self):
        """Parsear una declaración while"""
        self._consumir('WHILE', "Se esperaba 'while'")
        self._consumir('PARENTESIS_IZQ', "Se esperaba '(' después de 'while'")
        condicion = self._expresion()
        self._consumir('PARENTESIS_DER', "Se esperaba ')' después de la condición")
        bloque = self._bloque()
        return WhileDeclaracion(condicion, bloque)
    
    def _bloque(self):
        """Parsear un bloque de código entre llaves"""
        self._consumir('LLAVE_IZQ', "Se esperaba '{'")
        declaraciones = []
        while not self._coincide('LLAVE_DER') and not self._coincide('EOF'):
            declaraciones.append(self._declaracion())
        self._consumir('LLAVE_DER', "Se esperaba '}'")
        return Bloque(declaraciones)
    
    # ======================
    # 4. MÉTODOS PARA EXPRESIONES
    # ======================
    def _expresion(self):
        """Parsear una expresión (inicia la cadena de precedencia)"""
        return self._asignacion()
    
    def _asignacion(self):
        """Parsear una asignación (x = 5)"""
        expr = self._logic_or()
        
        if self._coincide('OPERADOR_ASIGNACION'):
            operador = self.token_actual['valor']
            self._avanzar()
            valor = self._asignacion()
            
            if isinstance(expr, Variable):
                return Asignacion(expr.nombre, valor)
            else:
                raise SyntaxError("El objetivo de la asignación debe ser una variable")
        
        return expr
    
    def _logic_or(self):
        """Parsear operadores lógicos OR (||)"""
        expr = self._logic_and()
        
        while self._coincide('OPERADOR_LOGICO_OR'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._logic_and()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _logic_and(self):
        """Parsear operadores lógicos AND (&&)"""
        expr = self._equality()
        
        while self._coincide('OPERADOR_LOGICO_AND'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._equality()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _equality(self):
        """Parsear operadores de igualdad (==, !=)"""
        expr = self._comparison()
        
        while self._coincide('OPERADOR_IGUALDAD', 'OPERADOR_DESIGUALDAD'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._comparison()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _comparison(self):
        """Parsear operadores de comparación (>, >=, <, <=)"""
        expr = self._term()
        
        while self._coincide('OPERADOR_MAYOR', 'OPERADOR_MAYOR_IGUAL', 
                            'OPERADOR_MENOR', 'OPERADOR_MENOR_IGUAL'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._term()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _term(self):
        """Parsear términos (+ y -)"""
        expr = self._factor()
        
        while self._coincide('OPERADOR_SUMA', 'OPERADOR_RESTA'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._factor()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _factor(self):
        """Parsear factores (* y /)"""
        expr = self._unary()
        
        while self._coincide('OPERADOR_MULTIPLICACION', 'OPERADOR_DIVISION'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._unary()
            expr = Binaria(expr, operador, derecha)
        
        return expr
    
    def _unary(self):
        """Parsear operadores unarios (!, -)"""
        if self._coincide('OPERADOR_NEGACION', 'OPERADOR_RESTA'):
            operador = self.token_actual['valor']
            self._avanzar()
            derecha = self._unary()
            return Unaria(operador, derecha)
        
        return self._primary()
    
    def _primary(self):
        """Parsear elementos primarios (literales, variables, agrupaciones)"""
        if self._coincide('FALSE'):
            self._avanzar()
            return Literal(False)
        elif self._coincide('TRUE'):
            self._avanzar()
            return Literal(True)
        elif self._coincide('NUMERO'):
            valor = float(self.token_actual['valor'])
            self._avanzar()
            return Literal(valor)
        elif self._coincide('CADENA'):
            valor = self.token_actual['valor']
            self._avanzar()
            return Literal(valor)
        elif self._coincide('IDENTIFICADOR'):
            nombre = self.token_actual['valor']
            self._avanzar()
            return Variable(nombre)
        elif self._coincide('PARENTESIS_IZQ'):
            self._avanzar()
            expr = self._expresion()
            self._consumir('PARENTESIS_DER', "Se esperaba ')' después de la expresión")
            return expr
        
        raise SyntaxError(f"Se esperaba una expresión pero se encontró {self.token_actual}")

# ======================
# 5. EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    # Ejemplo de tokens generados por un lexer (simulados)
    tokens_ejemplo = [
        {'tipo': 'WHILE', 'valor': 'while', 'linea': 1, 'columna': 1},
        {'tipo': 'PARENTESIS_IZQ', 'valor': '(', 'linea': 1, 'columna': 7},
        {'tipo': 'IDENTIFICADOR', 'valor': 'x', 'linea': 1, 'columna': 8},
        {'tipo': 'OPERADOR_MAYOR', 'valor': '>', 'linea': 1, 'columna': 10},
        {'tipo': 'NUMERO', 'valor': '0', 'linea': 1, 'columna': 12},
        {'tipo': 'PARENTESIS_DER', 'valor': ')', 'linea': 1, 'columna': 13},
        {'tipo': 'LLAVE_IZQ', 'valor': '{', 'linea': 1, 'columna': 15},
        {'tipo': 'IDENTIFICADOR', 'valor': 'x', 'linea': 2, 'columna': 5},
        {'tipo': 'OPERADOR_ASIGNACION', 'valor': '=', 'linea': 2, 'columna': 7},
        {'tipo': 'IDENTIFICADOR', 'valor': 'x', 'linea': 2, 'columna': 9},
        {'tipo': 'OPERADOR_RESTA', 'valor': '-', 'linea': 2, 'columna': 11},
        {'tipo': 'NUMERO', 'valor': '1', 'linea': 2, 'columna': 13},
        {'tipo': 'PUNTO_Y_COMA', 'valor': ';', 'linea': 2, 'columna': 14},
        {'tipo': 'LLAVE_DER', 'valor': '}', 'linea': 3, 'columna': 1},
        {'tipo': 'EOF', 'valor': '', 'linea': 3, 'columna': 2}
    ]
    
    print("=== ANALIZADOR SINTÁCTICO ===")
    print("\n🔹 Tokens de entrada:")
    for token in tokens_ejemplo:
        print(f"{token['tipo']: <20} {token['valor']}")
    
    try:
        parser = Parser(tokens_ejemplo)
        ast = parser.parsear()
        
        print("\n🔹 Árbol de Sintaxis Abstracta (AST) generado:")
        print(ast)
        
    except SyntaxError as e:
        print(f"\n❌ Error de sintaxis: {e}")