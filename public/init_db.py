from app import create_app, db
from app.models.user import User
from config import DevelopmentConfig
import os

def init_db():
    print("🚀 Inicializando banco de dados...")
    
    # Garantir que o diretório instance existe
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"📁 Diretório instance criado em: {instance_path}")
    
    # Criar a aplicação com a configuração de desenvolvimento
    app = create_app(DevelopmentConfig)
    print(f"📝 Usando banco de dados: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        try:
            # Remover todas as tabelas existentes
            db.drop_all()
            print("🗑️ Tabelas antigas removidas")
            
            # Criar todas as tabelas novamente
            db.create_all()
            print("✅ Novas tabelas criadas com sucesso!")
            
            # Criar usuário admin
            admin = User(
                email='admin@example.com',
                username='admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
            
            print("✨ Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {str(e)}")
            raise

if __name__ == "__main__":
    init_db() 