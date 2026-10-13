
# Analisador Educacional de Código Python

## Descrição
Este projeto tem como objetivo desenvolver um software
educacional para auxiliar no aprendizado de análise
léxica, sintática e semântica de códigos Python.

## Linguagem escolhida
A linguagem escolhida foi Python, por possuir uma
sintaxe simples e ser amplamente utilizada no ensino
de programação.

## Subconjunto inicial
O software abordará inicialmente:

- Declaração e atribuição de variáveis
- Números inteiros
- Operadores aritméticos (+, -, *, /)
- Expressões aritméticas simples

## Tecnologias
- Python
- Flask
- HTML, CSS e JavaScript
- Docker e Docker Compose

## Etapa atual
Criação da estrutura inicial do projeto,
configuração do ambiente Docker e implementação
de uma página web com a mensagem "Hello, World!".


## Pré-requisitos

Para executar o projeto, é necessário ter:

- Git instalado
- Docker Desktop instalado e em execução
- Docker Compose V2

Para verificar as versões instaladas:

```bash
git --version
docker --version
docker compose version
```

## Como executar o projeto

1. Abra o terminal e clone o repositório:

```bash
git clone https://github.com/rafaelapborges/analisador-educacional.git
```

2. Entre na pasta do projeto:

```bash
cd analisador-educacional
```

3. Inicie os contêineres:

```bash
docker compose up --build -d
```

4. Acesse a aplicação no navegador:

http://localhost:8080

A página deverá exibir a mensagem "Hello, World!"
e informar que o backend está conectado.

## Como verificar os contêineres

```bash
docker compose ps
```

## Como encerrar a aplicação

```bash
docker compose down
```

## Validação

O projeto foi executado localmente com Docker Compose.

Resultados observados:

- Imagem do frontend construída com sucesso.
- Imagem do backend construída com sucesso.
- Contêineres iniciados.
- Aplicação acessível em http://localhost:8080.
- Mensagem "Hello, World!" exibida.
- Comunicação entre frontend e backend confirmada.

A validação de uma instalação limpa será realizada
em uma nova pasta, seguindo estas instruções.

