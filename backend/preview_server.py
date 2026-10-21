"""Servidor de pré-visualização LOCAL para validar o frontend sem Docker/Flask.

O endpoint usa exatamente backend.service.process_source, a mesma lógica do app Flask.
Não substitui o Flask na versão entregue via Docker Compose.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from sys import path
import json

path.insert(0, str(Path(__file__).resolve().parent))
from service import process_source

FRONTEND = Path(__file__).resolve().parent.parent / 'frontend'

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        if self.path == '/api/hello':
            self.send_json({'message':'Hello, World!'},200)
            return
        if self.path == '/api/health':
            self.send_json({'ok':True,'servico':'compiladores','status':'ativo'},200)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path != '/api/analisar':
            return self.send_json({'ok':False,'mensagem':'Rota não encontrada'},404)
        if 'application/json' not in self.headers.get('Content-Type',''):
            return self.send_json({'ok':False,'codigo_erro':'CONTENT_TYPE','mensagem':'Envie os dados no formato JSON.'},415)
        length = int(self.headers.get('Content-Length', 0))
        if length > 16000:
            return self.send_json({'ok':False,'codigo_erro':'ENTRADA_LONGA','mensagem':'Requisição muito extensa.'},413)
        try:
            payload=json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            payload=None
        data,status=process_source(payload)
        return self.send_json(data,status)

    def send_json(self, obj, status):
        data=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__=='__main__':
    server=ThreadingHTTPServer(('127.0.0.1', 8765),Handler)
    print('Pré-visualização em http://127.0.0.1:8765', flush=True)
    server.serve_forever()
