# Etapa 4 — Proposta de materiais, métodos e avaliação (LexLab)

**Natureza deste documento:** proposta de implementação e avaliação, vinculada à etapa acadêmica. Não constitui registro de conclusão do parser ou da AST.

## 1. Contexto e literatura

O LexLab é um ambiente web didático para explorar o processamento de um subconjunto inspirado em Python. A Etapa 3 disponibilizou scanner léxico manual, tokens localizados por linha e coluna, mensagens de erro e navegação pelos tokens. A Etapa 4 prevê ampliar a experiência para análise sintática e representação da árvore sintática abstrata (AST).

O plano acadêmico toma como referências complementares:

- BARBOSA, C. R. S. C.; FARIA, C. R.; CAMPANO JUNIOR, M. M. **Análise de Ferramentas de Compiladores em Ambientes Virtualizados**. *Revista Brasileira de Informática na Educação*, v. 29, p. 1262–1290, 2021. DOI: https://doi.org/10.5753/rbie.2021.2302. O artigo discute ferramentas como GALS, Grammophone, CGFC, Verto e Parsing Simulator, além de relatos de estudantes. A avaliação apresentada não isola ganhos de aprendizagem.
- BORELA, E. P. S.; OLIVEIRA, A. L.; BRANCO NETO, W. C.; SOUZA, A. P. **Uma Ferramenta Educacional de Apoio ao Ensino de Compiladores**. *Workshop sobre Educação em Computação (WEI)*, p. 171–181, 2025. DOI: https://doi.org/10.5753/wei.2025.7407. A ferramenta estudada usa ANTLR e LLVM e permite visualizar artefatos da compilação. O estudo apresenta uma avaliação de aceitação, que não equivale a um experimento de ganho de aprendizagem.

A análise detalhada desses e dos sete trabalhos anteriores, com matriz comparativa e limitações das evidências, consta do trabalho acadêmico da Etapa 4.

## 2. O que existe no repositório publicado

- Frontend HTML, CSS e JavaScript, servido por Nginx, com editor e exemplos.
- Backend Python 3.12 com Flask, via Gunicorn.
- Scanner desenvolvido em Python no arquivo `backend/scanner.py`.
- API `POST /api/analisar`, que recebe `{"codigo":"numero = 10"}` e retorna `tokens`, `erros` e contagem.
- Validação de entrada: `400` para casos inválidos, `413` acima de 12.000 caracteres, `415` para conteúdo não JSON e `422` quando há erros léxicos.
- Docker Compose, com interface em `http://localhost:8080`.
- Testes `pytest` e Playwright disponíveis no diretório `tests`.

**Ainda não estão confirmados na versão publicada:** parser, AST, análise semântica, tabela de símbolos e geração de código. Por isso, nenhuma dessas etapas é indicada aqui como executada.

## 3. Escopo proposto para o parser

O parser da Etapa 4 deverá reconhecer um subconjunto restrito de comandos e expressões, com prioridades para atribuição, expressões aritméticas e comparações, parênteses, condicionais `if`/`else` e repetição `while`. Um conjunto mínimo de chamadas de função embutida poderá ser incluído somente depois de documentado e coberto por testes. Não se pretende oferecer conformidade com toda a gramática da linguagem Python.

**Questão técnica que deverá ser resolvida:** o scanner da Etapa 3 ignora espaços e não fornece tokens `INDENT`/`DEDENT`. Para interpretar blocos recuados, o parser precisará receber uma representação de indentação ou usar outra estratégia explicitamente documentada. Até que isso seja implementado e testado, suporte a blocos é requisito planejado, não funcionalidade entregue.

A gramática EBNF definitiva deverá ser registrada junto ao código quando a implementação for concluída. A versão do artigo é uma proposta, sujeita aos testes de correspondência com o comportamento implementado.

## 4. Arquitetura e decisão de tratamento de erros

O navegador envia o texto à API Flask. A API realiza validações de entrada e chama o scanner. Na proposta, quando houver erro léxico, a resposta deverá preservar os tokens válidos e exibir os erros, **sem passar tokens parciais ao parser**. Sem erros léxicos, a próxima etapa será o parser, encarregado de construir uma AST serializável e informar erros sintáticos. Análise semântica e tabela de símbolos permanecem para a Etapa 5.

Veja a figura [`fluxograma_etapa4.png`](fluxograma_etapa4.png), que diferencia componentes concluídos e previstos. Os campos da resposta antiga (`tokens`, `erros`, `mensagem`, `ok`) deverão ser preservados ao incluir a AST, para reduzir quebras de compatibilidade.

## 5. Critérios e plano de avaliação

Os critérios serão definidos antes da execução dos novos testes: (C1) reconhecimento léxico; (C2) aceitação e rejeição sintática; (C3) conformidade da AST com exemplos de referência; (C4) localização dos erros; (C5) clareza dos diagnósticos; (C6) legibilidade e consistência entre código, tokens e árvore; (C7) regressão da Etapa 3; (C8) execução com Docker Compose; (C9) documentação reprodutível e (C10) usabilidade percebida.

A avaliação deverá combinar testes unitários, testes da API, inspeção manual da interface, execução em ambiente limpo e questionário anônimo com estudantes que já cursaram ou cursam Compiladores. A participação de docentes pode ser considerada. Os participantes deverão experimentar pelo menos um caso válido e um inválido, com registro das tarefas e respostas em escala Likert de cinco pontos, além de perguntas abertas. **Esses procedimentos ainda são planejados; não há resultados de avaliação de usuários atribuídos ao LexLab nesta etapa.**

O plano inicial dos casos, com entradas e saídas esperadas, está em [`casos_de_teste_etapa4.md`](casos_de_teste_etapa4.md). Não presumir que casos planejados passaram: registrar resultado observado e status após a implementação e execução.

## 6. Execução do projeto atualmente publicado

```bash
docker compose up --build -d
python -m pytest tests -v
docker compose down
```

O navegador acessa `http://localhost:8080`. Os comandos acima usam a versão local efetivamente presente no repositório no momento do teste.

**Repositório:** https://github.com/rafaelapborges/analisador-educacional
