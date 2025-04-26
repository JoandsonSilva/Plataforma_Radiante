from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Configurar o diretório de templates e arquivos estáticos
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static')
    
    # Configurar o modo debug
    app.debug = True
    
    # Iniciar o servidor
    app.run(host='0.0.0.0', port=5000) 