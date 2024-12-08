class AnalisadorSintatico:
    """
    Classe responsável pela análise sintática usando o método de descida recursiva.
    """

    def __init__(self, tokens):
        """
        Inicializa o analisador sintático com a lista de tokens gerada pelo analisador léxico.
        
        :param tokens: Lista de objetos Token reconhecidos.
        """
        self.tokens = tokens
        self.posicao = 0
        self.erros = []

    def obter_token_atual(self):
        """
        Retorna o token atual no fluxo, ou None se não houver mais tokens.
        """
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def consumir_token(self):
        """
        Avança o ponteiro para o próximo token no fluxo.
        """
        self.posicao += 1

    def erro(self, esperado):
        """
        Adiciona um erro à lista de erros encontrados.

        :param esperado: Token ou tipo de token esperado.
        """
        token_atual = self.obter_token_atual()
        if token_atual:
            self.erros.append(
                f"Erro: esperado '{esperado}', mas encontrado '{token_atual.lexema}' na linha {token_atual.linha}."
            )
        else:
            self.erros.append(f"Erro: esperado '{esperado}', mas fim do arquivo alcançado.")

    def combinar(self, tipo):
        """
        Verifica se o token atual é do tipo esperado e consome o token se for o caso.

        :param tipo: Tipo do token esperado.
        :return: True se o token for consumido, False caso contrário.
        """
        token_atual = self.obter_token_atual()
        if token_atual and token_atual.tipo == tipo:
            self.consumir_token()
            return True
        return False

    # Regras da Gramática

    def programa(self):
        """
        Regra inicial da gramática: programa -> função programa | ε.
        Processa um programa composto por zero ou mais funções.
        """
        while self.obter_token_atual() is not None:
            if not self.funcao():
                break

    def funcao(self):
        """
        Regra para definir uma função: função -> 'function' IDENTIFICADOR '(' parâmetros ')' '{' corpo '}'.
        """
        if not self.combinar("PALAVRA_CHAVE") or self.obter_token_atual().lexema != "function":
            return False
        self.consumir_token()
        if not self.combinar("IDENTIFICADOR"):
            self.erro("IDENTIFICADOR")
            return False
        if not self.combinar("DELIMITADOR") or self.obter_token_atual().lexema != "(":
            self.erro("'('")
            return False
        self.consumir_token()
        self.parametros()
        if not self.combinar("DELIMITADOR") or self.obter_token_atual().lexema != ")":
            self.erro("')'")
            return False
        self.consumir_token()
        if not self.combinar("DELIMITADOR") or self.obter_token_atual().lexema != "{":
            self.erro("'{'")
            return False
        self.consumir_token()
        self.corpo()
        if not self.combinar("DELIMITADOR") or self.obter_token_atual().lexema != "}":
            self.erro("'}'")
            return False
        self.consumir_token()
        return True

    def parametros(self):
        """
        Regra para os parâmetros de uma função: parâmetros -> IDENTIFICADOR (',' IDENTIFICADOR)* | ε.
        """
        if self.combinar("IDENTIFICADOR"):
            while self.combinar("DELIMITADOR") and self.obter_token_atual().lexema == ",":
                self.consumir_token()
                if not self.combinar("IDENTIFICADOR"):
                    self.erro("IDENTIFICADOR")
                    break

    def corpo(self):
        """
        Regra para o corpo de uma função: corpo -> instrução corpo | ε.
        """
        while self.instrucao():
            pass

    def instrucao(self):
        """
        Regra para uma instrução: instrução -> 'return' expressão ';'.
        """
        if not self.combinar("PALAVRA_CHAVE") or self.obter_token_atual().lexema != "return":
            return False
        self.consumir_token()
        if not self.expressao():
            self.erro("expressão válida")
            return False
        if not self.combinar("DELIMITADOR") or self.obter_token_atual().lexema != ";":
            self.erro("';'")
            return False
        self.consumir_token()
        return True

    def expressao(self):
        """
        Regra para uma expressão: expressão -> IDENTIFICADOR ('+' IDENTIFICADOR)?.
        """
        if not self.combinar("IDENTIFICADOR"):
            return False
        if self.combinar("OPERADOR") and self.obter_token_atual().lexema == "+":
            self.consumir_token()
            if not self.combinar("IDENTIFICADOR"):
                self.erro("IDENTIFICADOR")
                return False
        return True
