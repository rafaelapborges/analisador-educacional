# LexLab — Gramática e decisões da Etapa 4

## Natureza do subconjunto

A linguagem **não é Python completo**: é um subconjunto inspirado em Python. O scanner da Etapa 3 ignora quebras de linha e espaços; o parser da Etapa 4 recupera os limites dos comandos a partir do atributo `linha` de cada token e calcula os níveis de indentação a partir do texto original. Não executa código nem realiza verificação semântica.

## Gramática didática (EBNF simplificada)

```ebnf
programa     = { comando } ;
comando      = atribuicao | expressao | passar | condicional | repeticao ;
atribuicao   = IDENTIFICADOR, "=", expressao ;
passar       = "pass" ;
condicional  = "if", expressao, ":", BLOCO, { "elif", expressao, ":", BLOCO }, [ "else", ":", BLOCO ] ;
repeticao    = "while", expressao, ":", BLOCO ;
BLOCO        = NOVA_LINHA, INDENTACAO_4_ESPACOS, comando, { comando }, FIM_BLOCO ;
expressao    = expressao_binaria | [ "+" | "-" | "not" ], expressao | primario ;
primario     = IDENTIFICADOR | INTEIRO | REAL | STRING | "True" | "False" | "None"
             | "(", expressao, ")" | chamada ;
chamada      = IDENTIFICADOR, "(", [ expressao, { ",", expressao } ], ")" ;
```

A EBNF acima descreve as construções, mas deixa a precedência para a tabela a seguir; a implementação usa precedência vinculada (Pratt/precedence-climbing) dentro de um parser descendente para comandos. As atribuições e os comandos são limitados à mesma linha lógica. Em blocos, cada nível utiliza **exatamente quatro espaços a mais** que o comando pai. Os nomes `INDENTACAO_4_ESPACOS`, `FIM_BLOCO` e `NOVA_LINHA` são abstrações didáticas derivadas do código-fonte, não tokens emitidos pelo scanner.

| Precedência crescente | Operadores | Associatividade |
|---|---|---|
| 1 | `or` | esquerda |
| 2 | `and` | esquerda |
| 2,5 | `not` prefixo | prefixo |
| 3 | `== != < <= > >=` | esquerda (encadeamento Python não contemplado) |
| 4 | `+ -` binários | esquerda |
| 5 | `* / // %` | esquerda |
| 7 | `+ -` unários e `**` | `**` direita; unários prefixos |

**Limitação importante:** a precedência de operadores prefixos e `**` é didática e não reproduz todos os casos de precedência do Python real, mas `not` tem escopo sobre comparações e é avaliado antes de `and`/`or`. Usar exemplos básicos (`-x`, `x**2`, `not x`) e declarar a diferença.

## Nós JSON da AST

- `Programa` com `corpo[]`;
- `Atribuicao` com `alvo`, `valor`;
- `Literal` e `Identificador`;
- `Binario` / `Unario` com operador e operandos;
- `Chamada` com `funcao`, `argumentos[]`;
- `Expressao`, `Se` com `ramos[]`, `senao[]`, `Enquanto`, `Passar`.

Os nós guardam `linha`, `coluna`, `inicio` e `fim` (posição no código) quando disponíveis; o botão de localizar seleciona o trecho no editor. Trata-se de uma **AST**, não árvore de derivação: não são mantidos todos os símbolos terminadores da gramática.

## API: compatibilidade

`POST /api/analisar` conserva `tokens`, `erros`, `contagem`, `ok`, `sucesso`, `recebido`, `mensagem`, `linhas`, `caracteres` e os códigos de erro de validação anteriores. A Etapa 4 acrescenta:

```json
{
  "ast": {"tipo":"Programa","corpo":[]},
  "erros_sintaticos": [],
  "sintaxe": {"status":"valida","valida":true}
}
```

- **200:** entrada bem formada e sem erros lexicais/sintáticos;
- **422 lexical:** preserva tokens parciais e `erros`, define `ast=null`, `sintaxe.status="nao_executada"`;
- **422 sintático:** `erros=[]`, `erros_sintaticos` preenchido, `ast=null`, `sintaxe.status="com_erros"`;
- **400/413/415:** validação da entrada como antes.

A decisão de não executar o parser diante de erro léxico evita produzir diagnósticos em cascata a partir de tokens ausentes.

## Fora do escopo da Etapa 4

`for`, `def`, `return`, `break`, `continue`, dicionários, listas, indexação, atributos (`obj.x`), comentários multilinha, f-strings, identação com tabs, expressões multilinha, cadeias de comparação complexas, chamada com argumentos nomeados e semântica de nomes/tipos. A AST não é executada. **Análise semântica e tabela de símbolos serão planejadas na Etapa 5**, ainda não implementadas.

## Limitações de robustez

Entrada limitada a 12.000 caracteres pelo serviço. Profundidade recursiva limitada a 32 níveis; até 30 diagnósticos sintáticos são registrados. A árvore visual é abreviada após 800 elementos ou profundidade visual de 18 nós. Erros múltiplos podem ser detectados no mesmo envio, mas a AST é nula se houver erro sintático, para não apresentar uma estrutura incompleta como válida. O parser pode deixar de recuperar certas estruturas aninhadas malformadas.
