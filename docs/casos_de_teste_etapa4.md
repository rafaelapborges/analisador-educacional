# Etapa 4 — Casos de teste planejados

**Estado:** planejamento acadêmico; a execução do parser, da AST e da nova suíte deverá ser registrada após implementação. Os casos de validação léxica/regressão que já existem podem ser reexecutados, mas não são declarados aqui como resultados novos.

| ID | Categoria | Entrada ou cenário | Resultado esperado |
| --- | --- | --- | --- |
| CT-01 | Válido | numero = 10 | 3 tokens; AST de atribuição |
| CT-02 | Válido | x = 1 + 2 * 3 | AST respeita multiplicação antes da soma |
| CT-03 | Válido | x = (1 + 2) * 3 | AST respeita parênteses |
| CT-04 | Válido | print("oi") | Chamada simples aceita se incluída no parser |
| CT-05 | Válido | if x > 0: + bloco recuado | AST com condição e corpo |
| CT-06 | Válido | if x: ... else: ... | Árvore com ramo alternativo |
| CT-07 | Válido | while x < 10: + atribuição | AST com laço e corpo |
| CT-08 | Válido | while x: + if aninhado | AST com níveis hierárquicos |
| CT-09 | Léxico | x = 1 @ 2 | Erro léxico localizado; parser não executado |
| CT-10 | Sintático | x = 1 + * 2 | Erro: operador sem operando válido |
| CT-11 | Sintático | if x > 2 sem : | Erro: dois-pontos ausentes |
| CT-12 | Sintático | if x: + bloco sem recuo | Erro: falta de indentação |
| CT-13 | Sintático | else: desacompanhado | Erro: else sem if |
| CT-14 | Sintático | print(1 | Erro: fechamento de parêntese ausente |
| CT-15 | Validação | Entrada somente espaços | 400; ENTRADA_VAZIA |
| CT-16 | Limite | Código > 12.000 caracteres | 413; ENTRADA_LONGA |
| CT-17 | Borda | Somente comentário | Scanner sem tokens; programa vazio ou mensagem conforme contrato sintático definido |
| CT-18 | Regressão | numero = 10 | Tokens idênticos aos da Etapa 3 |
| CT-19 | Interface | Exemplo válido | Tokens e AST legíveis |
| CT-20 | Responsividade | Janela de 390 px | Sem overflow horizontal global |
| CT-21 | Semântica | Identificador não declarado | Fora da pontuação da Etapa 4 |
| CT-22 | Sintático | Tabulação na indentação | Diagnóstico de tabulação em recuo, segundo a regra de indentação adotada |
| CT-23 | Léxico | x = 12abc | Erro de literal numérico malformado; parser não executado |
| CT-24 | Léxico | nome = "texto sem fechamento | Erro de string não terminada com linha/coluna |
| CT-25 | Recuperação | x = 1 @ 2; em outra linha, y = 3 | Erro léxico em @; tokens válidos de y = 3 preservados; parser não executado |
| CT-26 | Sintático | if = 2 | Erro: palavra reservada no lugar de identificador |
| CT-27 | Borda | while x: + blocos aninhados | AST ou diagnóstico coerente para aninhamento até o limite documentado |

## Registro a preencher após execução

| ID | Resultado observado | Status | Defeito / correção |
| --- | --- | --- | --- |
| A preencher | A preencher | Pendente | A preencher |

Teste automatizado disponível na Etapa 3: `python -m pytest tests -v`. Novos testes do parser ainda precisam ser incorporados ao código.
