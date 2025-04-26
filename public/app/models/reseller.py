from app import db
from app.models.sale import Sale
from datetime import datetime

class Reseller(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    document = db.Column(db.String(20), unique=True)  # CPF/CNPJ
    commission_rate = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    photo_url = db.Column(db.String(200))  # URL da foto do revendedor
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relacionamentos
    orders = db.relationship('Order', back_populates='reseller', lazy='dynamic')
    sales = db.relationship('Sale', backref='reseller', lazy='dynamic')
    
    def __repr__(self):
        return f'<Reseller {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'document': self.document,
            'commission_rate': self.commission_rate,
            'is_active': self.is_active,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Tabela intermediária para relacionamento many-to-many entre Order e Product
order_products = db.Table('order_products',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False),
    db.Column('price_at_time', db.Float, nullable=False)  # Preço do produto no momento do pedido
)

class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Chaves estrangeiras
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'))
    
    # Relacionamentos
    reseller = db.relationship('Reseller', back_populates='orders')
    products = db.relationship('Product', secondary=order_products, back_populates='orders')
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'reseller_id': self.reseller_id
        }

@property
def current_inventory(self):
    """Retorna o estoque atual do revendedor por produto"""
    from app.models.product import Product
    from app.models.order import Order, order_products
    from app.models.sale import Sale, sale_products
    from sqlalchemy import func
    
    # Busca todos os pedidos entregues do revendedor
    delivered_orders = Order.query.filter_by(
        reseller_id=self.id,
        status='delivered'
    ).all()
    
    # Calcula o estoque atual
    inventory = {}
    for order in delivered_orders:
        # Busca os produtos do pedido
        products = db.session.query(
            Product,
            order_products.c.quantity,
            order_products.c.price_at_time
        ).join(
            order_products,
            Product.id == order_products.c.product_id
        ).filter(
            order_products.c.order_id == order.id
        ).all()
        
        for product, quantity, price in products:
            if product.id not in inventory:
                inventory[product.id] = {
                    'product': product,
                    'quantity': 0,
                    'last_sale': order.created_at
                }
            inventory[product.id]['quantity'] += quantity
    
    # Subtrai as vendas do estoque
    sales = Sale.query.filter_by(reseller_id=self.id).all()
    for sale in sales:
        # Busca os produtos da venda
        products = db.session.query(
            Product,
            sale_products.c.quantity,
            sale_products.c.price_at_time
        ).join(
            sale_products,
            Product.id == sale_products.c.product_id
        ).filter(
            sale_products.c.sale_id == sale.id
        ).all()
        
        for product, quantity, price in products:
            if product.id in inventory:
                if sale.sale_date > inventory[product.id]['last_sale']:
                    inventory[product.id]['last_sale'] = sale.sale_date
                inventory[product.id]['quantity'] -= quantity
    
    # Retorna apenas produtos com quantidade maior que zero
    return [(item['product'], item['quantity'], item['last_sale']) 
            for item in inventory.values() 
            if item['quantity'] > 0]

@property
def sales_by_product(self):
    """Retorna o histórico de vendas agrupado por produto"""
    from app.models.product import Product
    from app.models.sale import Sale, sale_products
    from sqlalchemy import func
    
    # Busca todas as vendas do revendedor
    sales = Sale.query.filter_by(reseller_id=self.id).all()
    
    # Agrupa as vendas por produto
    product_sales = {}
    for sale in sales:
        # Busca os produtos da venda
        products = db.session.query(
            Product,
            sale_products.c.quantity,
            sale_products.c.price_at_time
        ).join(
            sale_products,
            Product.id == sale_products.c.product_id
        ).filter(
            sale_products.c.sale_id == sale.id
        ).all()
        
        for product, quantity, price in products:
            if product.id not in product_sales:
                product_sales[product.id] = {
                    'product': product,
                    'total_quantity': 0,
                    'total_amount': 0,
                    'first_sale': sale.sale_date,
                    'last_sale': sale.sale_date
                }
            product_sales[product.id]['total_quantity'] += quantity
            product_sales[product.id]['total_amount'] += quantity * price
            if sale.sale_date < product_sales[product.id]['first_sale']:
                product_sales[product.id]['first_sale'] = sale.sale_date
            if sale.sale_date > product_sales[product.id]['last_sale']:
                product_sales[product.id]['last_sale'] = sale.sale_date
    
    # Retorna a lista formatada ordenada por quantidade vendida
    return sorted(
        [(item['product'], item['total_quantity'], item['total_amount'], 
          item['first_sale'], item['last_sale']) 
         for item in product_sales.values()],
        key=lambda x: x[1],  # Ordena por quantidade vendida
        reverse=True
    ) 