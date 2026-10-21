'use strict';
const EXEMPLOS = Object.freeze({
  variavel: '# Exemplo 01 · Variáveis e atribuição\nnumero = 10\ntotal = 5',
  aritmetica: '# Exemplo 02 · Soma e subtração\nsoma = 10 + 5\nresto = soma - 2',
  operadores: '# Exemplo 03 · Multiplicação e divisão\ndobro = 6 * 2\nquociente = dobro / 3'
});
const codigo = document.getElementById('codigo');
const exemplo = document.getElementById('exemplo');
const analisar = document.getElementById('analisar');
const limpar = document.getElementById('limpar');
const resultBody = document.getElementById('result-body');
const resultStatus = document.getElementById('result-status');
const footerStatus = document.getElementById('footer-status');
const lineNumbers = document.getElementById('line-numbers');
let currentRequest = 0;
function lineCount(){return Math.max(1,codigo.value.split('\n').length)}
function updateLines(){lineNumbers.textContent=Array.from({length:lineCount()},(_,i)=>i+1).join('\n')}
function setStatus(label,kind){resultStatus.textContent=label;resultStatus.className='result-badge '+kind}
function resetResult(){resultBody.className='result-body';resultBody.innerHTML='<div class="empty-icon">↗</div><h3>Pronto para começar</h3><p>O resultado aparecerá aqui depois que você enviar um código para validação.</p>';setStatus('AGUARDANDO','neutral');footerStatus.textContent='Aguardando entrada'}
function safeText(tag,cls,value){const x=document.createElement(tag);if(cls)x.className=cls;x.textContent=value;return x}
function renderSuccess(data){resultBody.className='result-body success';resultBody.replaceChildren(safeText('div','result-mark','✓'),safeText('h3','', 'Código recebido com sucesso'),safeText('p','',data.mensagem),safeText('span','detail-label','RESUMO DA ENTRADA'));const grid=safeText('div','stat-grid','');for(const [v,label] of [[data.linhas,'Linhas enviadas'],[data.caracteres,'Caracteres']]){const stat=safeText('div','stat','');stat.append(safeText('strong','',String(v)),safeText('span','',label));grid.append(stat)}resultBody.append(grid,safeText('p','','As análises do compilador serão implementadas em etapas futuras.'));setStatus('RECEBIDO','success');footerStatus.textContent='Resposta recebida do backend'}
function renderError(message){resultBody.className='result-body error';resultBody.replaceChildren(safeText('div','result-mark','!'),safeText('h3','','Não foi possível processar'),safeText('p','',message));setStatus('ATENÇÃO','error');footerStatus.textContent='Verifique a entrada e tente novamente'}
function loadExample(){++currentRequest;codigo.value=EXEMPLOS[exemplo.value]||'';updateLines();resetResult()}
codigo.addEventListener('input',()=>{++currentRequest;updateLines();resetResult()});
codigo.addEventListener('scroll',()=>lineNumbers.scrollTop=codigo.scrollTop);
exemplo.addEventListener('change',loadExample);
limpar.addEventListener('click',()=>{++currentRequest;codigo.value='';updateLines();resetResult();codigo.focus()});
codigo.addEventListener('keydown',event=>{if(event.key==='Tab'){event.preventDefault();const a=codigo.selectionStart,b=codigo.selectionEnd;codigo.setRangeText('    ',a,b,'end');updateLines()}});
analisar.addEventListener('click',async()=>{
  const code=codigo.value;
  if(!code.trim()){renderError('Informe um código-fonte antes de solicitar a análise.');return}
  const request=++currentRequest;
  analisar.disabled=true;
  setStatus('ENVIANDO','neutral');footerStatus.textContent='Aguardando resposta do servidor';
  try{
    const response=await fetch('/api/analisar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({codigo:code})});
    const data=await response.json();
    if(request!==currentRequest)return;
    if(!response.ok || !data.ok){renderError(typeof data.mensagem==='string'?data.mensagem:'Não foi possível validar o código.');return}
    renderSuccess(data);
  }catch(_){if(request===currentRequest)renderError('Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.')}
  finally{if(request===currentRequest)analisar.disabled=false;else analisar.disabled=false}
});
loadExample();
