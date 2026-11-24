"""Validação de entrada, scanner e parser didáticos do LexLab (sem execução)."""
from scanner import tokenize
from parser import parse

MAX_CODE_LENGTH = 12000


def process_source(payload):
    if not isinstance(payload, dict):
        return {'ok': False, 'mensagem': 'Envie um objeto JSON válido contendo o campo codigo.', 'codigo_erro': 'JSON_INVALIDO'}, 400
    if 'codigo' not in payload:
        return {'ok': False, 'mensagem': 'O campo codigo é obrigatório.', 'codigo_erro': 'CAMPO_AUSENTE'}, 400
    code = payload['codigo']
    if not isinstance(code, str):
        return {'ok': False, 'mensagem': 'O código-fonte precisa ser um texto.', 'codigo_erro': 'TIPO_INVALIDO'}, 400
    if not code.strip():
        return {'ok': False, 'mensagem': 'Informe um código-fonte antes de solicitar a análise.', 'codigo_erro': 'ENTRADA_VAZIA'}, 400
    if len(code) > MAX_CODE_LENGTH:
        return {'ok': False, 'mensagem': f'O código ultrapassou o limite de {MAX_CODE_LENGTH} caracteres.', 'codigo_erro': 'ENTRADA_LONGA'}, 413

    tokens, erros, contagem = tokenize(code)
    ast, erros_sintaticos = (None, []) if erros else parse(code, tokens)
    sucesso = not erros and not erros_sintaticos
    if erros:
        mensagem = f'Análise léxica encontrou {len(erros)} erro(s). O parser não foi executado.'
    elif erros_sintaticos:
        mensagem = f'Análise sintática encontrou {len(erros_sintaticos)} erro(s). Confira as posições abaixo.'
    else:
        mensagem = 'Análises léxica e sintática concluídas: AST gerada.'
    return {
        'ok': sucesso,
        'sucesso': sucesso,
        'recebido': True,
        'mensagem': mensagem,
        'linhas': len(code.splitlines()),
        'caracteres': len(code),
        'tokens': tokens,
        'erros': erros,  # Etapa 3: manter somente diagnósticos léxicos
        'contagem': contagem,
        'ast': ast,
        'erros_sintaticos': erros_sintaticos,
        'sintaxe': {
            'status': 'nao_executada' if erros else ('com_erros' if erros_sintaticos else 'valida'),
            'valida': None if erros else not erros_sintaticos,
        },
        'proxima_etapa': 'A análise semântica será implementada na Etapa 5.',
    }, 200 if sucesso else 422
