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
        # Check for specific commands first
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
        elif linha.startswith("para "):
            return self.executar_para(linha, i, linhas)
        # Check for assignment last, to avoid confusion with other commands
        elif re.match(r"^\w+ = .+$", linha):
            match = re.match(r"^(\w+) = (.+)$", linha)
            if match:
                nome, valor = match.groups()
                self.variables[nome] = self.avaliar_expressao(valor)
            return i + 1
        else:
            print(f"Erro: Comando desconhecido: {linha}")
            return i + 1

    def declarar_variavel(self, linha):
        match = re.match(r"criar (\w+) = (.+)", linha)
        if match:
            nome, valor = match.groups()
            try:
                self.variables[nome] = ast.literal_eval(valor)
            except (ValueError, SyntaxError) as e:
                print(f"Erro ao declarar variável: {e}")
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
                    next_i = self.executar_linha(linhas[i].strip(), i, linhas)
                    if next_i is not None:
                        i = next_i
                    else:
                        i += 1  # Fallback to avoid infinite loop
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
                            next_i = self.executar_linha(linhas[i].strip(), i, linhas)
                            if next_i is not None:
                                i = next_i
                            else:
                                i += 1  # Fallback
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
            loop_start = i + 1  # Store the start of the loop
            
            # Process the loop
            while self.avaliar_condicao(condicao):
                # Execute loop body
                j = loop_start
                while j < len(linhas) and linhas[j].strip() != "fim":
                    j = self.executar_linha(linhas[j].strip(), j, linhas)
                    
            # Skip to the "fim"
            i = loop_start
            while i < len(linhas) and not linhas[i].strip() == "fim":
                i += 1
            return i + 1
        else:
            print(f"Erro: Sintaxe inválida para enquanto: {linha}")
            return i + 1

    def executar_para(self, linha, i, linhas):
        match = re.match(r"para (\w+) de (.+) até (.+) fazer", linha)
        if match:
            var_name, start_val, end_val = match.groups()
            start = int(self.avaliar_expressao(start_val))
            end = int(self.avaliar_expressao(end_val))

            i += 1
            loop_start = i

            for var_value in range(start, end + 1):
                self.variables[var_name] = float(var_value)  # Store as float for consistency
                i = loop_start
                while i < len(linhas) and linhas[i].strip() != "fim":
                    i = self.executar_linha(linhas[i].strip(), i, linhas)

            # Skip to the "fim"
            while i < len(linhas) and not linhas[i].strip() == "fim":
                i += 1
            return i + 1
        elif match := re.match(r"para (\w+) em (.+) fazer", linha):
            var_name, collection_name = match.groups()
            if collection_name in self.variables:
                collection = self.variables[collection_name]
                if isinstance(collection, list):
                    i += 1
                    loop_start = i
                    for item in collection:
                        self.variables[var_name] = item
                        i = loop_start
                        while i < len(linhas) and linhas[i].strip() != "fim":
                            i = self.executar_linha(linhas[i].strip(), i, linhas)

                    # Skip to the "fim"
                    while i < len(linhas) and not linhas[i].strip() == "fim":
                        i += 1
                    return i + 1
                else:
                    print(f"Erro: '{collection_name}' não é uma lista.")
                    return i + 1
            else:
                print(f"Erro: Coleção '{collection_name}' não definida.")
                return i + 1
        else:
            print(f"Erro: Sintaxe inválida para para: {linha}")
            return i + 1

    def avaliar_condicao(self, condicao):
        try:
            operadores = [">=", "<=", "==", "!=", ">", "<"]
            operador_encontrado = None
            for operador in operadores:
                if operador in condicao:
                    operador_encontrado = operador
                    break

            if operador_encontrado:
                partes = condicao.split(operador_encontrado)
                if len(partes) == 2:
                    esquerda = partes[0].strip()
                    direita = partes[1].strip()
                    return self.evaluar_comparacao(esquerda, operador_encontrado, direita)
                else:
                    print(f"Erro: Condição mal formada: {condicao}")
                    return False
            else:
                return bool(self.avaliar_expressao(condicao))
        except Exception as e:
            print(f"Erro ao avaliar condição: {e}")
            return False

    def evaluar_comparacao(self, esquerda, operador, direita):
        esquerda_valor = self.avaliar_expressao(esquerda)
        direita_valor = self.avaliar_expressao(direita)

        try:
            esquerda_num = float(esquerda_valor)
            direita_num = float(direita_valor)

            if operador == ">":
                return esquerda_num > direita_num
            elif operador == "<":
                return esquerda_num < direita_num
            elif operador == "==":
                return esquerda_num == direita_num
            elif operador == "!=":
                return esquerda_num != direita_num
            elif operador == ">=":
                return esquerda_num >= direita_num
            elif operador == "<=":
                return esquerda_num <= direita_num
        except (ValueError, TypeError):
            if operador == "==":
                return str(esquerda_valor) == str(direita_valor)
            elif operador == "!=":
                return str(esquerda_valor) != str(direita_valor)
            else:
                print(f"Erro: Comparação de strings inválida com operador: {operador}")
                return False

    def avaliar_expressao(self, expressao):
        expressao = expressao.strip()

        if expressao.startswith('"') and expressao.endswith('"'):
            return expressao[1:-1]

        if expressao in self.variables:
            return self.variables[expressao]

        try:
            return float(expressao)
        except ValueError:
            try:
                expr_copy = expressao
                for var, val in sorted(self.variables.items(), key=lambda x: len(x[0]), reverse=True):
                    pattern = r'\b' + re.escape(var) + r'\b'
                    expr_copy = re.sub(pattern, str(val), expr_copy)

                try:
                    if all(c in "0123456789.+-*/() " for c in expr_copy):
                        return eval(expr_copy, {"__builtins__": {}})
                    else:
                        return expressao
                except:
                    return expressao
            except:
                return expressao

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

para i de 1 até 5 fazer
    mostrar i
fim

criar nomes = ["Tupã", "Anhangá", "Iara"]
para nome em nomes fazer
    mostrar nome
fim
"""

interpreter = TupaInterpreter()
interpreter.interpretar(codigo_tupa)