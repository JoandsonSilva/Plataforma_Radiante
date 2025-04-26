import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Garantir que o diretório instance existe
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

class Config:
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    TESTING = False
    ENV = os.environ.get('FLASK_ENV') or 'production'
    
    # Configuração do banco de dados
    db_path = os.path.join(instance_path, 'app.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = 30 * 24 * 60 * 60  # 30 dias em segundos
    SESSION_COOKIE_SECURE = False  # Permitir em desenvolvimento
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 30 * 24 * 60 * 60  # 30 dias em segundos
    REMEMBER_COOKIE_SECURE = False  # Permitir em desenvolvimento
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações de upload
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Configurações do Firebase
    FIREBASE_CONFIG = {
        "apiKey": "AIzaSyB3b8HR1Gcmfp4YMh7Ibj7a-X7sGYd_6uk",
        "authDomain": "plataforma-radiante.firebaseapp.com",
        "projectId": "plataforma-radiante",
        "storageBucket": "plataforma-radiante.firebasestorage.app",
        "messagingSenderId": "990096383941",
        "appId": "1:990096383941:web:46541971f9a5e86ead75ac",
        "measurementId": "G-VZZZYRQZFP"
    }

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "dev.db")}'
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SESSION_COOKIE_SECURE = False  # Desabilitar em desenvolvimento
    REMEMBER_COOKIE_SECURE = False  # Desabilitar em desenvolvimento

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production' 