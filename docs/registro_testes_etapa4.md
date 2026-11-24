# Registro de validação - LexLab Etapa 4

## Ambiente de preparação do pacote (24/11/2026)

O código da Etapa 4 foi aplicado sobre uma cópia dos arquivos das Etapas 2 e 3. O scanner da Etapa 3 foi mantido, com validação dos testes de regressão.

| Teste | Procedimento | Resultado |
|---|---|---|
| Scanner, parser, serviço e interface | `python -m pytest tests -q` | **101 aprovados, 0 falhas** |
| Sintaxe Python | `python -m compileall -q backend tests` | Sem erros |
| Sintaxe JavaScript | `node --check frontend/script.js` e `node --check frontend/ast_ui.js` | Sem erros |
| Erro sintático didático | `if nota >= 7` seguido de `    pass` | HTTP 422; AST nula; esperado `:`; regra e sugestão presentes |
| Sucesso sintático | `resultado = 10 + 5 * 2` | HTTP 200; AST com adição e multiplicação corretamente aninhadas |
| Regressão léxica | `numero = 10 $ 2` | HTTP 422; erro léxico; parser não executado |

A suíte de navegador utiliza Playwright + Chromium com o servidor de pré-visualização local do projeto, **não equivale a executar Flask/Nginx em Docker**. Os testes de integração com Docker e os prints da execução no Windows do estudante ainda precisam ser feitos nesse ambiente.

## Conferências obrigatórias no Windows antes de publicar

- [ ] Copiar a atualização para o repositório já clonado, usando `aplicar_etapa4.bat`.
- [ ] `python -m pytest tests -v` - registrar quantidade de testes e falhas.
- [ ] `docker compose up --build -d` - conferir `docker compose ps`.
- [ ] Abrir `http://localhost:8080` e testar programa válido com AST.
- [ ] Testar `if nota >= 7` sem `:` e conferir regra/esperado/sugestão.
- [ ] Testar `numero = 10 $ 2`, confirmando erro léxico separado.
- [ ] Conferir controles para expandir árvore e selecionar trecho no editor.
- [ ] Registrar print real do navegador no Docker.
- [ ] Revisar Changes no GitHub Desktop, fazer commit/push **somente após os testes**.

## Limites

O parser suporta o subconjunto didático delimitado em `gramatica_etapa4.md`, não Python integral. A integração opcional com Ollama/Llama 3.2 **não foi implementada**. A análise semântica fica para a Etapa 5.
