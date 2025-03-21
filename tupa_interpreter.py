print("Executando o interpretador Tupã...")

import re
import ast

class TupaInterpreter:
    def __init__(self):
        self.variables = {}

    def interpretar(self, codigo):
        linhas = codigo.splitlines()
        i = 0
        while i < len(linhas):
            linha = linhas[i].strip()
            if not linha:
                i += 1
                continue
            i = self.executar_linha(linha, i, linhas)

    def executar_linha(self, linha, i, linhas):
        if linha.startswith("criar "):
            self.declarar_variavel(linha)
            return i + 1
        elif linha.startswith("mostrar "):
            self.mostrar_valor(linha)
            return i + 1
        elif linha.startswith("se "):
            return self.executar_condicional(linha, i, linhas)
        elif linha.startswith("enquanto "):
            return self.executar_enquanto(linha, i, linhas)
        else:
            # Check if it's an assignment to an existing variable
            match = re.match(r"(\w+) = (.+)", linha)
            if match:
                nome, valor = match.groups()
                if nome in self.variables:
                    self.variables[nome] = self.avaliar_expressao(valor)
                    return i + 1
                else:
                    print(f"Erro: Variável '{nome}' não declarada.")
                    return i + 1
            else:
                print(f"Erro: Comando desconhecido: {linha}")
                return i + 1

    def declarar_variavel(self, linha):
        match = re.match(r"criar (\w+) = (.+)", linha)
        if match:
            nome, valor = match.groups()
            self.variables[nome] = self.avaliar_expressao(valor)
        else:
            print(f"Erro: Sintaxe inválida para declaração de variável: {linha}")

    def mostrar_valor(self, linha):
        match = re.match(r"mostrar (.+)", linha)
        if match:
            expressao = match.groups()[0]
            valor = self.avaliar_expressao(expressao)
            print(valor)
        else:
            print(f"Erro: Sintaxe inválida para mostrar: {linha}")

    def executar_condicional(self, linha, i, linhas):
        match = re.match(r"se (.+) então", linha)
        if match:
            condicao = match.groups()[0].strip()
            if self.avaliar_condicao(condicao):
                i += 1
                while i < len(linhas) and linhas[i].strip() != "fim" and not linhas[i].strip().startswith("senão"):
                    i = self.executar_linha(linhas[i].strip(), i, linhas)
                # Skip to the "fim"
                while i < len(linhas) and not linhas[i].strip() == "fim":
                    i += 1
                return i + 1

            else:
                # Pular para o "senão" ou "fim"
                i += 1
                while i < len(linhas):
                    linha_atual = linhas[i].strip()
                    if linha_atual == "senão":
                        i += 1
                        while i < len(linhas) and linhas[i].strip() != "fim":
                            i = self.executar_linha(linhas[i].strip(), i, linhas)
                        return i + 1
                    elif linha_atual == "fim":
                        return i + 1
                    else:
                        i += 1
                return i
        else:
            print(f"Erro: Sintaxe inválida para condicional: {linha}")
            return i + 1

    def executar_enquanto(self, linha, i, linhas):
        match = re.match(r"enquanto (.+) fazer", linha)
        if match:
            condicao = match.groups()[0].strip()
            loop_start = i + 1 # Store the start of the loop
            while self.avaliar_condicao(condicao):
                i = loop_start # Reset i to the start of the loop
                while i < len(linhas) and linhas[i].strip() != "fim":
                    i = self.executar_linha(linhas[i].strip(), i, linhas)

            # Skip to the "fim"
            while i < len(linhas) and not linhas[i].strip() == "fim":
                i += 1
            return i + 1
        else:
            print(f"Erro: Sintaxe inválida para enquanto: {linha}")
            return i + 1


    def avaliar_condicao(self, condicao):
        try:
            # Substitute variables in the condition string
            for var, val in self.variables.items():
                condicao = condicao.replace(var, str(val))

            return self.evaluar_comparacao(condicao)
        except Exception as e:
            print(f"Erro ao avaliar condição: {e}")
            return False

    def evaluar_comparacao(self, condicao):
        if ">" in condicao:
            partes = condicao.split(">")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) > float(direita)
        elif "<" in condicao:
            partes = condicao.split("<")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) < float(direita)
        elif "==" in condicao:
            partes = condicao.split("==")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) == float(direita)
        elif "!=" in condicao:
            partes = condicao.split("!=")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) != float(direita)
        elif ">=" in condicao:
            partes = condicao.split(">=")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) >= float(direita)
        elif "<=" in condicao:
            partes = condicao.split("<=")
            if len(partes) == 2:
                esquerda = self.avaliar_expressao(partes[0])
                direita = self.avaliar_expressao(partes[1])
                return float(esquerda) <= float(direita)
        else:
            return bool(self.avaliar_expressao(condicao))


    def avaliar_expressao(self, expressao):
        expressao = expressao.strip()
        try:
            # Tenta avaliar como número
            return float(expressao)
        except ValueError:
            # Se não for número, tenta como variável
            if expressao in self.variables:
                return self.variables[expressao]
            else:
                # Tenta avaliar expressão aritmética
                try:
                    result = eval(expressao, self.variables)
                    return result
                except (NameError, TypeError, SyntaxError):
                    return expressao  # Retorna a string se não for variável

# Exemplo de uso
codigo_tupa = """
criar numero = 10
se numero > 5 então
    mostrar "Número é maior que 5"
senão
    mostrar "Número é menor ou igual a 5"
fim

criar contador = 0
enquanto contador < 5 fazer
    mostrar contador
    contador = contador + 1
fim
"""

interpreter = TupaInterpreter()
interpreter.interpretar(codigo_tupa)