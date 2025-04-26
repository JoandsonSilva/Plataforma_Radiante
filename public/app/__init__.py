from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Criar diretório de uploads se não existir
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Criar diretório específico para fotos de revendedores
    resellers_upload_folder = os.path.join('app', 'static', 'uploads', 'resellers')
    if not os.path.exists(resellers_upload_folder):
        os.makedirs(resellers_upload_folder)

    # Importar modelos
    from app.models.user import User
    from app.models.product import Product
    from app.models.task import Task
    from app.models.reseller import Reseller, Order
    from app.models.sale import Sale

    # Registro dos blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.tasks import tasks_bp
    from app.routes.resellers import resellers_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(resellers_bp, url_prefix='/resellers')

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Criar todas as tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app 