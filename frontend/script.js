'use strict';
const EXEMPLOS = Object.freeze({
  variavel: '# Exemplo 01 · Variáveis e atribuição\nnumero = 10\ntotal = 5',
  aritmetica: '# Exemplo 02 · Soma e subtração\nsoma = 10 + 5\nresto = soma - 2',
  operadores: '# Exemplo 03 · Multiplicação e divisão\ndobro = 6 * 2\nquociente = dobro / 3',
  condicional: '# Exemplo 04 · Condição (somente scanner)\nnota = 8.5\nif nota >= 7:\n    print("Aprovado")',
  erro: '# Exemplo 05 · Encontre o erro\nnumero = 12\ntotal = numero @ 2'
});
const $ = id => document.getElementById(id);
const codigo = $('codigo');
const exemplo = $('exemplo');
const analisar = $('analisar');
const limpar = $('limpar');
const resultBody = $('result-body');
const resultStatus = $('result-status');
const footerStatus = $('footer-status');
const lineNumbers = $('line-numbers');
const section = $('lexical-section');
const tokenTbody = $('tokens-tbody');
const sourceHighlight = $('source-highlight');
const explanation = $('token-explanation');
const stepLabel = $('token-step');
const tokenPrev = $('token-prev');
const tokenNext = $('token-next');
let currentRequest = 0;
let currentTokens = [];
let selectedToken = -1;

const EXPLICACOES = {
  PALAVRA_RESERVADA: 'Palavra que tem função especial no subconjunto da linguagem.',
  IDENTIFICADOR: 'Nome usado para representar uma variável ou outra referência.',
  LITERAL_INTEIRO: 'Número inteiro escrito diretamente no código.',
  LITERAL_REAL: 'Número decimal escrito diretamente no código.',
  LITERAL_STRING: 'Texto delimitado por aspas simples ou duplas.',
  OPERADOR: 'Símbolo utilizado em atribuições, cálculos ou comparações.',
  DELIMITADOR: 'Símbolo que separa ou agrupa partes do código.'
};

function lineCount() { return Math.max(1, codigo.value.split('\n').length); }
function updateLines() { lineNumbers.textContent = Array.from({length: lineCount()}, (_, i) => i + 1).join('\n'); }
function setStatus(label, kind) { resultStatus.textContent = label; resultStatus.className = 'result-badge ' + kind; }
function safeText(tag, className, value) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = value;
  return element;
}
function resetResult() {
  section.hidden = true;
  currentTokens = [];
  selectedToken = -1;
  resultBody.className = 'result-body';
  resultBody.replaceChildren(safeText('div', 'empty-icon', '↗'),
    safeText('h3', '', 'Pronto para começar'),
    safeText('p', '', 'Os tokens e os erros aparecerão aqui depois da análise.'));
  setStatus('AGUARDANDO', 'neutral');
  footerStatus.textContent = 'Aguardando entrada';
}
function renderValidationError(message) {
  section.hidden = true;
  resultBody.className = 'result-body error';
  resultBody.replaceChildren(safeText('div', 'result-mark', '!'),
    safeText('h3', '', 'Verifique a entrada'), safeText('p', '', message));
  setStatus('ATENÇÃO', 'error');
  footerStatus.textContent = 'Verifique o código e tente novamente';
}
function renderSummary(data) {
  const errors = Array.isArray(data.erros) ? data.erros : [];
  const tokens = Array.isArray(data.tokens) ? data.tokens : [];
  const failed = errors.length > 0;
  resultBody.className = 'result-body ' + (failed ? 'error' : 'success');
  resultBody.replaceChildren(safeText('div', 'result-mark', failed ? '!' : '✓'),
    safeText('h3', '', failed ? 'Análise concluída com avisos' : 'Tokens identificados'),
    safeText('p', '', data.mensagem));
  const grid = safeText('div', 'stat-grid', '');
  for (const [value, label] of [[tokens.length, 'Tokens'], [errors.length, 'Erros léxicos']]) {
    const item = safeText('div', 'stat', '');
    item.append(safeText('strong', '', String(value)), safeText('span', '', label));
    grid.append(item);
  }
  resultBody.append(grid, safeText('p', 'scope-message',
    'O scanner reconhece lexemas, mas não verifica se o programa está sintaticamente correto.'));
  setStatus(failed ? 'COM ERROS' : 'CONCLUÍDO', failed ? 'error' : 'success');
  footerStatus.textContent = 'Análise léxica realizada no backend';
}

function categoryClass(kind) {
  if (kind === 'PALAVRA_RESERVADA') return 'cat-reservada';
  if (kind === 'IDENTIFICADOR') return 'cat-identificador';
  if (kind.startsWith('LITERAL_')) return 'cat-literal';
  if (kind === 'OPERADOR') return 'cat-operador';
  return 'cat-delimitador';
}
function selectToken(index) {
  if (!currentTokens.length) {
    selectedToken = -1;
    explanation.textContent = 'Nenhum token reconhecido. Confira os erros ou insira outro código.';
  } else {
    selectedToken = Math.min(currentTokens.length - 1, Math.max(0, index));
    const t = currentTokens[selectedToken];
    explanation.textContent = `Passo ${selectedToken + 1}: “${t.lexema}” é ${t.tipo.toLowerCase().replaceAll('_', ' ')} (linha ${t.linha}, coluna ${t.coluna}). ${EXPLICACOES[t.tipo] || ''}`;
  }
  stepLabel.textContent = `${selectedToken < 0 ? 0 : selectedToken + 1} de ${currentTokens.length}`;
  tokenPrev.disabled = selectedToken <= 0;
  tokenNext.disabled = selectedToken >= currentTokens.length - 1;
  for (const element of section.querySelectorAll('[data-token-index]')) {
    element.classList.toggle('selected-token', Number(element.dataset.tokenIndex) === selectedToken);
  }
}
function renderAnalysis(data, code) {
  const tokens = Array.isArray(data.tokens) ? data.tokens : [];
  const errors = Array.isArray(data.erros) ? data.erros : [];
  currentTokens = tokens;
  tokenTbody.replaceChildren();
  sourceHighlight.replaceChildren();
  $('token-total').textContent = `${tokens.length} TOKENS`;

  tokens.forEach((token, index) => {
    const row = document.createElement('tr');
    row.tabIndex = 0;
    row.dataset.tokenIndex = index;
    row.setAttribute('aria-label', `Token ${index + 1}: ${token.lexema}, ${token.tipo}`);
    for (const value of [token.tipo.replaceAll('_', ' '), token.lexema, token.linha, token.coluna]) {
      row.append(safeText('td', '', String(value)));
    }
    row.addEventListener('click', () => selectToken(index));
    row.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); selectToken(index); } });
    tokenTbody.append(row);
  });

  // Os índices de Python contam pontos de código Unicode. Array.from usa a mesma regra.
  const letters = Array.from(code);
  const spans = [...tokens.map((t, index) => ({...t, index, erro: false})), ...errors.map(e => ({...e, erro: true}))]
    .sort((a, b) => a.inicio - b.inicio || a.fim - b.fim);
  let cursor = 0;
  for (const item of spans) {
    const start = Math.max(cursor, item.inicio);
    const end = Math.min(letters.length, item.fim);
    if (start > cursor) sourceHighlight.append(document.createTextNode(letters.slice(cursor, start).join('')));
    if (end > start) {
      const highlight = safeText('span', item.erro ? 'cat-error' : categoryClass(item.tipo), letters.slice(start, end).join(''));
      if (!item.erro) highlight.dataset.tokenIndex = item.index;
      if (item.erro) highlight.title = item.mensagem;
      else highlight.title = `${item.tipo}: ${item.lexema}`;
      if (!item.erro) highlight.addEventListener('click', () => selectToken(item.index));
      sourceHighlight.append(highlight);
    }
    cursor = Math.max(cursor, end);
  }
  if (cursor < letters.length) sourceHighlight.append(document.createTextNode(letters.slice(cursor).join('')));

  const errorSection = $('lexical-errors');
  const errorList = $('errors-list');
  errorList.replaceChildren();
  errorSection.hidden = errors.length === 0;
  for (const err of errors) {
    const item = safeText('div', 'lexical-error', '');
    item.append(safeText('strong', '', `Linha ${err.linha}, coluna ${err.coluna}`),
      safeText('p', '', err.mensagem));
    errorList.append(item);
  }
  section.hidden = false;
  selectToken(0);
}
function loadExample() { ++currentRequest; codigo.value = EXEMPLOS[exemplo.value] || ''; updateLines(); resetResult(); }
codigo.addEventListener('input', () => { ++currentRequest; updateLines(); resetResult(); });
codigo.addEventListener('scroll', () => { lineNumbers.scrollTop = codigo.scrollTop; });
exemplo.addEventListener('change', loadExample);
limpar.addEventListener('click', () => { ++currentRequest; codigo.value = ''; updateLines(); resetResult(); codigo.focus(); });
codigo.addEventListener('keydown', event => {
  if (event.key === 'Tab') {
    event.preventDefault();
    codigo.setRangeText('    ', codigo.selectionStart, codigo.selectionEnd, 'end');
    codigo.dispatchEvent(new Event('input', {bubbles: true}));
  }
});
tokenPrev.addEventListener('click', () => selectToken(selectedToken - 1));
tokenNext.addEventListener('click', () => selectToken(selectedToken + 1));
analisar.addEventListener('click', async () => {
  const code = codigo.value;
  const request = ++currentRequest;
  if (!code.trim()) { renderValidationError('Informe um código-fonte antes de solicitar a análise.'); return; }
  analisar.disabled = true;
  setStatus('ANALISANDO', 'neutral');
  footerStatus.textContent = 'Aguardando o scanner do servidor';
  try {
    const response = await fetch('/api/analisar', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({codigo: code})
    });
    const data = await response.json();
    if (request !== currentRequest) return;
    if (Array.isArray(data.tokens) && Array.isArray(data.erros)) {
      renderSummary(data);
      renderAnalysis(data, code);
    } else {
      renderValidationError(typeof data.mensagem === 'string' ? data.mensagem : 'Não foi possível analisar a entrada.');
    }
  } catch (_) {
    if (request === currentRequest) renderValidationError('Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.');
  } finally {
    analisar.disabled = false;
  }
});
loadExample();
