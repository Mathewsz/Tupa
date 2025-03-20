# Tupã Programming Language

## Filosofia (Philosophy)

"Simplicidade na escrita, poder na execução." (Simplicity in writing, power in execution.)

Tupã aims to minimize verbosity and maximize expressiveness, reflecting the natural flow of the Brazilian Portuguese language. It is designed to be accessible to beginners while remaining powerful enough for experienced developers to build complex systems.

## Tipagem (Typing)

Tupã uses dynamic typing by default, meaning that the type of a variable is checked at runtime. However, it also supports optional static type annotations to improve safety and performance in larger projects. The type system infers types whenever possible, reducing the need for explicit declarations.

### Tipos Primitivos (Primitive Types)

*   `inteiro` (integer): Represents whole numbers (e.g., `10`, `-5`, `0`).
*   `real` (real/float): Represents numbers with decimal points (e.g., `3.14`, `-2.5`, `0.0`).
*   `cadeia` (string): Represents text (e.g., `"Olá, mundo!"`, `"Tupã"`).
*   `booleano` (boolean): Represents truth values (`verdadeiro` or `falso`).
*   `nulo` (null): Represents the absence of a value.

### Estruturas de Dados (Data Structures)

*   `lista` (list/array): An ordered collection of items (e.g., `[1, 2, 3]`, `["a", "b", "c"]`).
*   `dicionário` (dictionary/map): A collection of key-value pairs (e.g., `{ "nome": "Tupã", "versão": "1.0" }`).

## Paradigmas (Paradigms)

Tupã natively supports imperative, functional, and object-oriented programming paradigms. This allows developers to choose the most appropriate paradigm for each task.

*   **Imperativo (Imperative):** Code is written as a sequence of commands that modify the program's state.
*   **Funcional (Functional):** Code is written as a series of function calls, emphasizing immutability and avoiding side effects.
*   **Orientada a Objetos (Object-Oriented):** Code is organized around objects, which encapsulate data and behavior.

## Sintaxe (Syntax)

Tupã's syntax is designed to be intuitive and easy to learn, especially for those familiar with Brazilian Portuguese.

### Variáveis (Variables)

*   **Declaração e atribuição (Declaration and assignment):**

    ```tupã
    criar <nome> = <expressão> # Type inference
    ```
*   **Atribuição múltipla (Multiple assignment):**

    ```tupã
    criar a, b = 1, 2
    ```

### Saída (Output)

*   **Mostrar (Print to console):**

    ```tupã
    mostrar <expressão>
    ```

### Entrada (Input)

*   **Pegar (Read user input):**

    ```tupã
    pegar <nome> [mensagem] # Optional message
    ```

### Condicionais (Conditionals)

```tupã
se <condição> então
    <bloco>
senão se <condição> então
    <bloco>
senão
    <bloco>
fim
```

### Laços (Loops)

*   **Enquanto (While loop):**

    ```tupã
    enquanto <condição> fazer
        <bloco>
    fim
    ```
*   **Para (For loop - range):**

    ```tupã
    para <variável> de <início> até <fim> [passo <incremento>] fazer
        <bloco>
    fim
    ```
*   **Para (For loop - collection):**

    ```tupã
    para <elemento> em <coleção> fazer
        <bloco>
    fim
    ```

### Funções (Functions)

*   **Declaração (Declaration):**

    ```tupã
    função <nome>(<parâmetros>)
        <bloco>
    fim
    ```
*   **Retorno (Return):**

    ```tupã
    devolver <expressão>
    ```
*   **Funções anônimas (Anonymous functions/lambdas):**

    ```tupã
    função(<parâmetros>) devolver <expressão>
    ```

### Listas (Lists/Arrays)

*   **Declaração (Declaration):**

    ```tupã
    criar lista <nome> = [<expressão1>, <expressão2>, ...]
    ```
*   **Acesso (Access):**

    ```tupã
    <nome>[<índice>] # 0-based indexing
    ```
*   **Métodos (Methods):**
    *   `.tamanho` (size/length)
    *   `.adicionar(<elemento>)` (add element)
    *   `.remover(<índice>)` (remove element at index)

### Dicionários (Dictionaries/Maps)

*   **Declaração (Declaration):**

    ```tupã
    criar dicionário <nome> = {<chave>: <valor>, ...}
    ```
*   **Acesso (Access):**

    ```tupã
    <nome>[<chave>]
    ```
*   **Métodos (Methods):**
    *   `.chaves` (keys)
    *   `.valores` (values)
    *   `.contém(<chave>)` (contains key)

### Orientação a Objetos (Object-Oriented Programming)

*   **Classes:**

    ```tupã
    classe <nome>
        <atributos>
        <métodos>
    fim
    ```
*   **Construtores (Constructors):**

    ```tupã
    função inicializar(<parâmetros>)
        <bloco>
    fim
    ```
*   **Herança (Inheritance):**

    ```tupã
    classe <nome> herda de <classe_pai>
        <bloco>
    fim
    ```
*   **Métodos (Methods):**

    ```tupã
    função <nome>(<parâmetros>)
        <bloco>
    fim
    ```
*   **Atributos (Attributes):**

    ```tupã
    criar <nome> = <valor>
    ```

### Tratamento de Exceções (Exception Handling)

```tupã
tentar
    <bloco>
pegar <tipo_de_erro> <nome_da_variável>
    <bloco>
finalmente
    <bloco>
fim
```

### Módulos (Modules)

*   **Importação (Import):**

    ```tupã
    usar <nome_do_módulo> # Imports all functions and classes
    ```
*   **Importação seletiva (Selective import):**

    ```tupã
    usar <nome_do_módulo> com <função1>, <função2>, <Classe1>
    ```

### Comentários (Comments)

```tupã
# Comentário de uma linha (Single-line comment)
```

## Recursos Avançados (Advanced Features)

*   **Concorrência (Concurrency):**

    Tupã supports concurrent programming through goroutines (similar to Go) and channels for communication between them.

    *   `vá <função>(<argumentos>)` (go routine - starts a new goroutine)
    *   `criar canal <nome>` (create channel)

*   **Metaprogramação (Metaprogramming):**

    Tupã allows manipulating the language's code at runtime, enabling the creation of DSLs (Domain-Specific Languages) and other advanced abstractions.

*   **Interoperabilidade (Interoperability):**

    Tupã provides mechanisms to interact with code written in other languages, such as C and Python.

*   **Sistema de Módulos (Module System):**

    A robust system for organizing and reusing code, with support for dependency management.

## Biblioteca Padrão (Standard Library)

Tupã includes a comprehensive standard library with modules for:

*   Operações de entrada/saída (Input/Output operations - files, network)
*   Manipulação de strings (String manipulation)
*   Estruturas de dados (Data structures - lists, dictionaries, sets)
*   Funções matemáticas (Mathematical functions)
*   Expressões regulares (Regular expressions)
*   Suporte para JSON e outros formatos de dados (JSON and other data formats support)

## Exemplo de Código (Code Example)

### Calculando o fatorial de um número (Calculating the factorial of a number)

```tupã
função fatorial(n)
    se n == 0 então
        devolver 1
    senão
        devolver n * fatorial(n - 1)
    fim
fim

pegar numero "Digite um número: "
numero = para_inteiro(numero) # Converte a entrada para inteiro

se numero >= 0 então
    criar resultado = fatorial(numero)
    mostrar "O fatorial de " + numero + " é " + resultado
senão
    mostrar "Número inválido. Digite um número não negativo."
fim
```

## Detalhes da Implementação (Implementation Details)

### Semântica (Semantics)

Each command in Tupã has a specific meaning and effect on the program's state. The semantics are designed to be clear and consistent, making it easier to understand and predict the behavior of Tupã code.

### Sistema de Tipos (Type System)

Tupã's type system combines dynamic typing with optional static type annotations. This allows for rapid prototyping and flexibility while also providing the option to add type safety and performance optimizations when needed.

### Modelo de Memória (Memory Model)

Tupã uses a managed memory model with automatic garbage collection. This means that developers do not need to manually allocate and deallocate memory, reducing the risk of memory leaks and other memory-related errors.

### Coleta de Lixo (Garbage Collection)

Tupã's garbage collector automatically reclaims memory that is no longer being used by the program. The garbage collector is designed to be efficient and non-intrusive, minimizing the impact on program performance.

### Regras de Escopo (Scoping Rules)

Tupã uses lexical scoping, meaning that the scope of a variable is determined by its position in the source code. Variables are accessible within the block in which they are defined, as well as any nested blocks.

### Compilação/Interpretação (Compilation/Interpretation)

Tupã can be implemented as either a compiled or an interpreted language. A compiled implementation would translate Tupã code into machine code, which can then be executed directly by the computer's processor. An interpreted implementation would execute Tupã code directly, without the need for a separate compilation step.