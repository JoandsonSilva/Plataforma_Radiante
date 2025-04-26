from app import create_app, db
from app.models.product import Product

app = create_app()

with app.app_context():
    # Adiciona o campo status se não existir
    db.session.execute('ALTER TABLE product ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT "active"')
    
    # Atualiza o status de todos os produtos existentes para 'active'
    Product.query.update({Product.status: 'active'})
    
    db.session.commit()
    print("Banco de dados atualizado com sucesso!") 