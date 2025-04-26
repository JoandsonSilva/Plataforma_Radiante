from app import create_app
from config import DevelopmentConfig
import os

# Configurar ambiente de desenvolvimento
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Criar aplicação com configurações de desenvolvimento
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # Garantir que o diretório de templates está configurado corretamente
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static')
    
    # Iniciar o servidor
    print("🚀 Iniciando servidor de desenvolvimento...")
    print("📡 Acesse: http://localhost:5000")
    print("🔧 Modo de depuração: ATIVADO")
    print("🔄 Recarregamento automático: ATIVADO")
    
    app.run(
        host='0.0.0.0',  # Localhost
        port=5000,
        debug=True,
        use_reloader=True
    ) 