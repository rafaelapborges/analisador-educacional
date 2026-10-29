"""Teste das categorias, localizações, erros e casos de borda do scanner."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from scanner import tokenize, RESERVADAS, OPERADORES, DELIMITADORES


def tipos(codigo):
    return [(t['tipo'], t['lexema']) for t in tokenize(codigo)[0]]


@pytest.mark.parametrize('palavra', sorted(RESERVADAS))
def test_palavras_reservadas(palavra):
    assert tipos(palavra) == [('PALAVRA_RESERVADA', palavra)]


@pytest.mark.parametrize('nome', ['a', '_x1', 'total_12', 'TOTAL'])
def test_identificadores_validos(nome):
    assert tipos(nome) == [('IDENTIFICADOR', nome)]


@pytest.mark.parametrize('valor,categoria', [
    ('0', 'LITERAL_INTEIRO'), ('42', 'LITERAL_INTEIRO'),
    ('12.5', 'LITERAL_REAL'), ('0.001', 'LITERAL_REAL'),
    ("'texto'", 'LITERAL_STRING'), ('"João"', 'LITERAL_STRING'),
    ('"linha\\ntexto"', 'LITERAL_STRING'), ("'it\\'s'", 'LITERAL_STRING'),
])
def test_literais(valor, categoria):
    assert tipos(valor) == [(categoria, valor)]


@pytest.mark.parametrize('operador', OPERADORES)
def test_operadores(operador):
    assert tipos(f'x {operador} 1')[1] == ('OPERADOR', operador)


@pytest.mark.parametrize('delimitador', sorted(DELIMITADORES))
def test_delimitadores(delimitador):
    assert tipos(delimitador) == [('DELIMITADOR', delimitador)]


def test_operadores_compostos_priorizados():
    assert [t[1] for t in tipos('a == b != c <= d >= e ** 2 // 2')] == [
        'a', '==', 'b', '!=', 'c', '<=', 'd', '>=', 'e', '**', '2', '//', '2'
    ]


def test_comentarios_e_espacos_ignorados():
    tokens, erros, _ = tokenize('   # início\nvalor = 2  # comentário\n\t')
    assert [t['lexema'] for t in tokens] == ['valor', '=', '2']
    assert erros == []


def test_posicao_com_crlf_e_tabs():
    tokens, erros, _ = tokenize('a = 1\r\n\tb = 2')
    assert [(t['linha'], t['coluna']) for t in tokens] == [
        (1, 1), (1, 3), (1, 5), (2, 2), (2, 4), (2, 6)
    ]
    assert erros == []


def test_invalido_nao_para_os_outros_tokens():
    tokens, erros, _ = tokenize('a = 1\n@ & $\nb = 2')
    assert [e['lexema'] for e in erros] == ['@', '&', '$']
    assert [e['linha'] for e in erros] == [2, 2, 2]
    assert [t['lexema'] for t in tokens][-3:] == ['b', '=', '2']


@pytest.mark.parametrize('texto', ['12abc', '1.2.3', '12.', '5_x'])
def test_numero_malformado(texto):
    tokens, erros, _ = tokenize(texto)
    assert not tokens and len(erros) == 1 and erros[0]['lexema'] == texto


@pytest.mark.parametrize('texto', ["'sem fim", '"sem fim\nmais = 3', '"a\\z"'])
def test_strings_malformadas(texto):
    _, erros, _ = tokenize(texto)
    assert len(erros) == 1 and erros[0]['linha'] == 1


def test_string_nao_fechada_nao_impede_linhas_seguintes():
    tokens, erros, _ = tokenize('nome = "aberto\nresultado = 4')
    assert len(erros) == 1 and erros[0]['coluna'] == 8
    assert [t['lexema'] for t in tokens][-3:] == ['resultado', '=', '4']


def test_nada_e_comentario_so():
    assert tokenize('')[0:2] == ([], [])
    assert tokenize(' \t\n# comentário')[0:2] == ([], [])


def test_token_sem_quebra_de_linha():
    tokens, erros, _ = tokenize('final')
    assert tokens[0]['lexema'] == 'final' and tokens[0]['coluna'] == 1 and not erros


def test_contagem_por_categoria():
    tokens, erros, contagem = tokenize('if a >= 3: print("ok")')
    assert not erros
    assert contagem['PALAVRA_RESERVADA'] == 1
    assert contagem['IDENTIFICADOR'] == 2
    assert contagem['LITERAL_INTEIRO'] == 1
    assert contagem['LITERAL_STRING'] == 1
    assert len(tokens) == sum(contagem.values())


def test_posicao_unicode_apos_string():
    tokens, erros, _ = tokenize('x="😀";y=2')
    assert len(erros) == 1 and erros[0]['lexema'] == ';'
    assert tokens[-3]['lexema'] == 'y' and tokens[-3]['coluna'] == 7


def test_scanner_rejeita_entrada_nao_textual():
    with pytest.raises(TypeError):
        tokenize(None)
