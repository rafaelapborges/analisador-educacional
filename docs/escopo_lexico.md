# Subconjunto léxico do LexLab — Etapa 3

A linguagem de entrada é um subconjunto didático inspirado em Python. O objetivo nesta etapa é **identificar lexemas e categorias**, não executar o programa nem verificar sua gramática. Os exemplos abaixo são a especificação usada pelos testes automatizados.

| Categoria | Reconhecimento | Exemplos |
| --- | --- | --- |
| Reservadas | `if`, `elif`, `else`, `while`, `and`, `or`, `not`, `True`, `False`, `None`, `pass` | `if`, `True` |
| Identificador | `[A-Za-z_][A-Za-z0-9_]*` | `x`, `_nota2` |
| Inteiro | `[0-9]+` | `0`, `16` |
| Real | `[0-9]+\.[0-9]+` | `12.5` |
| String | Aspas `'` ou `"`, com escapes `\\`, `\"`, `\'`, `\n`, `\r`, `\t`, `\0` | `"Ana"`, `'oi'` |
| Operador | `==`, `!=`, `<=`, `>=`, `**`, `//`, `+`, `-`, `*`, `/`, `%`, `=`, `<`, `>` | `>=`, `+` |
| Delimitador | `(`, `)`, `[`, `]`, `{`, `}`, `:`, `,` | `(`, `:` |
| Comentário | `#` até a quebra de linha | `# exemplo` (ignorado) |
| Espaços | Branco, tabulação, novas linhas | Ignorados, mas atualizam linha e coluna |
| Erros léxicos | Caracteres não listados, números malformados e strings inválidas | `@`, `12abc`, `"aberto` |

## Observações importantes

- O scanner usa correspondência mais longa para operadores compostos (`>=` antes de `>` + `=`).
- O scanner percorre a entrada caractere a caractere, guardando linha e coluna a partir de 1. CRLF conta como uma única mudança de linha.
- Erros são adicionados à lista `erros`; o scanner tenta continuar após o trecho problemático para mostrar problemas posteriores.
- `print` é identificador no scanner, não palavra reservada.
- Não há blocos de comentários `/* */`, porque o escopo é inspirado em Python; a forma suportada é `#`.
- Não existem tokens `INDENT` / `DEDENT`, f-strings, strings triplas, identificadores Unicode, notação exponencial, literais binários/hexadecimais e outras estruturas completas de Python.
- A ausência de erros léxicos **não comprova** sintaxe válida: verificar se os tokens formam um programa correto será tarefa da Etapa 4.
- O código-fonte é tratado como texto; **nunca é executado** pelo backend.

## Exemplos do contrato

### Entrada válida

```python
nota = 8.5
if nota >= 7:
    print("Aprovado")
```

O scanner reconhece palavras reservadas, identificadores, número real, operador composto, delimitadores e string. A indentação ainda não é analisada.

### Entrada com erro

```python
numero = 10
total = numero @ 2
```

`@` é reportado como `ERRO_LEXICO` com linha/coluna; outros tokens reconhecidos são retornados normalmente para fins pedagógicos.
