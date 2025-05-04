"""
====================================================
ANALIZADOR LÉXICO (LEXER) AVANZADO
====================================================
Objetivo: Convertir código fuente en una secuencia de tokens clasificados,
detectando errores léxicos y construyendo una tabla de símbolos.
"""

# ======================
# 1. DEFINICIONES DE TOKENS
# ======================
# Diccionario que mapea tipos de token a sus categorías
TOKENS = {
    # Palabras reservadas
    'IF': 'PALABRA_RESERVADA',
    'ELSE': 'PALABRA_RESERVADA',
    'WHILE': 'PALABRA_RESERVADA',
    'FUNCTION': 'PALABRA_RESERVADA',
    
    # Operadores
    '+': 'OPERADOR_ARITMETICO',
    '-': 'OPERADOR_ARITMETICO',
    '*': 'OPERADOR_ARITMETICO',
    '/': 'OPERADOR_ARITMETICO',
    '=': 'OPERADOR_ASIGNACION',
    '==': 'OPERADOR_COMPARACION',
    '<': 'OPERADOR_COMPARACION',
    '>': 'OPERADOR_COMPARACION',
    
    # Símbolos
    '(': 'PARENTESIS_IZQ',
    ')': 'PARENTESIS_DER',
    '{': 'LLAVE_IZQ',
    '}': 'LLAVE_DER',
    ';': 'PUNTO_Y_COMA',
    ',': 'COMA'
}

# ======================
# 2. CLASE ERROR LÉXICO
# ======================
class ErrorLexico(Exception):
    """Excepción personalizada para errores léxicos"""
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"Error léxico en línea {linea}, columna {columna}: {mensaje}")

# ======================
# 3. CLASE ANALIZADOR LÉXICO
# ======================
class Lexer:
    def __init__(self, codigo):
        """
        Inicializa el lexer con el código fuente a analizar.
        
        Args:
            codigo (str): Código fuente a analizar
        """
        self.codigo = codigo          # Código fuente completo
        self.posicion = 0             # Posición actual en el código
        self.linea_actual = 1          # Línea actual (para mensajes de error)
        self.columna_actual = 1        # Columna actual (para mensajes de error)
        self.tabla_simbolos = []       # Almacena los tokens encontrados
        self.caracter_actual = self._avanzar()  # Primer caracter

    def _avanzar(self):
        """
        Avanza al siguiente caracter en el código fuente y actualiza posición.
        
        Returns:
            str: Siguiente caracter o None si llegamos al final
        """
        if self.posicion >= len(self.codigo):
            return None
        
        caracter = self.codigo[self.posicion]
        self.posicion += 1
        
        # Actualizar contadores de línea y columna
        if caracter == '\n':
            self.linea_actual += 1
            self.columna_actual = 1
        else:
            self.columna_actual += 1
            
        return caracter

    def _saltar_espacios(self):
        """Salta espacios en blanco, tabs y saltos de línea"""
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.caracter_actual = self._avanzar()

    def _obtener_numero(self):
        """
        Extrae un número entero o decimal del código fuente.
        
        Returns:
            str: Número completo como string
        """
        numero = ''
        punto_encontrado = False
        
        while (self.caracter_actual is not None and 
               (self.caracter_actual.isdigit() or self.caracter_actual == '.')):
            
            if self.caracter_actual == '.':
                if punto_encontrado:
                    raise ErrorLexico("Número con múltiples puntos decimales", 
                                     self.linea_actual, self.columna_actual)
                punto_encontrado = True
                
            numero += self.caracter_actual
            self.caracter_actual = self._avanzar()
            
        return numero

    def _obtener_identificador(self):
        """
        Extrae un identificador o palabra reservada del código fuente.
        
        Returns:
            str: Identificador completo
        """
        identificador = ''
        
        while (self.caracter_actual is not None and 
               (self.caracter_actual.isalnum() or self.caracter_actual == '_')):
            identificador += self.caracter_actual
            self.caracter_actual = self._avanzar()
            
        return identificador

    def _obtener_cadena(self):
        """
        Extrae una cadena entre comillas del código fuente.
        
        Returns:
            str: Contenido de la cadena (sin comillas)
        """
        cadena = ''
        comilla = self.caracter_actual  # Guardamos el tipo de comilla (' o ")
        self.caracter_actual = self._avanzar()  # Saltamos la comilla inicial
        
        while self.caracter_actual is not None and self.caracter_actual != comilla:
            cadena += self.caracter_actual
            self.caracter_actual = self._avanzar()
            
        if self.caracter_actual != comilla:
            raise ErrorLexico("Cadena no cerrada", self.linea_actual, self.columna_actual)
            
        self.caracter_actual = self._avanzar()  # Saltamos la comilla final
        return cadena

    def obtener_siguiente_token(self):
        """
        Obtiene el siguiente token del código fuente.
        
        Returns:
            dict: Token con tipo, valor y posición, o None si no hay más tokens
        """
        self._saltar_espacios()
        
        if self.caracter_actual is None:
            return None
            
        # Guardamos posición inicial del token
        inicio_linea = self.linea_actual
        inicio_columna = self.columna_actual
        
        # Identificadores y palabras reservadas
        if self.caracter_actual.isalpha() or self.caracter_actual == '_':
            valor = self._obtener_identificador()
            tipo = TOKENS.get(valor.upper(), 'IDENTIFICADOR')
            return {
                'tipo': tipo,
                'valor': valor,
                'linea': inicio_linea,
                'columna': inicio_columna
            }
            
        # Números
        elif self.caracter_actual.isdigit():
            valor = self._obtener_numero()
            return {
                'tipo': 'NUMERO',
                'valor': valor,
                'linea': inicio_linea,
                'columna': inicio_columna
            }
            
        # Cadenas
        elif self.caracter_actual in ('"', "'"):
            valor = self._obtener_cadena()
            return {
                'tipo': 'CADENA',
                'valor': valor,
                'linea': inicio_linea,
                'columna': inicio_columna
            }
            
        # Operadores y símbolos (incluyendo operadores de 2 caracteres como ==)
        elif self.caracter_actual in {'=', '!', '<', '>'}:
            primer_caracter = self.caracter_actual
            self.caracter_actual = self._avanzar()
            
            if self.caracter_actual == '=':  # Operadores como ==, !=, etc.
                operador = primer_caracter + self.caracter_actual
                self.caracter_actual = self._avanzar()
                if operador in TOKENS:
                    return {
                        'tipo': TOKENS[operador],
                        'valor': operador,
                        'linea': inicio_linea,
                        'columna': inicio_columna
                    }
                    
            # Si no era un operador de 2 caracteres, verificamos el de 1
            if primer_caracter in TOKENS:
                return {
                    'tipo': TOKENS[primer_caracter],
                    'valor': primer_caracter,
                    'linea': inicio_linea,
                    'columna': inicio_columna
                }
                
        # Símbolos de un caracter
        elif self.caracter_actual in TOKENS:
            simbolo = self.caracter_actual
            self.caracter_actual = self._avanzar()
            return {
                'tipo': TOKENS[simbolo],
                'valor': simbolo,
                'linea': inicio_linea,
                'columna': inicio_columna
            }
            
        # Caracter no reconocido
        raise ErrorLexico(f"Caracter no válido: '{self.caracter_actual}'", 
                        self.linea_actual, self.columna_actual)

    def analizar(self):
        """
        Analiza todo el código fuente y devuelve la lista de tokens.
        
        Returns:
            list: Lista de tokens encontrados
        """
        tokens = []
        
        while True:
            token = self.obtener_siguiente_token()
            if token is None:
                break
            tokens.append(token)
            self.tabla_simbolos.append(token)  # Añadimos a tabla de símbolos
            
        return tokens

# ======================
# 4. EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    # Código de ejemplo para analizar
    codigo_ejemplo = """
    function suma(a, b) {
        if (a > 0) {
            return a + b;
        } else {
            return "error";
        }
    }
    """
    
    print("=== ANALIZADOR LÉXICO ===")
    print(f"\n🔹 Código fuente:\n{codigo_ejemplo}")
    
    try:
        lexer = Lexer(codigo_ejemplo)
        tokens = lexer.analizar()
        
        print("\n🔹 Tokens encontrados:")
        for token in tokens:
            print(f"Línea {token['linea']}: [{token['tipo']}] {token['valor']}")
            
        print("\n🔹 Tabla de símbolos generada:")
        for simbolo in lexer.tabla_simbolos:
            print(f"{simbolo['tipo']: <20} {simbolo['valor']}")
            
    except ErrorLexico as e:
        print(f"\n❌ Error: {e}")