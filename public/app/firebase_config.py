import os
import pyrebase

# Configuração do Firebase
firebase_config = {
    "apiKey": "AIzaSyB3b8HR1Gcmfp4YMh7Ibj7a-X7sGYd_6uk",
    "authDomain": "plataforma-radiante.firebaseapp.com",
    "projectId": "plataforma-radiante",
    "storageBucket": "plataforma-radiante.firebasestorage.app",
    "messagingSenderId": "990096383941",
    "appId": "1:990096383941:web:46541971f9a5e86ead75ac",
    "measurementId": "G-VZZZYRQZFP"
}

# Verificar se estamos em ambiente de desenvolvimento
is_dev = os.environ.get('FLASK_ENV') == 'development'

if is_dev:
    # Configurações para ambiente de desenvolvimento
    firebase_config["authDomain"] = "localhost:9099"
    firebase_config["databaseURL"] = "http://localhost:9000"
    print("⚠️ Modo de desenvolvimento ativado - usando emuladores do Firebase")
else:
    # Configurações para produção
    firebase_config["authDomain"] = "plataforma-radiante.firebaseapp.com"
    firebase_config["databaseURL"] = "https://plataforma-radiante.firebaseio.com"
    print("✅ Modo de produção ativado - usando Firebase real")

# Inicializar o Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth_firebase = firebase.auth()

def verify_token(token):
    try:
        # Verificação do token usando Pyrebase
        user = auth_firebase.get_account_info(token)
        print(f"Token verificado com sucesso: {user}")  # Log para debug
        
        # Extrair informações do usuário
        if 'users' in user and len(user['users']) > 0:
            user_info = user['users'][0]
            return {
                'email': user_info.get('email'),
                'uid': user_info.get('localId'),
                'email_verified': user_info.get('emailVerified', False),
                'provider_id': user_info.get('providerUserInfo', [{}])[0].get('providerId', '')
            }
        return None
    except Exception as e:
        print(f"Erro ao verificar token: {str(e)}")  # Log do erro para debug
        return None

def get_user_by_email(email):
    try:
        # Buscar usuário usando Pyrebase
        users = auth_firebase.get_users()
        for user in users:
            if user.email == email:
                return user
        return None
    except Exception as e:
        print(f"Erro ao buscar usuário por email: {str(e)}")
        return None

def create_user(email, password):
    try:
        user = auth_firebase.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
        return None 