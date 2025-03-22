# Interpretador para a Linguagem Tupã
# Baseado em português brasileiro para facilitar o aprendizado de programação

import re
import sys
import math
from typing import Dict, List, Any, Callable, Optional, Union

class ErroTupa(Exception):
    """Classe para representar erros na linguagem Tupã"""
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

class Token:
    """Representa um token na linguagem Tupã"""
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, linha={self.linha}, coluna={self.coluna})"

class Lexer:
    """Analisador léxico para a linguagem Tupã"""
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []
        
        # Definição de palavras-chave
        self.palavras_chave = {
            'criar': 'CRIAR',
            'mostrar': 'MOSTRAR',
            'pegar': 'PEGAR',
            'se': 'SE',
            'então': 'ENTAO',
            'senão': 'SENAO',
            'fim': 'FIM',
            'enquanto': 'ENQUANTO',
            'fazer': 'FAZER',
            'para': 'PARA',
            'de': 'DE',
            'até': 'ATE',
            'em': 'EM',
            'função': 'FUNCAO',
            'devolver': 'DEVOLVER',
            'classe': 'CLASSE',
            'tentar': 'TENTAR',
            'pegar': 'PEGAR_ERRO',
            'erro': 'ERRO',
            'usar': 'USAR',
            'lista': 'LISTA',
            'dicionário': 'DICIONARIO',
            'verdadeiro': 'BOOLEANO',
            'falso': 'BOOLEANO',
            'e': 'E',
            'ou': 'OU',
            'não': 'NAO'
        }

    def avancar(self):
        """Avança para o próximo caractere"""
        self.posicao += 1
        self.coluna += 1
        if self.posicao < len(self.codigo) and self.codigo[self.posicao - 1] == '\n':
            self.linha += 1
            self.coluna = 1

    def caractere_atual(self):
        """Retorna o caractere atual"""
        if self.posicao >= len(self.codigo):
            return None
        return self.codigo[self.posicao]

    def pular_espacos(self):
        """Pula espaços em branco"""
        while self.caractere_atual() is not None and self.caractere_atual().isspace():
            self.avancar()

    def pular_comentarios(self):
        """Pula comentários (// até o final da linha)"""
        if self.caractere_atual() == '/' and self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '/':
            while self.caractere_atual() is not None and self.caractere_atual() != '\n':
                self.avancar()

    def identificar_numero(self):
        """Identifica um número (inteiro ou decimal)"""
        inicio_coluna = self.coluna
        inicio = self.posicao
        
        # Verifica se é um número negativo
        if self.caractere_atual() == '-':
            self.avancar()
        
        # Processa os dígitos antes do ponto decimal
        while self.caractere_atual() is not None and self.caractere_atual().isdigit():
            self.avancar()
        
        # Verifica se há um ponto decimal
        if self.caractere_atual() == '.':
            self.avancar()
            
            # Processa os dígitos após o ponto decimal
            while self.caractere_atual() is not None and self.caractere_atual().isdigit():
                self.avancar()
        
        valor = self.codigo[inicio:self.posicao]
        try:
            if '.' in valor:
                return Token('NUMERO', float(valor), self.linha, inicio_coluna)
            else:
                return Token('NUMERO', int(valor), self.linha, inicio_coluna)
        except ValueError:
            raise ErroTupa(f"Número inválido: {valor} na linha {self.linha}, coluna {inicio_coluna}")

    def identificar_string(self):
        """Identifica uma string (entre aspas)"""
        inicio_coluna = self.coluna
        delimitador = self.caractere_atual()  # " ou '
        self.avancar()  # Pula a aspas inicial
        inicio = self.posicao
        
        while self.caractere_atual() is not None and self.caractere_atual() != delimitador:
            self.avancar()
        
        if self.caractere_atual() is None:
            raise ErroTupa(f"String não fechada na linha {self.linha}, coluna {inicio_coluna}")
        
        valor = self.codigo[inicio:self.posicao]
        self.avancar()  # Pula a aspas final
        return Token('STRING', valor, self.linha, inicio_coluna)

    def identificar_identificador(self):
        """Identifica um identificador ou palavra-chave"""
        inicio_coluna = self.coluna
        inicio = self.posicao
        
        while (self.caractere_atual() is not None and 
               (self.caractere_atual().isalnum() or self.caractere_atual() == '_' or 
                self.caractere_atual() in 'áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ')):
            self.avancar()
        
        valor = self.codigo[inicio:self.posicao]
        tipo = self.palavras_chave.get(valor, 'IDENTIFICADOR')
        
        if tipo == 'BOOLEANO':
            valor = True if valor == 'verdadeiro' else False
            
        return Token(tipo, valor, self.linha, inicio_coluna)

    def tokenizar(self):
        """Converte o código em uma lista de tokens"""
        while self.posicao < len(self.codigo):
            # Pula espaços em branco e comentários
            self.pular_espacos()
            self.pular_comentarios()
            
            if self.posicao >= len(self.codigo):
                break
            
            caractere = self.caractere_atual()
            
            if caractere is None:
                break
            elif caractere.isdigit() or (caractere == '-' and self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1].isdigit()):
                self.tokens.append(self.identificar_numero())
            elif caractere == '"' or caractere == "'":
                self.tokens.append(self.identificar_string())
            elif caractere.isalpha() or caractere == '_':
                self.tokens.append(self.identificar_identificador())
            elif caractere == '+':
                self.tokens.append(Token('MAIS', '+', self.linha, self.coluna))
                self.avancar()
            elif caractere == '-':
                self.tokens.append(Token('MENOS', '-', self.linha, self.coluna))
                self.avancar()
            elif caractere == '*':
                self.tokens.append(Token('MULTIPLICACAO', '*', self.linha, self.coluna))
                self.avancar()
            elif caractere == '/':
                self.tokens.append(Token('DIVISAO', '/', self.linha, self.coluna))
                self.avancar()
            elif caractere == '=':
                if self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '=':
                    self.tokens.append(Token('IGUAL', '==', self.linha, self.coluna))
                    self.avancar()
                    self.avancar()
                else:
                    self.tokens.append(Token('ATRIBUICAO', '=', self.linha, self.coluna))
                    self.avancar()
            elif caractere == '!':
                if self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '=':
                    self.tokens.append(Token('DIFERENTE', '!=', self.linha, self.coluna))
                    self.avancar()
                    self.avancar()
                else:
                    raise ErroTupa(f"Caractere inesperado: ! na linha {self.linha}, coluna {self.coluna}")
            elif caractere == '>':
                if self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '=':
                    self.tokens.append(Token('MAIOR_IGUAL', '>=', self.linha, self.coluna))
                    self.avancar()
                    self.avancar()
                else:
                    self.tokens.append(Token('MAIOR', '>', self.linha, self.coluna))
                    self.avancar()
            elif caractere == '<':
                if self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '=':
                    self.tokens.append(Token('MENOR_IGUAL', '<=', self.linha, self.coluna))
                    self.avancar()
                    self.avancar()
                else:
                    self.tokens.append(Token('MENOR', '<', self.linha, self.coluna))
                    self.avancar()
            elif caractere == '(':
                self.tokens.append(Token('PARENTESE_ESQUERDO', '(', self.linha, self.coluna))
                self.avancar()
            elif caractere == ')':
                self.tokens.append(Token('PARENTESE_DIREITO', ')', self.linha, self.coluna))
                self.avancar()
            elif caractere == '[':
                self.tokens.append(Token('COLCHETE_ESQUERDO', '[', self.linha, self.coluna))
                self.avancar()
            elif caractere == ']':
                self.tokens.append(Token('COLCHETE_DIREITO', ']', self.linha, self.coluna))
                self.avancar()
            elif caractere == '{':
                self.tokens.append(Token('CHAVE_ESQUERDA', '{', self.linha, self.coluna))
                self.avancar()
            elif caractere == '}':
                self.tokens.append(Token('CHAVE_DIREITA', '}', self.linha, self.coluna))
                self.avancar()
            elif caractere == ',':
                self.tokens.append(Token('VIRGULA', ',', self.linha, self.coluna))
                self.avancar()
            elif caractere == '.':
                self.tokens.append(Token('PONTO', '.', self.linha, self.coluna))
                self.avancar()
            elif caractere == ':':
                self.tokens.append(Token('DOIS_PONTOS', ':', self.linha, self.coluna))
                self.avancar()
            else:
                raise ErroTupa(f"Caractere inesperado: {caractere} na linha {self.linha}, coluna {self.coluna}")
        
        self.tokens.append(Token('EOF', None, self.linha, self.coluna))
        return self.tokens

class Parser:
    """Analisador sintático para a linguagem Tupã"""
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.token_atual = self.tokens[0]

    def avancar(self):
        """Avança para o próximo token"""
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
        return self.token_atual

    def consumir(self, tipo):
        """Consome um token se ele for do tipo esperado"""
        if self.token_atual.tipo == tipo:
            token = self.token_atual
            self.avancar()
            return token
        
        raise ErroTupa(f"Erro de sintaxe: esperado {tipo}, obtido {self.token_atual.tipo} na linha {self.token_atual.linha}, coluna {self.token_atual.coluna}")

    def analisar(self):
        """Analisa o programa"""
        return self.programa()

    def programa(self):
        """Programa = Lista de declarações"""
        instrucoes = []
        
        while self.token_atual.tipo != 'EOF':
            instrucoes.append(self.declaracao())
        
        return {
            'tipo': 'Programa',
            'instrucoes': instrucoes
        }

    def declaracao(self):
        """Analisa uma declaração"""
        if self.token_atual.tipo == 'CRIAR':
            return self.declaracao_variavel()
        elif self.token_atual.tipo == 'MOSTRAR':
            return self.declaracao_mostrar()
        elif self.token_atual.tipo == 'PEGAR':
            return self.declaracao_pegar()
        elif self.token_atual.tipo == 'SE':
            return self.declaracao_se()
        elif self.token_atual.tipo == 'ENQUANTO':
            return self.declaracao_enquanto()
        elif self.token_atual.tipo == 'PARA':
            return self.declaracao_para()
        elif self.token_atual.tipo == 'FUNCAO':
            return self.declaracao_funcao()
        elif self.token_atual.tipo == 'DEVOLVER':
            return self.declaracao_devolver()
        elif self.token_atual.tipo == 'CLASSE':
            return self.declaracao_classe()
        elif self.token_atual.tipo == 'TENTAR':
            return self.declaracao_tentar()
        elif self.token_atual.tipo == 'USAR':
            return self.declaracao_usar()
        else:
            return self.expressao_declaracao()

    def declaracao_variavel(self):
        """Analisa uma declaração de variável"""
        self.consumir('CRIAR')
        
        # Verificar se é uma lista ou dicionário
        tipo = None
        if self.token_atual.tipo == 'LISTA':
            tipo = 'lista'
            self.avancar()
        elif self.token_atual.tipo == 'DICIONARIO':
            tipo = 'dicionario'
            self.avancar()
        
        nome = self.consumir('IDENTIFICADOR').valor
        self.consumir('ATRIBUICAO')
        valor = self.expressao()
        
        return {
            'tipo': 'DeclaracaoVariavel',
            'nome': nome,
            'valor': valor,
            'tipo_dado': tipo
        }

    def declaracao_mostrar(self):
        """Analisa uma declaração de saída"""
        self.consumir('MOSTRAR')
        expressao = self.expressao()
        
        return {
            'tipo': 'DeclaracaoMostrar',
            'expressao': expressao
        }

    def declaracao_pegar(self):
        """Analisa uma declaração de entrada"""
        self.consumir('PEGAR')
        nome = self.consumir('IDENTIFICADOR').valor
        
        return {
            'tipo': 'DeclaracaoPegar',
            'nome': nome
        }

    def declaracao_se(self):
        """Analisa uma estrutura condicional"""
        self.consumir('SE')
        condicao = self.expressao()
        
        self.consumir('ENTAO')
        bloco_entao = []
        
        while (self.token_atual.tipo != 'FIM' and 
               self.token_atual.tipo != 'SENAO' and 
               self.token_atual.tipo != 'EOF'):
            bloco_entao.append(self.declaracao())
        
        bloco_senao = []
        if self.token_atual.tipo == 'SENAO':
            self.avancar()
            
            while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
                bloco_senao.append(self.declaracao())
        
        self.consumir('FIM')
        
        return {
            'tipo': 'DeclaracaoSe',
            'condicao': condicao,
            'bloco_entao': bloco_entao,
            'bloco_senao': bloco_senao
        }

    def declaracao_enquanto(self):
        """Analisa um laço enquanto"""
        self.consumir('ENQUANTO')
        condicao = self.expressao()
        
        self.consumir('FAZER')
        corpo = []
        
        while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
            corpo.append(self.declaracao())
        
        self.consumir('FIM')
        
        return {
            'tipo': 'DeclaracaoEnquanto',
            'condicao': condicao,
            'corpo': corpo
        }

    def declaracao_para(self):
        """Analisa um laço para"""
        self.consumir('PARA')
        variavel = self.consumir('IDENTIFICADOR').valor
        
        # Verifica se é um loop for-in (para cada) ou for-range (para de-até)
        if self.token_atual.tipo == 'EM':
            # Loop for-in (para cada)
            self.avancar()
            colecao = self.expressao()
            
            self.consumir('FAZER')
            corpo = []
            
            while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
                corpo.append(self.declaracao())
            
            self.consumir('FIM')
            
            return {
                'tipo': 'DeclaracaoParaCada',
                'variavel': variavel,
                'colecao': colecao,
                'corpo': corpo
            }
        else:
            # Loop for-range (para de-até)
            self.consumir('DE')
            inicio = self.expressao()
            
            self.consumir('ATE')
            fim = self.expressao()
            
            self.consumir('FAZER')
            corpo = []
            
            while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
                corpo.append(self.declaracao())
            
            self.consumir('FIM')
            
            return {
                'tipo': 'DeclaracaoPara',
                'variavel': variavel,
                'inicio': inicio,
                'fim': fim,
                'corpo': corpo
            }

    def declaracao_funcao(self):
        """Analisa uma declaração de função"""
        self.consumir('FUNCAO')
        nome = self.consumir('IDENTIFICADOR').valor
        
        self.consumir('PARENTESE_ESQUERDO')
        parametros = []
        
        if self.token_atual.tipo != 'PARENTESE_DIREITO':
            parametros.append(self.consumir('IDENTIFICADOR').valor)
            
            while self.token_atual.tipo == 'VIRGULA':
                self.avancar()
                parametros.append(self.consumir('IDENTIFICADOR').valor)
        
        self.consumir('PARENTESE_DIREITO')
        
        corpo = []
        while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
            corpo.append(self.declaracao())
        
        self.consumir('FIM')
        
        return {
            'tipo': 'DeclaracaoFuncao',
            'nome': nome,
            'parametros': parametros,
            'corpo': corpo
        }

    def declaracao_devolver(self):
        """Analisa uma declaração de retorno"""
        self.consumir('DEVOLVER')
        valor = self.expressao()
        
        return {
            'tipo': 'DeclaracaoDevolver',
            'valor': valor
        }

    def declaracao_classe(self):
        """Analisa uma declaração de classe"""
        self.consumir('CLASSE')
        nome = self.consumir('IDENTIFICADOR').valor
        
        metodos = []
        atributos = []
        
        while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
            if self.token_atual.tipo == 'FUNCAO':
                metodos.append(self.declaracao_funcao())
            elif self.token_atual.tipo == 'CRIAR':
                atributos.append(self.declaracao_variavel())
            else:
                raise ErroTupa(f"Declaração inesperada dentro da classe: {self.token_atual.tipo} na linha {self.token_atual.linha}, coluna {self.token_atual.coluna}")
        
        self.consumir('FIM')
        
        return {
            'tipo': 'DeclaracaoClasse',
            'nome': nome,
            'metodos': metodos,
            'atributos': atributos
        }

    def declaracao_tentar(self):
        """Analisa uma estrutura de tratamento de erros"""
        self.consumir('TENTAR')
        
        bloco_tentar = []
        while (self.token_atual.tipo != 'PEGAR_ERRO' and 
               self.token_atual.tipo != 'FIM' and 
               self.token_atual.tipo != 'EOF'):
            bloco_tentar.append(self.declaracao())
        
        self.consumir('PEGAR_ERRO')
        nome_erro = self.consumir('IDENTIFICADOR').valor
        
        bloco_pegar = []
        while self.token_atual.tipo != 'FIM' and self.token_atual.tipo != 'EOF':
            bloco_pegar.append(self.declaracao())
        
        self.consumir('FIM')
        
        return {
            'tipo': 'DeclaracaoTentar',
            'bloco_tentar': bloco_tentar,
            'nome_erro': nome_erro,
            'bloco_pegar': bloco_pegar
        }

    def declaracao_usar(self):
        """Analisa uma declaração de importação de módulo"""
        self.consumir('USAR')
        nome = self.consumir('IDENTIFICADOR').valor
        
        return {
            'tipo': 'DeclaracaoUsar',
            'nome': nome
        }

    def expressao_declaracao(self):
        """Analisa uma declaração de expressão"""
        expressao = self.expressao()
        
        return {
            'tipo': 'ExpressaoDeclaracao',
            'expressao': expressao
        }

    def expressao(self):
        """Analisa uma expressão"""
        return self.atribuicao()

    def atribuicao(self):
        """Analisa uma atribuição"""
        expr = self.ou()
        
        if self.token_atual.tipo == 'ATRIBUICAO':
            self.avancar()
            valor = self.expressao()
            
            if expr['tipo'] == 'VariavelExpressao':
                return {
                    'tipo': 'AtribuicaoExpressao',
                    'nome': expr['nome'],
                    'valor': valor
                }
            elif expr['tipo'] == 'IndexacaoExpressao':
                return {
                    'tipo': 'AtribuicaoIndexacao',
                    'objeto': expr['objeto'],
                    'indice': expr['indice'],
                    'valor': valor
                }
            elif expr['tipo'] == 'AtributoExpressao':
                return {
                    'tipo': 'AtribuicaoAtributo',
                    'objeto': expr['objeto'],
                    'nome': expr['nome'],
                    'valor': valor
                }
            else:
                raise ErroTupa(f"Alvo inválido para atribuição na linha {self.tokens[self.posicao-1].linha}")
        
        return expr

    def ou(self):
        """Analisa uma expressão OU"""
        expr = self.e()
        
        while self.token_atual.tipo == 'OU':
            operador = self.avancar()
            direita = self.e()
            
            expr = {
                'tipo': 'LogicaExpressao',
                'operador': 'ou',
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def e(self):
        """Analisa uma expressão E"""
        expr = self.igualdade()
        
        while self.token_atual.tipo == 'E':
            operador = self.avancar()
            direita = self.igualdade()
            
            expr = {
                'tipo': 'LogicaExpressao',
                'operador': 'e',
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def igualdade(self):
        """Analisa uma expressão de igualdade"""
        expr = self.comparacao()
        
        while self.token_atual.tipo in ['IGUAL', 'DIFERENTE']:
            operador = self.token_atual.tipo
            self.avancar()
            direita = self.comparacao()
            
            expr = {
                'tipo': 'BinariaExpressao',
                'operador': '==' if operador == 'IGUAL' else '!=',
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def comparacao(self):
        """Analisa uma expressão de comparação"""
        expr = self.adicao()
        
        while self.token_atual.tipo in ['MENOR', 'MENOR_IGUAL', 'MAIOR', 'MAIOR_IGUAL']:
            operador = self.token_atual.tipo
            self.avancar()
            direita = self.adicao()
            
            expr = {
                'tipo': 'BinariaExpressao',
                'operador': {
                    'MENOR': '<',
                    'MENOR_IGUAL': '<=',
                    'MAIOR': '>',
                    'MAIOR_IGUAL': '>='
                }[operador],
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def adicao(self):
        """Analisa uma expressão de adição ou subtração"""
        expr = self.multiplicacao()
        
        while self.token_atual.tipo in ['MAIS', 'MENOS']:
            operador = self.token_atual.tipo
            self.avancar()
            direita = self.multiplicacao()
            
            expr = {
                'tipo': 'BinariaExpressao',
                'operador': '+' if operador == 'MAIS' else '-',
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def multiplicacao(self):
        """Analisa uma expressão de multiplicação ou divisão"""
        expr = self.unario()
        
        while self.token_atual.tipo in ['MULTIPLICACAO', 'DIVISAO']:
            operador = self.token_atual.tipo
            self.avancar()
            direita = self.unario()
            
            expr = {
                'tipo': 'BinariaExpressao',
                'operador': '*' if operador == 'MULTIPLICACAO' else '/',
                'esquerda': expr,
                'direita': direita
            }
        
        return expr

    def unario(self):
        """Analisa uma expressão unária"""
        if self.token_atual.tipo in ['MENOS', 'NAO']:
            operador = self.token_atual.tipo
            self.avancar()
            direita = self.unario()
            
            return {
                'tipo': 'UnariaExpressao',
                'operador': '-' if operador == 'MENOS' else '!',
                'direita': direita
            }
        
        return self.chamada()

    def chamada(self):
        """Analisa uma chamada de função"""
        expr = self.primario()
        
        while True:
            if self.token_atual.tipo == 'PARENTESE_ESQUERDO':
                self.avancar()
                argumentos = []
                
                if self.token_atual.tipo != 'PARENTESE_DIREITO':
                    argumentos.append(self.expressao())
                    
                    while self.token_atual.tipo == 'VIRGULA':
                        self.avancar()
                        argumentos.append(self.expressao())
                
                self.consumir('PARENTESE_DIREITO')
                
                expr = {
                    'tipo': 'ChamadaExpressao',
                    'funcao': expr,
                    'argumentos': argumentos
                }
            elif self.token_atual.tipo == 'COLCHETE_ESQUERDO':
                self.avancar()
                indice = self.expressao()
                self.consumir('COLCHETE_DIREITO')
                
                expr = {
                    'tipo': 'IndexacaoExpressao',
                    'objeto': expr,
                    'indice': indice
                }
            elif self.token_atual.tipo == 'PONTO':
                self.avancar()
                nome = self.consumir('IDENTIFICADOR').valor
                
                expr = {
                    'tipo': 'AtributoExpressao',
                    'objeto': expr,
                    'nome': nome
                }
            else:
                break
        
        return expr

    def primario(self):
        """Analisa uma expressão primária"""
        if self.token_atual.tipo == 'NUMERO':
            valor = self.token_atual.valor
            self.avancar()
            return {'tipo': 'LiteralExpressao', 'valor': valor}
        
        elif self.token_atual.tipo == 'STRING':
            valor = self.token_atual.valor
            self.avancar()
            return {'tipo': 'LiteralExpressao', 'valor': valor}
        
        elif self.token_atual.tipo == 'BOOLEANO':
            valor = self.token_atual.valor
            self.avancar()
            return {'tipo': 'LiteralExpressao', 'valor': valor}
        
        elif self.token_atual.tipo == 'IDENTIFICADOR':
            nome = self.token_atual.valor
            self.avancar()
            return {'tipo': 'VariavelExpressao', 'nome': nome}
        
        elif self.token_atual.tipo == 'PARENTESE_ESQUERDO':
            self.avancar()
            expr = self.expressao()
            self.consumir('PARENTESE_DIREITO')
            return {'tipo': 'AgruparExpressao', 'expressao': expr}
        
        elif self.token_atual.tipo == 'COLCHETE_ESQUERDO':
            self.avancar()
            elementos = []
            
            if self.token_atual.tipo != 'COLCHETE_DIREITO':
                elementos.append(self.expressao())
                
                while self.token_atual.tipo == 'VIRGULA':
                    self.avancar()
                    elementos.append(self.expressao())
            
            self.consumir('COLCHETE_DIREITO')
            return {'tipo': 'ListaExpressao', 'elementos': elementos}
        
        elif self.token_atual.tipo == 'CHAVE_ESQUERDA':
            self.avancar()
            pares = []
            
            if self.token_atual.tipo != 'CHAVE_DIREITA':
                chave = self.expressao()
                self.consumir('DOIS_PONTOS')
                valor = self.expressao()
                pares.append({'chave': chave, 'valor': valor})
                
                while self.token_atual.tipo == 'VIRGULA':
                    self.avancar()
                    chave = self.expressao()
                    self.consumir('DOIS_PONTOS')
                    valor = self.expressao()
                    pares.append({'chave': chave, 'valor': valor})
            
            self.consumir('CHAVE_DIREITA')
            return {'tipo': 'DicionarioExpressao', 'pares': pares}
        
        raise ErroTupa(f"Expressão inesperada: {self.token_atual.tipo} na linha {self.token_atual.linha}, coluna {self.token_atual.coluna}")

class Interpretador:
    """Interpretador para a linguagem Tupã"""
    def __init__(self):
        self.escopo_global = {}
        self.escopo_atual = [self.escopo_global]
        self.retorno_valor = None
        
        # Funções integradas
        self.escopo_global['tamanho'] = lambda x: len(x)
        self.escopo_global['tipo'] = lambda x: type(x).__name__
        self.escopo_global['para_texto'] = lambda x: str(x)
        self.escopo_global['para_numero'] = lambda x: float(x) if '.' in str(x) else int(x)
        self.escopo_global['para_lista'] = lambda x: list(x)
        self.escopo_global['raiz'] = lambda x: math.sqrt(x)
        
        # Módulos integrados básicos
        self.modulos = {
            'matematica': {
                'pi': math.pi,
                'e': math.e,
                'seno': math.sin,
                'cosseno': math.cos,
                'tangente': math.tan,
                'raiz': math.sqrt,
                'potencia': math.pow,
                'absoluto': abs,
                'teto': math.ceil,
                'piso': math.floor,
                'aleatorio': lambda: __import__('random').random(),
                'aleatorio_entre': lambda min, max: __import__('random').randint(min, max)
            }
        }

    def definir(self, nome, valor):
        """Define uma variável no escopo atual"""
        self.escopo_atual[-1][nome] = valor

    def obter(self, nome):
        """Obtém o valor de uma variável"""
        for escopo in reversed(self.escopo_atual):
            if nome in escopo:
                return escopo[nome]
        
        raise ErroTupa(f"Variável não definida: '{nome}'")

    def iniciar_escopo(self):
        """Inicia um novo escopo"""
        self.escopo_atual.append({})

    def encerrar_escopo(self):
        """Encerra o escopo atual"""
        self.escopo_atual.pop()

    def interpretar(self, arvore):
        """Interpreta a árvore sintática"""
        try:
            self.executar(arvore)
        except ErroTupa as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro interno: {e}")

    def executar(self, no):
        """Executa um nó da árvore sintática"""
        tipo = no['tipo']
        
        # Programa
        if tipo == 'Programa':
            for instrucao in no['instrucoes']:
                self.executar(instrucao)
        
        # Declarações
        elif tipo == 'DeclaracaoVariavel':
            valor = self.avaliar(no['valor'])
            self.definir(no['nome'], valor)
        
        elif tipo == 'DeclaracaoMostrar':
            valor = self.avaliar(no['expressao'])
            print(valor)
        
        elif tipo == 'DeclaracaoPegar':
            valor = input()
            try:
                # Tenta converter para número se possível
                if '.' in valor:
                    valor = float(valor)
                else:
                    valor = int(valor)
            except ValueError:
                # Mantém como string se não for um número
                pass
            
            self.definir(no['nome'], valor)
        
        elif tipo == 'DeclaracaoSe':
            if self.avaliar(no['condicao']):
                for instrucao in no['bloco_entao']:
                    self.executar(instrucao)
            else:
                for instrucao in no['bloco_senao']:
                    self.executar(instrucao)
        
        elif tipo == 'DeclaracaoEnquanto':
            while self.avaliar(no['condicao']):
                try:
                    for instrucao in no['corpo']:
                        self.executar(instrucao)
                except BreakException:
                    break
                except ContinueException:
                    continue
        
        elif tipo == 'DeclaracaoPara':
            self.iniciar_escopo()
            inicio = self.avaliar(no['inicio'])
            fim = self.avaliar(no['fim'])
            
            self.definir(no['variavel'], inicio)
            
            try:
                while self.obter(no['variavel']) <= fim:
                    try:
                        for instrucao in no['corpo']:
                            self.executar(instrucao)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                    
                    self.definir(no['variavel'], self.obter(no['variavel']) + 1)
            finally:
                self.encerrar_escopo()
        
        elif tipo == 'DeclaracaoParaCada':
            self.iniciar_escopo()
            colecao = self.avaliar(no['colecao'])
            
            try:
                for item in colecao:
                    self.definir(no['variavel'], item)
                    
                    try:
                        for instrucao in no['corpo']:
                            self.executar(instrucao)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
            finally:
                self.encerrar_escopo()
        
        elif tipo == 'DeclaracaoFuncao':
            def funcao(*args):
                self.iniciar_escopo()
                
                # Define os parâmetros
                for i, param in enumerate(no['parametros']):
                    valor = args[i] if i < len(args) else None
                    self.definir(param, valor)
                
                # Salva o valor de retorno anterior
                retorno_anterior = self.retorno_valor
                self.retorno_valor = None
                
                try:
                    # Executa o corpo da função
                    for instrucao in no['corpo']:
                        self.executar(instrucao)
                        if self.retorno_valor is not None:
                            break
                    
                    # Retorna o valor
                    return self.retorno_valor
                finally:
                    # Restaura o valor de retorno anterior
                    valor_retorno = self.retorno_valor
                    self.retorno_valor = retorno_anterior
                    self.encerrar_escopo()
                    return valor_retorno
            
            self.definir(no['nome'], funcao)
        
        elif tipo == 'DeclaracaoDevolver':
            self.retorno_valor = self.avaliar(no['valor'])
        
        elif tipo == 'DeclaracaoClasse':
            class Classe:
                def __init__(self, interpretador, classe_no):
                    self.interpretador = interpretador
                    self.classe_no = classe_no
                    self.atributos = {}
                    
                    # Inicializa os atributos
                    for atributo in classe_no['atributos']:
                        valor = interpretador.avaliar(atributo['valor'])
                        self.atributos[atributo['nome']] = valor
                    
                    # Inicializa os métodos
                    self.metodos = {}
                    for metodo in classe_no['metodos']:
                        self.metodos[metodo['nome']] = metodo
                
                def __getattr__(self, nome):
                    if nome in self.atributos:
                        return self.atributos[nome]
                    
                    if nome in self.metodos:
                        metodo = self.metodos[nome]
                        
                        def metodo_wrapper(*args):
                            self.interpretador.iniciar_escopo()
                            
                            # Define o 'self' para o método
                            self.interpretador.definir('self', self)
                            
                            # Define os parâmetros
                            for i, param in enumerate(metodo['parametros']):
                                valor = args[i] if i < len(args) else None
                                self.interpretador.definir(param, valor)
                            
                            # Salva o valor de retorno anterior
                            retorno_anterior = self.interpretador.retorno_valor
                            self.interpretador.retorno_valor = None
                            
                            try:
                                # Executa o corpo do método
                                for instrucao in metodo['corpo']:
                                    self.interpretador.executar(instrucao)
                                    if self.interpretador.retorno_valor is not None:
                                        break
                                
                                # Retorna o valor
                                return self.interpretador.retorno_valor
                            finally:
                                # Restaura o valor de retorno anterior
                                valor_retorno = self.interpretador.retorno_valor
                                self.interpretador.retorno_valor = retorno_anterior
                                self.interpretador.encerrar_escopo()
                                return valor_retorno
                        
                        return metodo_wrapper
                    
                    raise ErroTupa(f"Atributo não definido: '{nome}'")
                
                def __setattr__(self, nome, valor):
                    if nome in ['interpretador', 'classe_no', 'atributos', 'metodos']:
                        super().__setattr__(nome, valor)
                    else:
                        self.atributos[nome] = valor
            
            def construtor():
                return Classe(self, no)
            
            self.definir(no['nome'], construtor)
        
        elif tipo == 'DeclaracaoTentar':
            try:
                for instrucao in no['bloco_tentar']:
                    self.executar(instrucao)
            except Exception as e:
                self.iniciar_escopo()
                self.definir(no['nome_erro'], str(e))
                
                try:
                    for instrucao in no['bloco_pegar']:
                        self.executar(instrucao)
                finally:
                    self.encerrar_escopo()
        
        elif tipo == 'DeclaracaoUsar':
            nome = no['nome']
            if nome in self.modulos:
                modulo = self.modulos[nome]
                for nome_funcao, funcao in modulo.items():
                    self.definir(nome_funcao, funcao)
            else:
                raise ErroTupa(f"Módulo não encontrado: '{nome}'")
        
        elif tipo == 'ExpressaoDeclaracao':
            self.avaliar(no['expressao'])
        
        else:
            raise ErroTupa(f"Tipo de nó desconhecido: {tipo}")

    def avaliar(self, no):
        """Avalia uma expressão"""
        tipo = no['tipo']
        
        # Expressões
        if tipo == 'LiteralExpressao':
            return no['valor']
        
        elif tipo == 'VariavelExpressao':
            return self.obter(no['nome'])
        
        elif tipo == 'AgruparExpressao':
            return self.avaliar(no['expressao'])
        
        elif tipo == 'UnariaExpressao':
            direita = self.avaliar(no['direita'])
            
            if no['operador'] == '-':
                return -direita
            elif no['operador'] == '!':
                return not direita
        
        elif tipo == 'BinariaExpressao':
            esquerda = self.avaliar(no['esquerda'])
            direita = self.avaliar(no['direita'])
            
            if no['operador'] == '+':
                return esquerda + direita
            elif no['operador'] == '-':
                return esquerda - direita
            elif no['operador'] == '*':
                return esquerda * direita
            elif no['operador'] == '/':
                return esquerda / direita
            elif no['operador'] == '==':
                return esquerda == direita
            elif no['operador'] == '!=':
                return esquerda != direita
            elif no['operador'] == '<':
                return esquerda < direita
            elif no['operador'] == '<=':
                return esquerda <= direita
            elif no['operador'] == '>':
                return esquerda > direita
            elif no['operador'] == '>=':
                return esquerda >= direita
        
        elif tipo == 'LogicaExpressao':
            esquerda = self.avaliar(no['esquerda'])
            
            if no['operador'] == 'e':
                return esquerda and self.avaliar(no['direita'])
            elif no['operador'] == 'ou':
                return esquerda or self.avaliar(no['direita'])
        
        elif tipo == 'AtribuicaoExpressao':
            valor = self.avaliar(no['valor'])
            self.definir(no['nome'], valor)
            return valor
        
        elif tipo == 'AtribuicaoIndexacao':
            objeto = self.avaliar(no['objeto'])
            indice = self.avaliar(no['indice'])
            valor = self.avaliar(no['valor'])
            
            objeto[indice] = valor
            return valor
        
        elif tipo == 'AtribuicaoAtributo':
            objeto = self.avaliar(no['objeto'])
            valor = self.avaliar(no['valor'])
            
            setattr(objeto, no['nome'], valor)
            return valor
        
        elif tipo == 'ChamadaExpressao':
            funcao = self.avaliar(no['funcao'])
            argumentos = [self.avaliar(arg) for arg in no['argumentos']]
            
            if not callable(funcao):
                raise ErroTupa(f"Não é possível chamar um não-callable: {funcao}")
            
            return funcao(*argumentos)
        
        elif tipo == 'IndexacaoExpressao':
            objeto = self.avaliar(no['objeto'])
            indice = self.avaliar(no['indice'])
            
            try:
                return objeto[indice]
            except (IndexError, KeyError):
                raise ErroTupa(f"Índice inválido: {indice}")
            except TypeError:
                raise ErroTupa(f"Objeto não indexável: {objeto}")
        
        elif tipo == 'AtributoExpressao':
            objeto = self.avaliar(no['objeto'])
            
            try:
                return getattr(objeto, no['nome'])
            except AttributeError:
                raise ErroTupa(f"Atributo não encontrado: '{no['nome']}'")
        
        elif tipo == 'ListaExpressao':
            elementos = [self.avaliar(elem) for elem in no['elementos']]
            return elementos
        
        elif tipo == 'DicionarioExpressao':
            dicionario = {}
            for par in no['pares']:
                chave = self.avaliar(par['chave'])
                valor = self.avaliar(par['valor'])
                dicionario[chave] = valor
            return dicionario
        
        else:
            raise ErroTupa(f"Tipo de expressão desconhecido: {tipo}")

class BreakException(Exception):
    """Exceção usada para implementar o comando 'break'"""
    pass

class ContinueException(Exception):
    """Exceção usada para implementar o comando 'continue'"""
    pass

def executar_arquivo(caminho):
    """Executa um arquivo Tupã"""
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            codigo = arquivo.read()
        
        executar_codigo(codigo)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho}")
    except Exception as e:
        print(f"Erro ao executar o arquivo: {e}")

def executar_codigo(codigo):
    """Executa um código Tupã"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenizar()
    
    parser = Parser(tokens)
    arvore = parser.analisar()
    
    interpretador = Interpretador()
    interpretador.interpretar(arvore)

def iniciar_shell():
    """Inicia um shell interativo para a linguagem Tupã"""
    print("Bem-vindo ao Shell Tupã!")
    print("Digite 'sair' para sair.")
    
    interpretador = Interpretador()
    
    while True:
        try:
            codigo = input(">>> ")
            
            if codigo.lower() == 'sair':
                break
            
            lexer = Lexer(codigo)
            tokens = lexer.tokenizar()
            
            parser = Parser(tokens)
            arvore = parser.analisar()
            
            interpretador.interpretar(arvore)
        except ErroTupa as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro interno: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Executa o arquivo especificado
        executar_arquivo(sys.argv[1])
    else:
        # Inicia o shell interativo
        iniciar_shell()