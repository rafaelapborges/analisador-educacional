# Registro de testes — Etapa 2 integrada ao repositório original

Repositório de origem: https://github.com/rafaelapborges/analisador-educacional  
Branch consultada: `main`, commit `b798bff11d3f6fb2b0fb6139fb0ead4439032d2a`.

## Testes executados neste ambiente

| Conjunto | Como verificar | Resultado |
|---|---|---|
| Validação de entrada (Python) | `python -m pytest tests/test_service.py -q` | 10 aprovados |
| Endpoint HTTP do servidor local e regressão `/api/hello` | `python -m pytest tests/test_e2e.py -q` | 1 teste aprovado |
| Interações do navegador, 3 exemplos, edição, envio e limpar | `python -m pytest tests/test_e2e.py -q` | 1 teste aprovado |
| Suíte completa | `python -m pytest tests -q` | **12 aprovados** |
| Sintaxe Python | `python -m compileall -q backend` | concluído sem erros |

A captura `docs/print_interface_etapa2.png` foi realizada com Chromium. O navegador recebeu a resposta do serviço HTTP local através da ponte do Playwright; o servidor de pré-visualização usa a mesma função `service.process_source` chamada pelo Flask. É uma **captura real da interface testada**, não uma imagem ilustrativa, mas não constitui evidência de execução via Docker.

## Verificações ainda necessárias no computador de entrega

- Construção e inicialização real com `docker compose up --build -d`.
- Confirmação das rotas `GET /api/hello`, `GET /api/health` e `POST /api/analisar` **através de Nginx → Flask**, acessando `http://localhost:8080`.
- Captura adicional do navegador rodando em Docker para apresentação final, se a professora exigir evidência da execução em contêineres.
- Confirmação de que as alterações estão no GitHub após commit/push.

Não se afirma que os testes do Flask em Docker ou do ambiente de implantação passaram: **não foram executados aqui** porque Docker e Flask não estão disponíveis no ambiente de geração.


## Validação da segunda etapa — 20/10/2026

A aplicação foi iniciada utilizando Docker Compose no ambiente Windows.

- Frontend: contêiner iniciado com sucesso.
- Backend: contêiner iniciado e saudável (Healthy).
- Interface acessada em http://localhost:8080.
- Três exemplos de código Python selecionados e enviados com sucesso.
- Validação de código vazio apresentada corretamente.
- Comunicação entre frontend e backend confirmada.

### Testes automatizados

Comando executado:

python -m pytest tests -v

Resultado: **12 testes aprovados, 0 falhas, em 17,87 segundos**.

Os testes abrangem validação de entrada, endpoints, comunicação,
interação com a interface e regressão.

A execução foi realizada no Windows com Python 3.13.7
e pytest 9.1.1.

## Validação da Etapa 3 — 29/10/2026

A aplicação foi executada localmente com Docker Compose.

- Backend e frontend iniciados corretamente.
- Scanner identificou 6 tokens no exemplo de variáveis.
- Tokens exibidos com tipo, lexema, linha e coluna.
- Caractere inválido "$" identificado na linha 2, coluna 20.
- Mensagens de erro apresentadas corretamente.
- Prints reais da interface e do erro léxico salvos.

### Testes automatizados

Comando executado:
python -m pytest tests -v

Resultado: Todos os testes aprovados na execução local.

### Situação
Análise léxica validada no ambiente local.s