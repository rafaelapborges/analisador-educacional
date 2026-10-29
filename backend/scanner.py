"""Scanner didático para um subconjunto inspirado em Python.

A análise é exclusivamente léxica: não executa nem valida a gramática do código.
Cada token informa lexema, tipo, linha, coluna e índices de caracteres para
visualização na interface. Erros são acumulados sem interromper a análise.
"""

from collections import Counter

RESERVADAS = frozenset({'if', 'elif', 'else', 'while', 'and', 'or', 'not', 'True', 'False', 'None', 'pass'})
OPERADORES = ('==', '!=', '<=', '>=', '**', '//', '+', '-', '*', '/', '%', '=', '<', '>')
DELIMITADORES = frozenset('()[]{}:,')
ESCAPES_SUPORTADOS = frozenset('\\\"\'nrt0')


def _letra(ch):
    return ('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ch == '_'


def _digito(ch):
    return '0' <= ch <= '9'


def tokenize(source):
    """Analisa a entrada e retorna (tokens, erros, contagem_por_tipo)."""
    if not isinstance(source, str):
        raise TypeError('O scanner recebe uma string.')

    tokens = []
    erros = []
    i, linha, coluna = 0, 1, 1
    n = len(source)

    def avancar(fim):
        nonlocal i, linha, coluna
        while i < fim:
            if source[i] == '\r':
                # CRLF conta como uma única quebra de linha.
                if i + 1 < fim and source[i + 1] == '\n':
                    i += 1
                linha += 1
                coluna = 1
            elif source[i] == '\n':
                linha += 1
                coluna = 1
            else:
                coluna += 1
            i += 1

    def token(tipo, inicio, fim, lin, col):
        tokens.append({'tipo': tipo, 'lexema': source[inicio:fim], 'linha': lin,
                       'coluna': col, 'inicio': inicio, 'fim': fim})

    def erro(inicio, fim, lin, col, mensagem):
        erros.append({'tipo': 'ERRO_LEXICO', 'lexema': source[inicio:fim],
                      'linha': lin, 'coluna': col, 'mensagem': mensagem,
                      'inicio': inicio, 'fim': fim})

    while i < n:
        ch = source[i]
        inicio, lin, col = i, linha, coluna
        if ch.isspace():
            # Não geramos INDENT/DEDENT: blocos pertencem à etapa sintática.
            if ch == '\r' and i + 1 < n and source[i + 1] == '\n':
                avancar(i + 2)
            else:
                avancar(i + 1)
            continue

        if ch == '#':
            j = i + 1
            while j < n and source[j] not in '\r\n':
                j += 1
            avancar(j)
            continue

        if _letra(ch):
            j = i + 1
            while j < n and (_letra(source[j]) or _digito(source[j])):
                j += 1
            categoria = 'PALAVRA_RESERVADA' if source[i:j] in RESERVADAS else 'IDENTIFICADOR'
            token(categoria, i, j, lin, col)
            avancar(j)
            continue

        if _digito(ch):
            j = i
            while j < n and _digito(source[j]):
                j += 1
            tipo = 'LITERAL_INTEIRO'
            malformado = False
            if j < n and source[j] == '.':
                j += 1
                if j >= n or not _digito(source[j]):
                    malformado = True
                else:
                    while j < n and _digito(source[j]):
                        j += 1
                    tipo = 'LITERAL_REAL'
            if j < n and (_letra(source[j]) or source[j] == '.'):
                malformado = True
            if malformado:
                while j < n and (_letra(source[j]) or _digito(source[j]) or source[j] == '.'):
                    j += 1
                erro(i, j, lin, col, 'Literal numérico inválido: ' + repr(source[i:j]) + '. Use, por exemplo, 12 ou 12.5.')
            else:
                token(tipo, i, j, lin, col)
            avancar(j)
            continue

        if ch in ('\"', "'"):
            aspas = ch
            j = i + 1
            problema = None
            while j < n and source[j] not in '\r\n':
                if source[j] == '\\':
                    if j + 1 >= n or source[j + 1] in '\r\n':
                        problema = 'Barra invertida sem caractere de escape.'
                        j += 1
                        break
                    if source[j + 1] not in ESCAPES_SUPORTADOS and problema is None:
                        problema = 'Sequência de escape não suportada: ' + repr(source[j:j + 2]) + '.'
                    j += 2
                    continue
                if source[j] == aspas:
                    j += 1
                    if problema:
                        erro(i, j, lin, col, problema)
                    else:
                        token('LITERAL_STRING', i, j, lin, col)
                    break
                j += 1
            else:
                # EOF ou fim de linha sem aspas de fechamento.
                erro(i, j, lin, col, problema or 'String não terminada: feche as aspas na mesma linha.')
            avancar(j)
            continue

        composto = next((op for op in OPERADORES if len(op) > 1 and source.startswith(op, i)), None)
        if composto:
            token('OPERADOR', i, i + len(composto), lin, col)
            avancar(i + len(composto))
        elif ch in OPERADORES:
            token('OPERADOR', i, i + 1, lin, col)
            avancar(i + 1)
        elif ch in DELIMITADORES:
            token('DELIMITADOR', i, i + 1, lin, col)
            avancar(i + 1)
        else:
            erro(i, i + 1, lin, col, f"Caractere não reconhecido: {ch!r}. Verifique o subconjunto suportado.")
            avancar(i + 1)

    return tokens, erros, dict(Counter(t['tipo'] for t in tokens))
