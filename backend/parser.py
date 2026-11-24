"""Parser descendente recursivo (Pratt para expressões) do LexLab.

Entrada: tokens do scanner da Etapa 3 + código original para ler a indentação.
Saída: AST JSON e diagnósticos sintáticos contextualizados. Nunca executa código.
"""
from __future__ import annotations
from dataclasses import dataclass

MAX_DEPTH = 32
MAX_ERRORS = 30

REGRAS = {
    'atribuicao': 'atribuicao = IDENTIFICADOR "=" expressao',
    'condicional': 'condicional = "if" expressao ":" bloco ["else:" bloco]',
    'repeticao': 'repeticao = "while" expressao ":" bloco',
    'bloco': 'bloco = NOVA_LINHA INDENTACAO comandos',
    'expressao': 'expressao = operando { operador operando }',
    'agrupamento': 'fator = "(" expressao ")"',
    'senao': '"else" somente após um bloco de "if" na mesma indentação',
    'comando': 'comando = atribuicao | condicional | repeticao | "pass" | expressao',
}


class SyntaxProblem(Exception):
    """Uma falha gramatical, não uma exceção interna do servidor."""
    def __init__(self, message, token=None, *, line=1, column=1,
                 expected=(), found=None, rule='comando', suggestion=''):
        super().__init__(message)
        self.line = token['linha'] if token else line
        self.column = token['coluna'] if token else column
        self.expected = list(expected)
        self.found = token['lexema'] if token else (found if found is not None else 'fim da linha')
        self.rule = rule
        self.suggestion = suggestion

    def as_dict(self):
        return {
            'tipo': 'ERRO_SINTATICO',
            'linha': self.line,
            'coluna': self.column,
            'mensagem': str(self),
            'esperado': self.expected,
            'encontrado': self.found,
            'regra': REGRAS.get(self.rule, self.rule),
            'sugestao': self.suggestion,
        }


def _bounds(value):
    """Busca intervalos das subárvores para destacar nós no código-fonte."""
    if isinstance(value, list):
        items = [_bounds(v) for v in value]
    elif isinstance(value, dict):
        items = []
        if isinstance(value.get('inicio'), int) and isinstance(value.get('fim'), int):
            items.append((value['inicio'], value['fim']))
        else:
            items += [_bounds(v) for k, v in value.items() if k != 'tipo']
    else:
        return None
    spans = [x for x in items if x is not None]
    return (min(x[0] for x in spans), max(x[1] for x in spans)) if spans else None


def node(tipo, token=None, **attrs):
    result = {'tipo': tipo}
    if token is not None:
        result.update(linha=token['linha'], coluna=token['coluna'])
    result.update(attrs)
    spans = [_bounds(v) for v in attrs.values()]
    spans = [s for s in spans if s]
    if token and isinstance(token.get('inicio'), int):
        spans.append((token['inicio'], token['fim']))
    if spans:
        result['inicio'] = min(x[0] for x in spans)
        result['fim'] = max(x[1] for x in spans)
    return result


@dataclass
class SourceLine:
    line: int
    indent: int
    tokens: list


class ExpressionReader:
    PRECEDENCE = {'or': 1, 'and': 2, '==': 3, '!=': 3, '<': 3,
                  '<=': 3, '>': 3, '>=': 3, '+': 4, '-': 4,
                  '*': 5, '/': 5, '//': 5, '%': 5, '**': 7}

    def __init__(self, tokens, line):
        self.tokens, self.index, self.line = tokens, 0, line

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def pop(self):
        t = self.peek()
        if t is not None:
            self.index += 1
        return t

    def error(self, message, *, expected=(), rule='expressao', suggestion=''):
        token = self.peek()
        if token is None and self.tokens:
            last = self.tokens[-1]
            col = last['coluna'] + len(last['lexema'])
        else:
            col = 1
        raise SyntaxProblem(message, token, line=self.line, column=col,
                            expected=expected, rule=rule, suggestion=suggestion)

    def expect(self, lex):
        t = self.peek()
        if t is None or t['lexema'] != lex:
            self.error(f"Era esperado '{lex}', mas foi encontrado " +
                       (repr(t['lexema']) if t else 'o fim da linha') + '.',
                       expected=[lex], rule='agrupamento',
                       suggestion=f"Confira o fechamento dos parênteses com '{lex}'.")
        self.pop()

    def full(self):
        value = self.expr(0)
        if self.peek() is not None:
            t = self.peek()
            self.error(f"O símbolo {t['lexema']!r} não era esperado após esta expressão.",
                       expected=['operador', 'fim da instrução'],
                       suggestion='Separe comandos em linhas distintas e confira a gramática.')
        return value

    def expr(self, minimum, depth=0):
        if depth > MAX_DEPTH:
            self.error('A expressão ultrapassou o limite de aninhamento didático.',
                       suggestion='Reduza o número de parênteses ou operadores aninhados.')
        t = self.pop()
        if t is None:
            self.error('Expressão incompleta: faltou um valor após o operador.',
                       expected=['identificador', 'literal', '('],
                       suggestion='Adicione um número, identificador ou expressão entre parênteses.')
        lex, kind = t['lexema'], t['tipo']
        if lex in ('+', '-', 'not'):
            operand = self.expr(3 if lex == 'not' else 7, depth+1)
            left = node('Unario', t, operador=lex, operando=operand)
        elif lex == '(':
            left = self.expr(0, depth+1)
            self.expect(')')
        elif kind.startswith('LITERAL_') or lex in ('True','False','None'):
            left = node('Literal', t, valor=lex, categoria=kind)
        elif kind == 'IDENTIFICADOR':
            left = node('Identificador', t, nome=lex)
        else:
            raise SyntaxProblem(f"Era esperado um valor ou identificador, mas apareceu {lex!r}.", t,
                                expected=['identificador','literal','('], rule='expressao',
                                suggestion='Verifique se faltou um operando ou há operadores consecutivos.')
        # Chamadas simples: print(x), não executar o código.
        while self.peek() and self.peek()['lexema'] == '(':
            start = self.pop()
            args=[]
            if self.peek() and self.peek()['lexema'] != ')':
                while True:
                    args.append(self.expr(0,depth+1))
                    if not self.peek() or self.peek()['lexema'] != ',':
                        break
                    self.pop()
            self.expect(')')
            left = node('Chamada', start, funcao=left, argumentos=args)
        while self.peek():
            op = self.peek()
            prec = self.PRECEDENCE.get(op['lexema'])
            if prec is None or prec < minimum:
                break
            self.pop()
            right = self.expr(prec if op['lexema']=='**' else prec+1,depth+1)
            left = node('Binario', op, operador=op['lexema'], esquerda=left, direita=right)
        return left


class Parser:
    def __init__(self, source, tokens):
        grouped={}
        for t in tokens:
            grouped.setdefault(t['linha'],[]).append(t)
        self.lines=[]
        self.errors=[]
        for number, raw in enumerate(source.splitlines(),start=1):
            if number not in grouped:
                continue
            prefix = raw[:len(raw)-len(raw.lstrip(' \t'))]
            if '\t' in prefix:
                self._report(SyntaxProblem('Esta gramática usa quatro espaços por nível de indentação; tabulação não é aceita.',
                                           line=number,column=1,rule='bloco', expected=['4 espaços'],found='tabulação',
                                           suggestion='Troque a tabulação por quatro espaços.'))
            elif len(prefix)%4:
                self._report(SyntaxProblem('A indentação deve ter múltiplos de quatro espaços.',
                                           line=number,column=1,rule='bloco',expected=['4 espaços por nível'],
                                           found=f'{len(prefix)} espaços',suggestion='Ajuste o recuo do bloco.'))
            self.lines.append(SourceLine(number, len(prefix.replace('\t','    ')),grouped[number]))
        self.index=0

    def _report(self, exc):
        if len(self.errors)<MAX_ERRORS:
            self.errors.append(exc.as_dict())

    def _body(self, indent,depth=0):
        if depth>MAX_DEPTH:
            raise SyntaxProblem('Quantidade de blocos aninhados acima do limite.',rule='bloco')
        items=[]
        while self.index<len(self.lines):
            line=self.lines[self.index]
            if line.indent<indent:
                break
            if line.indent>indent:
                self._report(SyntaxProblem('Indentação inesperada: nenhum bloco foi aberto neste nível.',
                                           line=line.line,column=1,rule='bloco',expected=[f'{indent} espaços'],
                                           found=f'{line.indent} espaços',suggestion='Confira os dois-pontos do comando anterior.'))
                self.index+=1
                continue
            self.index+=1
            try:
                items.append(self._statement(line,depth))
            except SyntaxProblem as exc:
                self._report(exc)
        return items

    def _nested(self,parent,depth):
        if self.index>=len(self.lines) or self.lines[self.index].indent<=parent.indent:
            last=parent.tokens[-1]
            raise SyntaxProblem('Era esperado um bloco indentado após os dois-pontos.',
                                line=last['linha'],column=last['coluna']+len(last['lexema']),
                                expected=['bloco com 4 espaços'], rule='bloco',
                                suggestion='Na próxima linha, acrescente quatro espaços antes do comando.')
        expected=parent.indent+4
        if self.lines[self.index].indent!=expected:
            actual=self.lines[self.index]
            raise SyntaxProblem('O bloco deve avançar exatamente quatro espaços.',
                                line=actual.line,column=1,rule='bloco',expected=[f'{expected} espaços'],
                                found=f'{actual.indent} espaços',suggestion='Ajuste o recuo da linha indicada.')
        return self._body(expected,depth+1)

    def _condition(self,line,rule='condicional'):
        tokens=line.tokens
        if tokens[-1]['lexema']!=':':
            last=tokens[-1]
            raise SyntaxProblem("Faltou ':' ao final da condição.",line=line.line,
                                column=last['coluna']+len(last['lexema']),
                                expected=[':'], found='fim da linha',rule=rule,
                                suggestion="Adicione ':' ao final da linha antes do bloco indentado.")
        return ExpressionReader(tokens[1:-1],line.line).full()

    def _statement(self,line,depth):
        tokens=line.tokens
        head=tokens[0]['lexema']
        if head in ('elif','else'):
            raise SyntaxProblem(f"'{head}' sem um 'if' correspondente.", tokens[0],
                                expected=['if anterior'], rule='senao',
                                suggestion="Coloque o 'else' ou 'elif' após um bloco 'if' no mesmo recuo.")
        if head in ('if','while'):
            rule = 'condicional' if head=='if' else 'repeticao'
            condition=self._condition(line,rule)
            body=self._nested(line,depth)
            if head=='while':
                return node('Enquanto',tokens[0],condicao=condition,corpo=body)
            branches=[{'condicao':condition,'corpo':body}]
            alternative=[]
            seen_else=False
            while self.index<len(self.lines):
                candidate=self.lines[self.index]
                if candidate.indent!=line.indent or candidate.tokens[0]['lexema'] not in ('elif','else'):
                    break
                self.index+=1
                if candidate.tokens[0]['lexema']=='elif':
                    if seen_else:
                        raise SyntaxProblem("'elif' não pode aparecer depois de 'else'.",candidate.tokens[0],rule='condicional')
                    branches.append({'condicao':self._condition(candidate),'corpo':self._nested(candidate,depth)})
                else:
                    if len(candidate.tokens)!=2 or candidate.tokens[1]['lexema']!=':':
                        raise SyntaxProblem("Use 'else:' sem condição ou outros símbolos.",candidate.tokens[0],
                                            expected=['else:'],rule='senao',suggestion="Use somente 'else:' na linha.")
                    seen_else=True
                    alternative=self._nested(candidate,depth)
                    break
            return node('Se',tokens[0],ramos=branches,senao=alternative)
        if head=='pass':
            if len(tokens)!=1:
                raise SyntaxProblem("'pass' deve aparecer sozinho na linha.",tokens[1],
                                    expected=['fim da instrução'],rule='comando')
            return node('Passar',tokens[0])
        if len(tokens)>1 and tokens[1]['lexema']=='=':
            if tokens[0]['tipo']!='IDENTIFICADOR':
                raise SyntaxProblem('O lado esquerdo da atribuição precisa ser um identificador.',tokens[0],
                                    expected=['identificador'],rule='atribuicao')
            expr=ExpressionReader(tokens[2:],line.line).full()
            return node('Atribuicao',tokens[0],alvo=node('Identificador',tokens[0],nome=head),valor=expr)
        expr=ExpressionReader(tokens,line.line).full()
        return node('Expressao',tokens[0],valor=expr)

    def run(self):
        try:
            ast=node('Programa',corpo=self._body(0))
        except SyntaxProblem as exc:
            self._report(exc)
            ast=None
        # Nunca apresente uma AST incompleta como representação válida.
        return (None if self.errors else ast),self.errors


def parse(source,tokens):
    """Retorna (AST estruturada | None, lista de erros sintáticos)."""
    return Parser(source,tokens).run()
