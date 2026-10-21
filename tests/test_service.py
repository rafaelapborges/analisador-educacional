"""Testes da validação de entrada, independentes do framework web."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from service import process_source, MAX_CODE_LENGTH


def test_codigo_valido():
    dados,status=process_source({'codigo':'idade = 18\nresultado = idade + 2'})
    assert status==200 and dados['ok'] and dados['recebido']
    assert dados['linhas']==2


def test_entrada_vazia():
    dados,status=process_source({'codigo':''})
    assert status==400 and dados['codigo_erro']=='ENTRADA_VAZIA'


def test_apenas_espacos():
    dados,status=process_source({'codigo':' \t\n   '})
    assert status==400 and dados['codigo_erro']=='ENTRADA_VAZIA'


def test_campo_ausente():
    dados,status=process_source({})
    assert status==400 and dados['codigo_erro']=='CAMPO_AUSENTE'


def test_corpo_nao_e_objeto():
    for payload in [None, [], 'texto', 42]:
        dados,status=process_source(payload)
        assert status==400 and dados['codigo_erro']=='JSON_INVALIDO'


def test_tipo_invalido():
    dados,status=process_source({'codigo':10})
    assert status==400 and dados['codigo_erro']=='TIPO_INVALIDO'


def test_caracteres_especiais_preservados():
    text='nome = "João"\n# símbolos: <>&$\nprint("✓")'
    dados,status=process_source({'codigo':text})
    assert status==200 and dados['caracteres']==len(text) and dados['linhas']==3


def test_codigo_sintaticamente_invalido_nao_e_bloqueado():
    dados,status=process_source({'codigo':'if ( :$ :'} )
    assert status==200 and dados['ok']


def test_limite_de_tamanho():
    dados,status=process_source({'codigo':'a'*(MAX_CODE_LENGTH+1)})
    assert status==413 and dados['codigo_erro']=='ENTRADA_LONGA'


def test_codigo_no_limite():
    dados,status=process_source({'codigo':'a'*MAX_CODE_LENGTH})
    assert status==200 and dados['caracteres']==MAX_CODE_LENGTH
