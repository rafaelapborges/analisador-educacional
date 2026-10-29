# Roteiro de demonstração — Etapa 3

1. Com Docker Desktop aberto, execute `docker compose up --build -d` dentro do repositório. Confirme que o backend está saudável com `docker compose ps`.
2. Acesse `http://localhost:8080`. Selecione **01 · Variáveis e atribuição**, clique em **Analisar código** e confira a tabela de tokens, linha/coluna e o destaque por categoria.
3. Use **Próximo →** e **← Anterior** para mostrar como a interface acompanha cada token.
4. Selecione **04 · Condição e comparação** para demonstrar uma palavra reservada, o operador `>=` e uma string.
5. Selecione **05 · Exemplo de erro léxico**. Clique em **Analisar código**: o caractere `@` deverá ser indicado em vermelho, com linha e coluna, sem travar a aplicação.
6. Apague o conteúdo e clique em **Analisar código** para verificar a validação de entrada vazia.
7. Execute `python -m pytest tests -v` e registre o resultado observado no Windows em `docs/registro_testes_etapa3.md`.
8. Tire um print da interface aberta em Docker com a tabela de tokens e outro com o erro léxico. Faça commit/push com o GitHub Desktop.

Para explicar ao professor: **token** é a categoria reconhecida, **lexema** é o texto exato encontrado no código. O scanner apenas agrupa e classifica caracteres: a verificação das regras da linguagem virá com o parser na Etapa 4.
