"""Servidor Flask para a segunda etapa do software educacional."""
from flask import Flask, jsonify, request
from service import process_source

app = Flask(__name__)


@app.get('/api/hello')
def hello():
    """Rota preservada da etapa 1 para teste de regressão."""
    return jsonify({'message': 'Hello, World!'}), 200


@app.get('/api/health')
def health():
    return jsonify({'ok': True, 'servico': 'compiladores', 'status': 'ativo'}), 200


@app.post('/api/analisar')
def analisar():
    if not request.is_json:
        return jsonify({'ok': False, 'codigo_erro': 'CONTENT_TYPE',
                        'mensagem': 'Envie os dados no formato JSON.'}), 415
    payload, status = process_source(request.get_json(silent=True))
    return jsonify(payload), status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
