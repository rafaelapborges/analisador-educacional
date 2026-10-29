# Registro de testes — Etapa 3 (scanner)

## Execução no ambiente de preparação dos arquivos

Data: 29/10/2026.

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Scanner + validação de entrada | `python -m pytest tests/test_scanner.py tests/test_service.py -q` | 74 aprovados, 0 falhas |
| Suíte completa (scanner, serviço, HTTP local, Chromium) | `python -m pytest tests -q` | 77 aprovados, 0 falhas |
| Verificação sintática Python | `python -m compileall -q backend` | Concluída sem erro |
| Sintaxe JavaScript | `node --check frontend/script.js` | Concluída sem erro |

O teste de interface emprega o **Chromium via Playwright**, com o serviço `backend/preview_server.py`, que usa a mesma função Python chamada pelo Flask. Foi verificada a exibição dos tokens e erros, seleção de exemplos, edição e limpeza. Essa validação **não equivale a executar o Docker Compose**.

## Verificações pendentes no Windows (preencher após a execução)

- [ ] `docker compose up --build -d`
- [ ] `docker compose ps` — backend `healthy`, frontend `running`
- [ ] `http://localhost:8080` — testar os cinco exemplos
- [ ] Testar entrada com `@`, conferir linha e coluna
- [ ] Testar campo vazio e edição livre
- [ ] `python -m pytest tests -v` — registrar resultado atual
- [ ] Captura de tela com tokens e com erro léxico via Docker
- [ ] GitHub Desktop — commit e push publicados

**Observações/falhas corrigidas durante a validação no Windows:** registrar aqui o que realmente ocorrer. Não marcar como realizado antes de executar.
