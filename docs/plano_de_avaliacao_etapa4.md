# LexLab — Plano de avaliação pré-definido (Etapa 4)

## Objetivo

Verificar, separadamente, correção funcional do scanner/parser/AST e clareza pedagógica da visualização. Evidências de funcionamento não autorizam afirmar ganho de aprendizagem.

## Indicadores verificáveis

| Critério | Medida | Procedimento |
|---|---|---|
| Correção léxica | Tokens e posições corretos / total esperado | saída do scanner e testes legados |
| Correção sintática | Programas válidos reconhecidos / total de válidos | CT-01 a CT-08 |
| Detecção de erros | Entradas inválidas com diagnóstico correto / total inválido | CT-09 a CT-14 e CT-22 |
| Correção AST | Nós e relações conforme AST-referência / casos testados | comparação estrutural automatizada |
| Robustez | Tratamento esperado em entradas vazias/longas | CT-15, CT-16 |
| Recuperação | Quantidade e localização dos diagnósticos | registros manuais de entradas inválidas |
| Regressão | Testes antigos aprovados / executados | `python -m pytest tests -v` |
| Reprodutibilidade | Docker `backend healthy`, `frontend started` | `docker compose up --build -d` e `docker compose ps` |
| Legibilidade | Compreensão dos nomes, estrutura e contraste | inspeção por pares / questionário |
| Usabilidade | Escala Likert 1–5, tarefas concluídas, tempo e SUS se aplicado integralmente | sessões observadas |

## Testes técnicos

Unidade: `python -m pytest tests -v` no diretório raiz do repositório. Endpoints: respostas 200, 400, 413, 415 e 422; compatibilidade da Etapa 3. Regressão: confirmação de que destaque de tokens, erros léxicos e navegação continuam funcionando. E2E de interface com Playwright/Chromium quando disponível. Execução reproduzível por Docker Compose: `docker compose up --build -d`; encerramento `docker compose down`.

## Testes manuais

1. Inserir código → executar → verificar tokens → AST hierárquica → expandir/recolher nós.
2. Inserir erro lexical → conferir tipo e posição → verificar que AST não é gerada.
3. Inserir erro sintático → conferir retorno 422 e mensagem separada dos erros léxicos.
4. Repetir testes com exemplos de atribuição, precedência, `if` e `while`.
5. Verificar legibilidade em desktop e largura aproximada de celular.

O registro dos resultados será feito com data, saída esperada/observada, status, eventual correção e captura da tela. Nenhuma avaliação com estudantes foi executada nesta proposta.

## Avaliação por pares planejada

**Público:** estudantes de Computação e IA que já cursaram ou estão cursando Compiladores; convite opcional a professor da disciplina. **Amostra:** por conveniência; registrar número, experiência prévia e critérios de recrutamento. **Instrumento:** formulário voluntário e anônimo com escala Likert 1 (discordo totalmente) a 5 (concordo totalmente), mais duas perguntas abertas. Não coletar CPF, telefone ou e-mail.

**Itens da escala** (todos respondidos após executar tarefas com exemplos válidos e inválidos):

- A interface permite localizar as principais ações sem instruções adicionais.
- Consegui inserir e analisar um programa de exemplo.
- Compreendi a diferença entre token e estrutura sintática.
- O destaque dos tokens facilitou associar partes do código às categorias léxicas.
- A árvore AST foi legível e ajudou a identificar a estrutura do programa.
- A organização hierárquica e os controles de expandir/recolher facilitaram explorar a AST.
- O vínculo entre linhas/colunas e os resultados ajudou a localizar os elementos do código.
- As mensagens de erro léxico foram fáceis de entender.
- As mensagens de erro sintático foram fáceis de entender.
- A distinção entre erros léxicos e sintáticos ficou clara.
- A sequência editor → tokens → AST contribuiu para compreender a passagem entre as etapas de análise.
- A integração dessas visualizações em uma mesma interface foi útil para a atividade proposta. (**diferencial pretendido**)
- Os exemplos curtos em Python simplificado foram adequados ao nível introdutório. (**diferencial pretendido**)
- As limitações do subconjunto de linguagem estavam claras.
- Usaria a ferramenta como material complementar em Compiladores.

**Perguntas abertas:** Qual foi a principal dificuldade de uso? Que funcionalidade ou explicação deveria ser melhorada?

## Procedimento e análise

Termo de apresentação breve, consentimento informado, roteiro padronizado com 3 tarefas, observação de conclusão e erros, formulário anônimo. Relatar distribuição de respostas por item (n, mediana, intervalo), percentual de tarefas concluídas e sugestões recorrentes sem identificar participantes. Se houver pré/pós-teste, definir rubrica antes da execução. Comparações de aprendizagem só serão realizadas se o desenho metodológico permitir, evitando inferência causal automática. Para referências do modelo de avaliação, consultar Costagliola et al. (2022), que empregam tarefas, tempos, taxa de acertos e SUS; e Del Vado Vírseda (2023), que compara resultados acadêmicos entre grupos em diferentes períodos. Nenhum desses procedimentos foi realizado no LexLab até o momento.

## Situação

Etapa 3: testes locais e prints registrados na documentação. Etapa 4: parser e AST **preparados neste pacote para instalação e validação local**, não confirmados como publicados ou executados no computador do usuário. Etapa 5: análise semântica e símbolos **futuros**.
