"""Testes HTTP + interface usando um servidor de pré-visualização local.

Servidor local sem Flask reaproveita o módulo service (lógica comum).
Os testes não substituem testes de Docker ou do wrapper Flask em produção.
"""
import json
import subprocess
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error
import pytest

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8765'

@pytest.fixture(scope='module')
def server():
    proc=subprocess.Popen([sys.executable,str(ROOT/'backend'/'preview_server.py')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            with urllib.request.urlopen(BASE+'/api/health',timeout=.3) as resp:
                if resp.status==200: break
        except Exception:
            time.sleep(.1)
    else:
        proc.terminate(); raise AssertionError('Preview server não iniciou')
    yield proc
    proc.terminate()
    try: proc.wait(timeout=3)
    except subprocess.TimeoutExpired: proc.kill()


def post(payload,content_type='application/json'):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE+'/api/analisar',data=data,headers={'Content-Type':content_type},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=4) as resp: return resp.status,json.load(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


def test_http_validacao_endpoints(server):
    with urllib.request.urlopen(BASE+'/api/hello',timeout=4) as resp:
        assert resp.status==200 and json.load(resp)['message']=='Hello, World!'
    s,data=post({'codigo':'x = 1'})
    assert s==200 and data['ok'] and data['recebido'] and len(data['tokens'])==3
    s,data=post({'codigo':'x @ 1'})
    assert s==422 and not data['sucesso'] and data['erros'][0]['coluna']==3
    s,data=post({'codigo':'   '})
    assert s==400 and data['codigo_erro']=='ENTRADA_VAZIA'
    s,data=post({})
    assert s==400 and data['codigo_erro']=='CAMPO_AUSENTE'
    s,data=post({'codigo':'x=1'},content_type='text/plain')
    assert s==415 and data['codigo_erro']=='CONTENT_TYPE'


def _html_local():
    page=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')
    css=(ROOT/'frontend'/'style.css').read_text(encoding='utf-8')
    js=(ROOT/'frontend'/'script.js').read_text(encoding='utf-8')
    page=page.replace('<link rel="stylesheet" href="/style.css">', '<style>'+css+'</style>')
    page=page.replace('<script src="/script.js" defer></script>', '')
    return page.replace('</body>', '<script>'+js+'</script></body>')


def _call_backend(json_body):
    req=urllib.request.Request(BASE+'/api/analisar', data=json_body.encode('utf-8'),
            headers={'Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req,timeout=4) as resp:
            return {'status':resp.status,'data':json.load(resp)}
    except urllib.error.HTTPError as e:
        return {'status':e.code,'data':json.loads(e.read().decode('utf-8'))}


def test_interface_exemplos_e_comunicacao(server):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        from os import environ
        from shutil import which
        executable = environ.get('CHROMIUM_EXECUTABLE') or which('chromium') or which('chromium-browser')
        launch_kwargs = {'executable_path':executable} if executable else {}
        browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'],**launch_kwargs)
        page=browser.new_page(viewport={'width':1440,'height':1024},device_scale_factor=1)
        page.expose_function('callBackend', _call_backend)
        page.set_content(_html_local(), wait_until='domcontentloaded')
        # A política deste navegador bloqueia tráfego local diretamente.
        # A chamada chega à API real pela ponte de testes do Playwright.
        page.evaluate('''() => { window.fetch = async (url, opts) => {
          const response = await window.callBackend(opts.body);
          return {ok: response.status >= 200 && response.status < 300,
                  status: response.status, json: async () => response.data};
        }; }''')
        assert page.get_by_role('heading',name='Explore o código. Aprenda cada etapa.').count()==1
        editor=page.locator('#codigo')
        assert 'numero = 10' in editor.input_value()
        page.locator('#exemplo').select_option('aritmetica')
        assert 'resto = soma - 2' in editor.input_value()
        editor.fill('nota = 10 + 3\nprint(nota)')
        assert 'nota = 10 + 3' in editor.input_value()
        page.locator('#analisar').click()
        page.get_by_text('Tokens identificados',exact=True).wait_for(timeout=4000)
        assert page.locator('#result-status').inner_text()=='CONCLUÍDO'
        assert page.locator('#footer-status').inner_text()=='Análise léxica realizada no backend'
        assert page.locator('#tokens-tbody tr').count() >= 8
        assert page.locator('#token-step').inner_text().startswith('1 de ')
        page.locator('#token-next').click()
        assert page.locator('#token-step').inner_text().startswith('2 de ')
        page.locator('#exemplo').select_option('erro')
        page.locator('#analisar').click()
        page.get_by_text('Erros léxicos identificados').wait_for(timeout=4000)
        assert page.locator('#result-status').inner_text()=='COM ERROS'
        assert '@' in page.locator('#source-highlight').inner_text()
        assert page.locator('#errors-list .lexical-error').count()==1
        page.locator('#exemplo').select_option('operadores')
        assert 'quociente = dobro / 3' in editor.input_value()
        page.locator('#limpar').click()
        assert editor.input_value()==''
        page.locator('#analisar').click()
        assert page.get_by_text('Informe um código-fonte antes de solicitar a análise.').count()>=1
        browser.close()


def test_interface_mobile_sem_rolagem_horizontal(server):
    """A apresentação em celular permanece legível e o editor pode ser utilizado."""
    from playwright.sync_api import sync_playwright
    from os import environ
    from shutil import which
    with sync_playwright() as p:
        executable = environ.get('CHROMIUM_EXECUTABLE') or which('chromium') or which('chromium-browser')
        kwargs = {'executable_path': executable} if executable else {}
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'], **kwargs)
        page = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        page.set_content(_html_local(), wait_until='domcontentloaded')
        assert page.locator('#codigo').is_visible()
        assert page.locator('#exemplo').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        browser.close()
