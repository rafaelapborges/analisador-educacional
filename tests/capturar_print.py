"""Gera uma captura do Chromium usando a API local de pré-visualização.

A API real é acessada por Python devido à política de rede do navegador de teste.
Não substitui a verificação do Docker Compose em outro ambiente.
"""
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright
from test_e2e import BASE, ROOT, _html_local, _call_backend

out=ROOT/'docs'/'print_interface_etapa2.png'
proc=subprocess.Popen([sys.executable,str(ROOT/'backend'/'preview_server.py')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(30):
        try:
            with urllib.request.urlopen(BASE+'/api/health',timeout=.3) as resp:
                if resp.status==200: break
        except Exception:
            time.sleep(.1)
    else:
        raise RuntimeError('Servidor de preview não disponível')
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':1024},device_scale_factor=1)
        page.expose_function('callBackend',_call_backend)
        page.set_content(_html_local(),wait_until='domcontentloaded')
        page.evaluate('''() => {window.fetch = async (url, opts) => {
            const response = await window.callBackend(opts.body);
            return {ok: response.status >= 200 && response.status < 300,
                    status: response.status, json: async () => response.data};
        };}''')
        page.locator('#exemplo').select_option('aritmetica')
        page.locator('#analisar').click()
        page.get_by_text('Código recebido com sucesso',exact=True).wait_for(timeout=3000)
        print('UI STATUS',page.locator('#result-status').inner_text())
        page.screenshot(path=str(out),full_page=True)
        print(out)
        browser.close()
finally:
    proc.terminate()
    proc.wait(timeout=3)
