# Analisador Educacional de Código Python — Etapa 2

Repositório original: https://github.com/rafaelapborges/analisador-educacional  
Branch-base consultada: `main` (commit `b798bff11d3f6fb2b0fb6139fb0ead4439032d2a`)

## Sobre o projeto

Este projeto tem como objetivo desenvolver um **software educacional** para auxiliar na aprendizagem das análises léxica, sintática e semântica de código Python. A segunda etapa disponibiliza a **entrada, seleção e validação inicial de código**, sem fazer análise léxica, sintática ou semântica nesta versão.

O subconjunto inicial, preservado da primeira etapa, considera **atribuição de variáveis, números inteiros, operações `+`, `-`, `*`, `/` e expressões aritméticas simples**. Esse recorte é o plano para etapas futuras; **a versão atual aceita o texto enviado, mas ainda não verifica se ele pertence à gramática**.

## Tecnologias

- Frontend: HTML, CSS e JavaScript, servido via Nginx;
- Backend: Python 3.12 e Flask 3.1.1; Gunicorn na imagem Docker;
- Ambiente: Docker Compose, com serviços `frontend` e `backend`;
- Testes: pytest (lógica e HTTP local) e Playwright (interações do navegador).

## Recursos da segunda etapa

1. Identificação do software e da linguagem (Python simplificado).
2. Área para escrever, colar e editar código-fonte.
3. Três exemplos selecionáveis e editáveis.
4. Botão para enviar o código ao backend, com resposta verificável.
5. Painel de resultado com confirmação de recebimento e quantidade de linhas/caracteres.
6. Mensagens para campo vazio, apenas espaços, JSON ausente ou inválido, tipo incorreto, limite de tamanho e falhas de rede.
7. Testes automatizados e registro dos resultados.
8. Compatibilidade com a rota da primeira etapa: `GET /api/hello` → `{"message":"Hello, World!"}`.

## Exemplos

- **Variáveis e atribuição:** `numero = 10` e `total = 5`.
- **Soma e subtração:** `soma = 10 + 5` e `resto = soma - 2`.
- **Multiplicação e divisão:** `dobro = 6 * 2` e `quociente = dobro / 3`.

Cada um é um **texto de entrada** para futura análise; neste estágio seu conteúdo não é interpretado nem executado.

## Como executar no Docker

Pré-requisitos: Docker Desktop (ou Docker Engine) e Docker Compose v2.

```bash
git clone https://github.com/rafaelapborges/analisador-educacional.git
cd analisador-educacional
docker compose up --build -d
docker compose ps
```

Acesse **http://localhost:8080**. Para encerrar: `docker compose down`.

> Ao baixar este ZIP de integração, abra o terminal na pasta extraída e execute diretamente `docker compose up --build -d`. Os comandos de `git clone` acima servem para o repositório depois de você enviar estas alterações para o GitHub.

O frontend é servido por Nginx e faz chamadas relativas a `/api/`, encaminhadas por proxy à aplicação Flask no serviço `backend`.

## Contrato da API

- `GET /api/hello`: retorno de compatibilidade da primeira etapa, HTTP 200.
- `GET /api/health`: `{"ok":true,"servico":"compiladores","status":"ativo"}`, HTTP 200.
- `POST /api/analisar` com `Content-Type: application/json`, exemplo:

```json
{"codigo":"numero = 10"}
```

Resposta de sucesso: `200` com `ok`, `recebido`, `mensagem`, `linhas`, `caracteres` e `proxima_etapa`. Falhas: `400` (campo ausente, texto vazio ou inválido), `415` (tipo de conteúdo incorreto), `413` (mais de 12.000 caracteres).

As validações são aplicadas no backend e as mensagens são exibidas com clareza na interface. **Nenhum código é executado e nenhum programa é compilado**.

## Testes automatizados

Com Python e as dependências de testes instaladas (`pytest`, `playwright` e navegador Chromium), execute:

```bash
python -m pytest tests -q
```

O conjunto cobre regras de entrada, endpoint HTTP local, fluxo da interface e regressão do antigo `/api/hello`. A suíte de navegador utiliza o servidor local de **pré-visualização** (`backend/preview_server.py`), que chama a mesma função de validação do Flask, mas **não substitui os testes reais de Nginx/Flask/Docker**.

Para verificar a imagem Docker no computador:

```bash
docker compose config
docker compose up --build -d
docker compose ps
docker compose exec backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/hello').read())"
docker compose exec backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/health').read())"
```

Veja `docs/registro_testes.md` e `docs/print_interface_etapa2.png` para o registro local. Os testes de Docker Compose **precisam ser realizados no seu computador**, pois esse ambiente de geração não possui Docker.

## Estrutura do projeto

```text
analisador-educacional/
├── backend/
│   ├── app.py
│   ├── service.py
│   ├── preview_server.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── nginx.conf
│   └── Dockerfile
├── tests/
├── docs/
├── docker-compose.yml
└── README.md
```

## Limitações e próxima etapa

- A versão atual **não executa** código Python.
- **Não realiza** tokenização, parsing, nem identifica erros léxicos, sintáticos ou semânticos.
- **Não armazena** arquivos enviados em banco de dados.
- O escopo da gramática didática será formalizado e implementado progressivamente.
- Docker e Flask em contêiner ainda precisam de verificação no computador da entrega.

## Como publicar as alterações

Após comparar os arquivos com a sua cópia do repositório e executar os testes:

```bash
git status
git add .
git commit -m "Etapa 2: interface de entrada Python, API e testes automatizados"
git push origin main
```

Para preservar seu histórico Git, **copie o conteúdo da pasta deste ZIP para dentro do repositório clonado**, em vez de enviar a pasta extraída como um repositório novo. A conexão GitHub desta sessão tem acesso somente de leitura ao seu repositório; nenhum commit foi enviado automaticamente.
