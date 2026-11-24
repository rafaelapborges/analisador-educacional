/* Etapa 4: árvore sintática e explicações dos erros, sem execução de código. */
(function () {
  'use strict';
  let host = null;
  const make = (tag, cls='', value=null) => {
    const el = document.createElement(tag);
    if (cls) el.className=cls;
    if (value!==null) el.textContent=String(value);
    return el;
  };
  function ensure() {
    if (host) return host;
    const anchor=document.getElementById('lexical-section');
    if (!anchor) return null;
    host=make('section','ast-section');
    host.id='syntax-section';
    host.hidden=true;
    host.setAttribute('aria-label','Análise sintática e árvore AST');
    anchor.insertAdjacentElement('afterend',host);
    return host;
  }
  function reset() {
    const target=ensure();
    if (target) {target.replaceChildren();target.hidden=true;}
  }
  function selectSource(n) {
    const editor=document.getElementById('codigo');
    if (!editor || !Number.isInteger(n.inicio)||!Number.isInteger(n.fim)) return;
    editor.focus();
    editor.setSelectionRange(n.inicio,n.fim);
    editor.scrollIntoView({behavior:'smooth',block:'nearest'});
  }
  function tree(parent,value,key,depth,counter) {
    if (++counter.n>800) {
      if (!counter.warned) parent.append(make('p','ast-muted','Visualização abreviada após 800 elementos.'));
      counter.warned=true;return;
    }
    if (depth>18) {parent.append(make('p','ast-muted','Subárvore recolhida pelo limite de profundidade.'));return;}
    if (Array.isArray(value)) {
      const block=make('details','ast-branch');block.open=depth<2;
      block.append(make('summary','',key+' · '+value.length+' item(ns)'));
      for (let i=0;i<value.length;i++) tree(block,value[i],'['+(i+1)+']',depth+1,counter);
      parent.append(block);
    } else if (value && typeof value==='object') {
      const block=make('details','ast-branch');block.open=depth<2;
      const label=value.tipo||key;
      const suffix=value.nome ? ' · '+value.nome : value.operador ? ' · '+value.operador : '';
      block.append(make('summary','',label+suffix));
      if (Number.isInteger(value.inicio)&&Number.isInteger(value.fim)) {
        const b=make('button','ast-locate','Localizar no código');b.type='button';
        b.setAttribute('aria-label','Destacar '+label+' no editor');
        b.addEventListener('click',()=>selectSource(value));block.append(b);
      }
      for (const [childKey,child] of Object.entries(value)) {
        if (['tipo','linha','coluna','inicio','fim'].includes(childKey)) continue;
        tree(block,child,childKey,depth+1,counter);
      }
      if (Number.isInteger(value.linha)) block.append(make('span','ast-pos','Linha '+value.linha+', coluna '+value.coluna));
      parent.append(block);
    } else parent.append(make('p','ast-leaf',key+': '+String(value)));
  }
  function render(data) {
    const target=ensure();if (!target) return;
    target.hidden=false;target.replaceChildren();
    const title=make('div','ast-heading');
    title.append(make('h3','','Análise sintática · Árvore AST'));
    const state=data.sintaxe&&data.sintaxe.status;
    title.append(make('span','ast-status',state==='valida'?'ESTRUTURA VÁLIDA':state==='nao_executada'?'NÃO EXECUTADA':'ERROS SINTÁTICOS'));
    target.append(title);
    if (state==='nao_executada') {
      target.append(make('p','ast-muted','Primeiro corrija os erros léxicos acima. O parser só analisa uma sequência válida de tokens.'));
      return;
    }
    const errors=Array.isArray(data.erros_sintaticos)?data.erros_sintaticos:[];
    if (errors.length) {
      const list=make('div','ast-errors');
      list.append(make('h4','','Erros sintáticos — entenda a regra violada'));
      for (const error of errors) {
        const article=make('article','syntax-error-item');
        article.append(make('strong','',`Linha ${error.linha}, coluna ${error.coluna}: ${error.mensagem}`));
        if (error.regra) article.append(make('p','','Regra gramatical: '+error.regra));
        if (Array.isArray(error.esperado)&&error.esperado.length) article.append(make('p','','Esperado: '+error.esperado.join(' ou ')));
        if (error.encontrado) article.append(make('p','','Encontrado: '+error.encontrado));
        if (error.sugestao) article.append(make('p','','Como corrigir: '+error.sugestao));
        list.append(article);
      }
      target.append(list);
    }
    if (data.ast && typeof data.ast==='object') {
      target.append(make('p','ast-muted','Esta é a AST, uma representação simplificada do programa (não a árvore de derivação). Abra os nós e use “Localizar no código” para relacioná-los ao editor.'));
      const wrapper=make('div','ast-tree');tree(wrapper,data.ast,'AST',0,{n:0,warned:false});
      target.append(wrapper);
    }
  }
  window.lexlabRenderAST=render;
  window.lexlabResetAST=reset;
})();
