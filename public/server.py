from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'templates/products/create.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("Iniciando servidor...")
    print("Acesse: http://localhost:5000/templates/products/create.html")
    app.run(host='0.0.0.0', port=5000, debug=True) 