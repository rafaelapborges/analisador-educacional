"""Validação da entrada e análise léxica do LexLab (sem execução de código)."""
from scanner import tokenize

MAX_CODE_LENGTH = 12000


def process_source(payload):
    """Retorna (dados_json, status_http); 422 indica erros léxicos localizados."""
    if not isinstance(payload, dict):
        return {"ok": False, "mensagem": "Envie um objeto JSON válido contendo o campo codigo.", "codigo_erro": "JSON_INVALIDO"}, 400
    if "codigo" not in payload:
        return {"ok": False, "mensagem": "O campo codigo é obrigatório.", "codigo_erro": "CAMPO_AUSENTE"}, 400
    code = payload["codigo"]
    if not isinstance(code, str):
        return {"ok": False, "mensagem": "O código-fonte precisa ser um texto.", "codigo_erro": "TIPO_INVALIDO"}, 400
    if not code.strip():
        return {"ok": False, "mensagem": "Informe um código-fonte antes de solicitar a análise.", "codigo_erro": "ENTRADA_VAZIA"}, 400
    if len(code) > MAX_CODE_LENGTH:
        return {"ok": False, "mensagem": f"O código ultrapassou o limite de {MAX_CODE_LENGTH} caracteres.", "codigo_erro": "ENTRADA_LONGA"}, 413

    tokens, erros, contagem = tokenize(code)
    sucesso = not erros
    return {
        "ok": sucesso,
        "sucesso": sucesso,
        "recebido": True,
        "mensagem": ("Análise léxica concluída: tokens reconhecidos." if sucesso else
                     f"Análise léxica encontrou {len(erros)} erro(s). Confira as posições abaixo."),
        "linhas": len(code.splitlines()),
        "caracteres": len(code),
        "tokens": tokens,
        "erros": erros,
        "contagem": contagem,
        "proxima_etapa": "A análise sintática será implementada na Etapa 4.",
    }, 200 if sucesso else 422
