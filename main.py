from analisador_lexico import Lexer

def main():
    arquivo_entrada = "calculadora.p" #define o nome do arquivo de entrada
    try:
        with open(arquivo_entrada, "r") as file: #abre e le o arquivo de entrada
            code = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo_entrada} não encontrado.")
        return
    analisador_lexico = Lexer() #cria uma instancia do analisador léxico

    try:
        tokens = analisador_lexico.faz_tokens(code) #realiza a analise lexica
        with open("tokens.txt", "w") as output_file: #salva os tokens reconhecidos em um arquivo de saida
            for token in tokens:
                output_file.write(f"{token}\n")
        print("Análise léxica concluída com sucesso. Tokens salvos em 'tokens.txt'.")
    except SyntaxError as e:
        with open("erros.txt", "w") as error_file: #caso haja erro salva no arquivo de erros
            error_file.write(f"{str(e)}\n")
        print("Erro encontrado durante a análise léxica. Detalhes salvos em 'erros.txt'.")

if __name__ == "__main__":
    main()
