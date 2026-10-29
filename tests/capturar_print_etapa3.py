"""Gera um print real do scanner no navegador local, sem afirmar uso de Docker.

Exige: python -m pip install playwright; python -m playwright install chromium
Execute: python tests/capturar_print_etapa3.py
"""
from pathlib import Path
from shutil import which
from os import environ
from subprocess import Popen, DEVNULL
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8765'


def request_analysis(body):
    req = Request(BASE + '/api/analisar', data=body.encode('utf-8'),
                  headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(req, timeout=4) as response:
            return {'status': response.status, 'data': json.load(response)}
    except HTTPError as response:
        return {'status': response.code, 'data': json.loads(response.read().decode('utf-8'))}


def page_html():
    html = (ROOT / 'frontend/index.html').read_text(encoding='utf-8')
    css = (ROOT / 'frontend/style.css').read_text(encoding='utf-8')
    js = (ROOT / 'frontend/script.js').read_text(encoding='utf-8')
    return html.replace('<link rel="stylesheet" href="/style.css">', '<style>' + css + '</style>') \
               .replace('<script src="/script.js" defer></script>', '') \
               .replace('</body>', '<script>' + js + '</script></body>')


def main():
    proc = Popen([sys.executable, str(ROOT / 'backend/preview_server.py')], stdout=DEVNULL, stderr=DEVNULL)
    try:
        for _ in range(50):
            try:
                with urlopen(BASE + '/api/health', timeout=.3):
                    break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError('Servidor local de pré-visualização não iniciou.')
        with sync_playwright() as p:
            executable = environ.get('CHROMIUM_EXECUTABLE') or which('chromium') or which('chromium-browser')
            browser = p.chromium.launch(headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'],
                **({'executable_path': executable} if executable else {}))
            page = browser.new_page(viewport={'width': 1440, 'height': 960}, device_scale_factor=1)
            page.expose_function('callBackend', request_analysis)
            page.set_content(page_html(), wait_until='domcontentloaded')
            page.evaluate('''() => { window.fetch = async (url, options) => {
              const response = await window.callBackend(options.body);
              return {ok: response.status >= 200 && response.status < 300,
                      status: response.status, json: async () => response.data};
            }; }''')
            page.locator('#exemplo').select_option('condicional')
            page.locator('#analisar').click()
            page.get_by_text('Tokens identificados', exact=True).wait_for(timeout=5000)
            target = ROOT / 'docs/print_interface_etapa3.png'
            page.screenshot(path=str(target), full_page=True, animations='disabled')
            print('Screenshot salvo em', target)
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()


if __name__ == '__main__':
    main()
