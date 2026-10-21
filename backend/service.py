"""Regras puras de entrada de código — sem executar ou analisar o programa."""
MAX_CODE_LENGTH = 12000


def process_source(payload):
    """Retorna (dados_json, status_http) para uma solicitação de processamento."""
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
    return {
        "ok": True,
        "recebido": True,
        "mensagem": "Código recebido com sucesso. Nesta etapa, somente a entrada foi validada.",
        "linhas": len(code.splitlines()),
        "caracteres": len(code),
        "proxima_etapa": "Análises léxica e sintática serão implementadas futuramente.",
    }, 200
