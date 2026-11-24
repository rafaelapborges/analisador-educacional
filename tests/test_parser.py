"""Casos de teste da etapa 4: integração real com scanner e parser."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from scanner import tokenize
from parser import parse
from service import process_source


def analyse(code):
    tokens, lexerrors, _ = tokenize(code)
    assert not lexerrors, lexerrors
    return parse(code, tokens)


def test_atribuicao_basica():
    ast, err = analyse('numero = 10\ntotal = numero + 2 * 3')
    assert err == []
    assert [x['tipo'] for x in ast['corpo']] == ['Atribuicao', 'Atribuicao']
    assert ast['corpo'][1]['valor']['operador'] == '+' 
    assert ast['corpo'][1]['valor']['direita']['operador'] == '*'


def test_parenteses_alteram_precedencia():
    ast, err = analyse('x = (1 + 2) * 3')
    assert not err
    assert ast['corpo'][0]['valor']['operador'] == '*'
    assert ast['corpo'][0]['valor']['esquerda']['operador'] == '+'


def test_condicional_com_else():
    source = 'if nota >= 7:\n    print("ok")\nelse:\n    pass'
    ast, err = analyse(source)
    assert not err
    assert ast['corpo'][0]['tipo'] == 'Se'
    assert ast['corpo'][0]['ramos'][0]['corpo'][0]['tipo'] == 'Expressao'
    assert ast['corpo'][0]['senao'][0]['tipo'] == 'Passar'


def test_while_aninhado():
    source = 'while x < 10:\n    if x == 3:\n        pass\n    x = x + 1'
    ast, err = analyse(source)
    assert not err
    assert ast['corpo'][0]['tipo'] == 'Enquanto'
    assert ast['corpo'][0]['corpo'][0]['tipo'] == 'Se'


def test_erro_ausencia_dois_pontos():
    _, err = analyse('if x > 2\n    pass')
    assert any("':'" in e['mensagem'] for e in err)


def test_erro_operador_repetido():
    _, err = analyse('x = 1 + * 2')
    assert err and err[0]['tipo'] == 'ERRO_SINTATICO'


def test_erro_bloco_nao_indendado():
    _, err = analyse('if x:\npass')
    assert err and 'bloco indentado' in err[0]['mensagem']


def test_erro_lexico_nao_executa_parser():
    res, status = process_source({'codigo': 'x = 1 @ 2'})
    assert status == 422
    assert res['ast'] is None
    assert res['sintaxe']['status'] == 'nao_executada'
    assert res['erros']


def test_retorno_compativel_etapa_3():
    res, status = process_source({'codigo': 'numero = 10'})
    assert status == 200
    assert len(res['tokens']) == 3
    assert res['erros'] == []
    assert res['ast']['corpo'][0]['tipo'] == 'Atribuicao'


def test_entrada_vazia_igual_antes():
    res, status = process_source({'codigo': '   '})
    assert status == 400
    assert res['codigo_erro'] == 'ENTRADA_VAZIA'


def test_codigo_grande():
    res, status = process_source({'codigo': 'x' * 12001})
    assert status == 413


def test_if_elif_else():
    src = 'if nota >= 7:\n    pass\nelif nota >= 5:\n    pass\nelse:\n    pass'
    ast, errors = analyse(src)
    assert not errors
    assert len(ast['corpo'][0]['ramos']) == 2
    assert len(ast['corpo'][0]['senao']) == 1

def test_not_tem_precedencia_inferior_a_comparacao():
    ast, errors = analyse('x = not y == 3')
    assert not errors
    u = ast['corpo'][0]['valor']
    assert u['tipo'] == 'Unario' and u['operador'] == 'not'
    assert u['operando']['tipo'] == 'Binario'

def test_erro_else_sem_if():
    ast, errors = analyse('else:\n    pass')
    assert any("sem um 'if'" in e['mensagem'] for e in errors)

def test_comentario_sem_tokens_ast_vazia():
    output, status = process_source({'codigo':'# comentário'})
    assert status == 200 and output['ast']['corpo'] == []

def test_erro_didatico_com_regra_esperado_sugestao():
    result, status = process_source({'codigo':'if nota >= 7\n    pass'})
    assert status == 422 and result['ast'] is None
    error = result['erros_sintaticos'][0]
    assert error['tipo'] == 'ERRO_SINTATICO'
    assert error['linha'] == 1 and error['coluna'] > 1
    assert ':' in error['esperado']
    assert 'condicional' in error['regra']
    assert 'Adicione' in error['sugestao']
    assert error['encontrado'] == 'fim da linha'


def test_erro_operadores_seguidos_com_esperado_e_encontrado():
    result, status=process_source({'codigo':'x = 1 + * 3'})
    assert status == 422 and result['ast'] is None
    error=result['erros_sintaticos'][0]
    assert error['encontrado'] == '*'
    assert error['esperado']
    assert 'expressao' in error['regra']


def test_ast_posicoes_permite_destacar_codigo():
    text='resultado = 10 + 5 * 2'
    res, status = process_source({'codigo':text})
    assert status == 200
    expression=res['ast']['corpo'][0]['valor']
    assert expression['tipo']=='Binario' and expression['operador']=='+'
    assert text[expression['inicio']:expression['fim']] == '10 + 5 * 2'
    multiplication=expression['direita']
    assert text[multiplication['inicio']:multiplication['fim']] == '5 * 2'


def test_operador_subtracao_associatividade_esquerda():
    ast, errors=analyse('x = 20 - 5 - 3')
    assert not errors
    expr=ast['corpo'][0]['valor']
    assert expr['operador']=='-'
    assert expr['esquerda']['tipo']=='Binario'
    assert expr['esquerda']['esquerda']['valor']=='20'


def test_erro_lexico_tem_prioridade_sobre_o_sintatico():
    res,status=process_source({'codigo':'if nota > 7 @\n    pass'})
    assert status==422 and res['erros']
    assert res['sintaxe']['status']=='nao_executada'
    assert res['erros_sintaticos']==[] and res['ast'] is None


def test_nao_apresenta_ast_parcial_se_existirem_erros():
    res, status=process_source({'codigo':'x = 1\ny = 3 + * 4'})
    assert status==422
    assert res['ast'] is None
    assert res['erros_sintaticos']


def test_else_sem_if_contem_regra_e_sugestao():
    res,status=process_source({'codigo':'else:\n    pass'})
    assert status==422
    err=res['erros_sintaticos'][0]
    assert err['regra'] and err['sugestao']


def test_blocos_com_indendacao_incorreta_sao_diagnosticados():
    res,status=process_source({'codigo':'if x:\n  pass'})
    assert status==422
    assert res['erros_sintaticos'][0]['regra']
