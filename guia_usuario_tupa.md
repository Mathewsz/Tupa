# Guia do Usuário da Linguagem Tupã

## Introdução

Bem-vindo ao guia do usuário da linguagem de programação Tupã! Esta linguagem foi criada para ser fácil de aprender e usar, especialmente para falantes de português brasileiro.

## Sintaxe Básica

### Variáveis

Para declarar uma variável, use a palavra-chave `criar`:

```tupã
criar <nome_da_variável> = <valor>
```

Exemplo:

```tupã
criar nome = "Tupã"
criar idade = 10
mostrar nome # Imprime "Tupã"
mostrar idade # Imprime 10
```

### Saída

Para mostrar um valor na tela, use a palavra-chave `mostrar`:

```tupã
mostrar <expressão>
```

Exemplo:

```tupã
mostrar "Olá, mundo!" # Imprime "Olá, mundo!"
mostrar nome # Imprime o valor da variável nome
mostrar idade + 5 # Imprime o resultado da expressão idade + 5
```

### Entrada

Para ler a entrada do usuário, use a palavra-chave `pegar`:

```tupã
pegar <nome_da_variável> [mensagem]
```

Exemplo:

```tupã
pegar nome "Digite seu nome: "
mostrar "Olá, " + nome # Imprime "Olá, " seguido do nome digitado
```

### Condicionais

Para criar condicionais, use as palavras-chave `se`, `então`, `senão se`, `senão` e `fim`:

```tupã
se <condição> então
    <bloco_de_código>
senão se <condição> então
    <bloco_de_código>
senão
    <bloco_de_código>
fim
```

Exemplo:

```tupã
criar idade = 20
se idade >= 18 então
    mostrar "Você é maior de idade."
senão
    mostrar "Você é menor de idade."
fim

criar numero = 10
se numero > 5 então
    mostrar "Número é maior que 5"
senão se numero == 5 então
    mostrar "Número é igual a 5"
senão
    mostrar "Número é menor que 5"
fim
```

### Laços

#### Enquanto

Para criar um laço `enquanto`, use as palavras-chave `enquanto`, `fazer` e `fim`:

```tupã
enquanto <condição> fazer
    <bloco_de_código>
fim
```

Exemplo:

```tupã
criar contador = 0
enquanto contador < 10 fazer
    mostrar contador
    criar contador = contador + 1
fim
```

#### Para

Para criar um laço `para`, você pode usar um intervalo de números ou uma coleção:

```tupã
para <variável> de <início> até <fim> [passo <incremento>] fazer
    <bloco_de_código>
fim

para <elemento> em <coleção> fazer
    <bloco_de_código>
fim
```

Exemplo:

```tupã
para i de 1 até 5 fazer
    mostrar i
fim

criar lista nomes = ["Tupã", "Anhangá", "Iara"]
para nome em nomes fazer
    mostrar nome
fim
```

### Funções

Para declarar uma função, use a palavra-chave `função`:

```tupã
função <nome_da_função>(<parâmetros>)
    <bloco_de_código>
    devolver <valor>
fim
```

Exemplo:

```tupã
função somar(a, b)
    devolver a + b
fim

criar resultado = somar(5, 3)
mostrar resultado # Imprime 8
```

## Tipos de Dados

Tupã suporta os seguintes tipos de dados:

*   `inteiro`: Números inteiros (ex: 10, -5, 0)
*   `real`: Números decimais (ex: 3.14, -2.5, 0.0)
*   `cadeia`: Textos (ex: "Olá, mundo!", "Tupã")
*   `booleano`: Valores lógicos (verdadeiro ou falso)
*   `lista`: Listas de valores (ex: \[1, 2, 3], \["a", "b", "c"])
*   `dicionário`: Dicionários de chave-valor (ex: { "nome": "Tupã", "versão": "1.0" })

## Operadores

Tupã suporta os seguintes operadores:

*   Aritméticos: `+`, `-`, `*`, `/`, `%`
*   Comparação: `==`, `!=`, `>`, `<`, `>=`, `<=`
*   Lógicos: `e`, `ou`, `não`

## Próximos Passos

Este guia é apenas uma introdução à linguagem Tupã. Para aprender mais, consulte a documentação completa da linguagem.