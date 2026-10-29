"""Testes de validação da entrada e integração do scanner com o serviço."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from service import process_source, MAX_CODE_LENGTH


def test_codigo_valido():
    dados, status = process_source({'codigo': 'idade = 18\nresultado = idade + 2'})
    assert status == 200 and dados['ok'] and dados['recebido']
    assert dados['linhas'] == 2 and len(dados['tokens']) == 8
    assert dados['erros'] == []


def test_entrada_vazia():
    dados, status = process_source({'codigo': ''})
    assert status == 400 and dados['codigo_erro'] == 'ENTRADA_VAZIA'


def test_apenas_espacos():
    dados, status = process_source({'codigo': ' \t\n   '})
    assert status == 400 and dados['codigo_erro'] == 'ENTRADA_VAZIA'


def test_campo_ausente():
    dados, status = process_source({})
    assert status == 400 and dados['codigo_erro'] == 'CAMPO_AUSENTE'


def test_corpo_nao_e_objeto():
    for payload in [None, [], 'texto', 42]:
        dados, status = process_source(payload)
        assert status == 400 and dados['codigo_erro'] == 'JSON_INVALIDO'


def test_tipo_invalido():
    dados, status = process_source({'codigo': 10})
    assert status == 400 and dados['codigo_erro'] == 'TIPO_INVALIDO'


def test_caracteres_especiais_em_comentarios_e_strings():
    texto = 'nome = "João"\n# símbolos: <>&$\nprint("✓")'
    dados, status = process_source({'codigo': texto})
    assert status == 200 and dados['caracteres'] == len(texto) and dados['linhas'] == 3
    assert any(t['lexema'] == '"✓"' for t in dados['tokens'])


def test_erro_sintatico_sem_erro_lexico_deve_passar():
    dados, status = process_source({'codigo': 'if ( : :'})
    assert status == 200 and dados['sucesso'] and dados['erros'] == []


def test_erro_lexico_retorna_422_e_tokens_parciais():
    dados, status = process_source({'codigo': 'numero = 3 @ 2'})
    assert status == 422 and not dados['ok'] and not dados['sucesso']
    assert dados['erros'][0]['lexema'] == '@' and len(dados['tokens']) == 4


def test_limite_de_tamanho():
    dados, status = process_source({'codigo': 'a' * (MAX_CODE_LENGTH + 1)})
    assert status == 413 and dados['codigo_erro'] == 'ENTRADA_LONGA'


def test_codigo_no_limite():
    dados, status = process_source({'codigo': 'a' * MAX_CODE_LENGTH})
    assert status == 200 and dados['caracteres'] == MAX_CODE_LENGTH


def test_comentario_somente_nao_falha():
    dados, status = process_source({'codigo': '# Apenas um comentário'})
    assert status == 200 and dados['tokens'] == [] and dados['erros'] == []
