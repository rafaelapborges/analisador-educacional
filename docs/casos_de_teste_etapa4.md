# LexLab — Casos de teste predefinidos (Etapa 4)

**Estado:** plano elaborado antes da interpretação de resultados do novo parser. **Não confundir** com testes já executados na Etapa 3.

| ID | Classe | Entrada | Resultado esperado | Evidência |
|---|---|---|---|---|
| CT-01 | Válido / atribuição | `numero = 10` | 3 tokens; AST Programa > Atribuicao | scanner + AST |
| CT-02 | Válido / precedência | `x = 1 + 2 * 3` | raiz da expressão `+`, filho direito `*` | AST |
| CT-03 | Válido / parênteses | `x = (1 + 2) * 3` | raiz `*`, filho esquerdo `+` | AST |
| CT-04 | Válido / chamada | `print("oi")` | nó Chamada com argumento Literal | AST |
| CT-05 | Válido / condicional | `if x > 0:\n    pass` | nó Se, condição e corpo | AST |
| CT-06 | Válido / else | `if x:\n    pass\nelse:\n    pass` | Se com ramo `senao` | AST |
| CT-07 | Válido / repetição | `while x < 10:\n    x = x + 1` | Enquanto com corpo | AST |
| CT-08 | Válido / bloco aninhado | `while x:\n    if x:\n        pass` | AST hierárquica aninhada | AST |
| CT-09 | Léxico | `x = 1 @ 2` | 422, erro léxico com posição; parser não executado | JSON |
| CT-10 | Sintático | `x = 1 + * 2` | 422, erro sintático | JSON |
| CT-11 | Sintático | `if x > 2\n    pass` | erro por falta de `:` | JSON |
| CT-12 | Sintático | `if x:\npass` | erro por bloco sem indentação | JSON |
| CT-13 | Sintático | `else:\n    pass` | erro de `else` desacompanhado | JSON |
| CT-14 | Sintático | `print(1` | erro por fechamento de `)` ausente | JSON |
| CT-15 | Entrada | espaço em branco | HTTP 400, ENTRADA_VAZIA | HTTP |
| CT-16 | Borda | > 12.000 caracteres | HTTP 413, ENTRADA_LONGA | HTTP |
| CT-17 | Borda | somente comentário `# oi` | AST vazia, sem erros | API |
| CT-18 | Regressão | `numero = 10` | mesmas categorias/posições da Etapa 3 | testes legados |
| CT-19 | Interface | exemplo válido | tabela de tokens e árvore hierárquica legíveis | inspeção |
| CT-20 | Responsividade | 390px largura | navegação sem rolagem horizontal global | Playwright |
| CT-21 | Semântico (futuro) | uso de variável não declarada | **Pendente Etapa 5**; não avaliar como implementado | plano |
| CT-22 | Borda | código com tab na indentação | erro sintático de indentação | JSON |

**Modelo de registro por execução:** data, ambiente, caso, entrada, saída esperada, saída observada, aprovado/reprovado/pendente, defeito, correção, responsável. Somente marque `aprovado` após executar o teste no ambiente correspondente; esta tabela define expectativas.
