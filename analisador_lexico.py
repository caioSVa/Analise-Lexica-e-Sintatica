class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha

    def __repr__(self):
        return f"Token(tipo='{self.tipo}', lexema='{self.lexema}', linha={self.linha})"

class Lexer:
    def __init__(self): #definicao dos tokens
        self.lista_tokens = [
            ('FUNCTION', 'fn'),
            ('MAIN', 'main'),
            ('LET', 'let'),
            ('INT', 'int'),
            ('FLOAT', 'float'),
            ('CHAR', 'char'),
            ('IF', 'if'),
            ('ELSE', 'else'),
            ('WHILE', 'while'),
            ('PRINTLN', 'println'),
            ('RETURN', 'return'),
            ('LBRACKET', '('),
            ('RBRACKET', ')'),
            ('LBRACE', '{'),
            ('RBRACE', '}'),
            ('ARROW', '->'),
            ('COLON', ':'),
            ('SEMICOLON', ';'),
            ('COMMA', ','),
            ('ASSIGN', '='),
            ('EQ', '=='),
            ('NE', '!='),
            ('GT', '>'),
            ('GE', '>='),
            ('LT', '<'),
            ('LE', '<='),
            ('PLUS', '+'),
            ('MINUS', '-'),
            ('MULT', '*'),
            ('DIV', '/'),
        ]

    def faz_tokens(self, code):
        tokens = []
        linha_atual = 1
        i = 0

        while i < len(code):
            char = code[i]

            if char.isspace():  #ignora espaços e novas linhas
                if char == '\n':
                    linha_atual += 1
                i += 1
                continue

            combinado = False #procura tokens 
            for tipo, lexema in self.lista_tokens:
                if code[i:i + len(lexema)] == lexema:
                    tokens.append(Token(tipo, lexema, linha_atual))
                    i += len(lexema)
                    combinado = True
                    break
            if combinado:
                continue

            
            if char.isdigit(): #detecta numeros inteiros e reais
                lexema = char
                i += 1
                is_float = False
                while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                    if code[i] == '.':
                        if is_float:
                            raise SyntaxError(f"Erro léxico na linha {linha_atual}: número inválido.")
                        is_float = True
                    lexema += code[i]
                    i += 1
                tipo = 'FLOAT_CONST' if is_float else 'INT_CONST'
                tokens.append(Token(tipo, lexema, linha_atual))
                continue

            if char.isalpha() or char == '_':  #detecta identificadores
                lexema = char
                i += 1
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                    lexema += code[i]
                    i += 1
                tokens.append(Token('ID', lexema, linha_atual))
                continue

            if char == "'": #detecta literais de caracteres
                i += 1
                if i < len(code) and code[i] != "'":
                    lexema = char + code[i] + "'"
                    i += 2
                    tokens.append(Token('CHAR_LITERAL', lexema, linha_atual))
                    continue
                else:
                    raise SyntaxError(f"Erro léxico na linha {linha_atual}: literal de caractere inválido.")

            
            if char == '"': #detecta strings formatadas (começam e terminam com aspas duplas)
                lexema = char
                i += 1
                while i < len(code) and code[i] != '"':
                    lexema += code[i]
                    i += 1
                if i < len(code) and code[i] == '"':
                    lexema += code[i]
                    i += 1
                    tokens.append(Token('FMT_STRING', lexema, linha_atual))
                else:
                    raise SyntaxError(f"Erro léxico na linha {linha_atual}: string inválida.")
                continue

            #caso nao reconheca o caracter
            raise SyntaxError(f"Erro léxico na linha {linha_atual}: caractere inesperado '{char}'.")

        return tokens
