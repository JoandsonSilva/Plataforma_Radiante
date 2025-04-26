from app.firebase_config import create_user, verify_token, auth_firebase
import os

def test_authentication():
    # Teste de criação de usuário
    test_email = "test@example.com"
    test_password = "test123456"
    
    print("Testando criação de usuário...")
    try:
        user = create_user(test_email, test_password)
        if user:
            print("✅ Usuário criado com sucesso!")
        else:
            print("❌ Falha ao criar usuário")
            return
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {str(e)}")
        return

    # Teste de autenticação
    print("\nTestando autenticação...")
    try:
        user = auth_firebase.sign_in_with_email_and_password(test_email, test_password)
        if user:
            print("✅ Autenticação bem-sucedida!")
            print(f"ID do usuário: {user['localId']}")
        else:
            print("❌ Falha na autenticação")
            return
    except Exception as e:
        print(f"❌ Erro na autenticação: {str(e)}")
        return

    # Teste de verificação de token
    print("\nTestando verificação de token...")
    try:
        token = user['idToken']
        decoded_token = verify_token(token)
        if decoded_token:
            print("✅ Token verificado com sucesso!")
            print(f"UID do usuário: {decoded_token['uid']}")
        else:
            print("❌ Falha na verificação do token")
    except Exception as e:
        print(f"❌ Erro na verificação do token: {str(e)}")

if __name__ == "__main__":
    test_authentication() 