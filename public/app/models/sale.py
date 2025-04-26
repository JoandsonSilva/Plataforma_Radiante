from app import db
from datetime import datetime

# Tabela de relacionamento many-to-many entre Sale e Product
sale_products = db.Table('sale_products',
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False),
    db.Column('price_at_time', db.Float, nullable=False)
)

class Sale(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(500))
    
    # Relação com produtos
    products = db.relationship('Product', secondary=sale_products, 
                             backref=db.backref('sales', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Sale {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'commission': self.commission,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'description': self.description,
            'reseller_id': self.reseller_id,
            'products': [{
                'id': product.id,
                'name': product.name,
                'quantity': db.session.query(sale_products).filter_by(
                    sale_id=self.id, product_id=product.id).first().quantity,
                'price_at_time': db.session.query(sale_products).filter_by(
                    sale_id=self.id, product_id=product.id).first().price_at_time
            } for product in self.products]
        }

    @property
    def products_with_details(self):
        """Retorna os produtos da venda com suas quantidades e preços"""
        from app.models.product import Product
        from sqlalchemy import func
        
        # Busca os produtos da venda
        products = db.session.query(
            Product,
            sale_products.c.quantity,
            sale_products.c.price_at_time
        ).join(
            sale_products,
            Product.id == sale_products.c.product_id
        ).filter(
            sale_products.c.sale_id == self.id
        ).all()
        
        return products 