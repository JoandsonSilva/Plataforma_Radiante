from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.reseller import Reseller, Order, order_products
from app.models.product import Product
from app.models.sale import Sale, sale_products
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from sqlalchemy import insert
import json

resellers_bp = Blueprint('resellers', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resellers_bp.route('/resellers')
@login_required
def index():
    resellers = Reseller.query.all()
    return render_template('resellers/index.html', resellers=resellers)

@resellers_bp.route('/resellers/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        document = request.form.get('document')
        commission_rate = float(request.form.get('commission_rate'))
        
        reseller = Reseller(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            document=document,
            commission_rate=commission_rate
        )
        
        # Processar upload da foto
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                # Gerar um nome único para o arquivo
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                photo.save(os.path.join('app', 'static', 'uploads', 'resellers', unique_filename))
                reseller.photo_url = f'/static/uploads/resellers/{unique_filename}'
        
        db.session.add(reseller)
        db.session.commit()
        
        flash('Revendedor criado com sucesso!', 'success')
        return redirect(url_for('resellers.index'))
    
    return render_template('resellers/create.html')

@resellers_bp.route('/resellers/<int:id>')
@login_required
def show(id):
    reseller = Reseller.query.get_or_404(id)
    orders = Order.query.filter_by(reseller_id=id).all()
    sales = Sale.query.filter_by(reseller_id=id).all()
    
    # Carregar os produtos de cada pedido
    for order in orders:
        order.products_with_details = db.session.query(Product, order_products.c.quantity, order_products.c.price_at_time)\
            .select_from(order_products)\
            .join(Product, Product.id == order_products.c.product_id)\
            .filter(order_products.c.order_id == order.id)\
            .all()
    
    return render_template('resellers/show.html', 
                         reseller=reseller, 
                         orders=orders, 
                         sales=sales)

@resellers_bp.route('/resellers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    reseller = Reseller.query.get_or_404(id)
    
    if request.method == 'POST':
        reseller.name = request.form.get('name')
        reseller.email = request.form.get('email')
        reseller.phone = request.form.get('phone')
        reseller.address = request.form.get('address')
        reseller.city = request.form.get('city')
        reseller.state = request.form.get('state')
        reseller.zip_code = request.form.get('zip_code')
        reseller.document = request.form.get('document')
        reseller.commission_rate = float(request.form.get('commission_rate'))
        reseller.is_active = request.form.get('is_active') == 'on'
        
        # Processar upload da foto
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                # Remover foto antiga se existir
                if reseller.photo_url:
                    old_photo_path = os.path.join('app', 'static', 'uploads', 'resellers', 
                                                os.path.basename(reseller.photo_url))
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                # Salvar nova foto
                filename = secure_filename(photo.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                photo.save(os.path.join('app', 'static', 'uploads', 'resellers', unique_filename))
                reseller.photo_url = f'/static/uploads/resellers/{unique_filename}'
        
        db.session.commit()
        
        flash('Revendedor atualizado com sucesso!', 'success')
        return redirect(url_for('resellers.show', id=reseller.id))
    
    return render_template('resellers/edit.html', reseller=reseller)

@resellers_bp.route('/resellers/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    reseller = Reseller.query.get_or_404(id)
    db.session.delete(reseller)
    db.session.commit()
    
    flash('Revendedor removido com sucesso!', 'success')
    return redirect(url_for('resellers.index'))

@resellers_bp.route('/resellers/<int:id>/orders/create', methods=['GET', 'POST'])
@login_required
def create_order(id):
    reseller = Reseller.query.get_or_404(id)
    products = Product.query.filter_by(status='active').all()
    
    if request.method == 'POST':
        # Criar o pedido
        order = Order(
            reseller_id=id,
            status='pending',
            total_price=0  # Será calculado com base nos produtos
        )
        
        db.session.add(order)
        db.session.flush()  # Gera o ID do pedido sem commitar
        
        # Processar produtos do pedido
        product_ids = request.form.getlist('product_ids[]')
        quantities = request.form.getlist('quantities[]')
        
        # Agrupar produtos iguais
        product_quantities = {}
        for product_id, quantity in zip(product_ids, quantities):
            if not quantity or int(quantity) <= 0:
                continue
            product_id = int(product_id)
            quantity = int(quantity)
            if product_id in product_quantities:
                product_quantities[product_id] += quantity
            else:
                product_quantities[product_id] = quantity
        
        # Registrar produtos no pedido e criar venda
        total_amount = 0
        for product_id, total_quantity in product_quantities.items():
            product = Product.query.get(product_id)
            if not product:
                continue
                
            # Registrar produto no pedido
            stmt = insert(order_products).values(
                order_id=order.id,
                product_id=product.id,
                quantity=total_quantity,
                price_at_time=product.price
            )
            db.session.execute(stmt)
            
            # Adicionar ao valor total
            total_amount += product.price * total_quantity
        
        # Atualizar valor total do pedido
        order.total_price = total_amount
        
        # Criar venda se houver produtos
        if product_quantities:
            sale = Sale(
                reseller_id=id,
                sale_date=datetime.now(),
                description=f"Venda registrada com pedido #{order.id}",
                amount=total_amount,
                commission=total_amount * (reseller.commission_rate / 100)
            )
            
            db.session.add(sale)
            db.session.flush()
            
            # Registrar produtos na venda
            for product_id, total_quantity in product_quantities.items():
                product = Product.query.get(product_id)
                stmt = insert(sale_products).values(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=total_quantity,
                    price_at_time=product.price
                )
                db.session.execute(stmt)
                
                # Atualizar estoque
                product.stock -= total_quantity
        
        db.session.commit()
        
        flash('Pedido criado e venda registrada com sucesso!', 'success')
        return redirect(url_for('resellers.show', id=id))
    
    return render_template('resellers/create_order.html', reseller=reseller, products=products)

@resellers_bp.route('/resellers/<int:id>/sales/create', methods=['GET', 'POST'])
@login_required
def create_sale(id):
    reseller = Reseller.query.get_or_404(id)
    products = Product.query.filter_by(status='active').all()
    
    if request.method == 'POST':
        sale_date = datetime.strptime(request.form.get('sale_date'), '%Y-%m-%d')
        description = request.form.get('description', '')
        
        # Criar a venda
        sale = Sale(
            reseller_id=id,
            sale_date=sale_date,
            description=description,
            amount=0,  # Será calculado com base nos produtos
            commission=0  # Será calculado com base no valor total
        )
        
        db.session.add(sale)
        db.session.flush()  # Gera o ID da venda sem commitar
        
        total_amount = 0
        # Processar produtos vendidos
        product_ids = request.form.getlist('product_ids[]')
        quantities = request.form.getlist('quantities[]')
        
        # Agrupar produtos iguais
        product_quantities = {}
        for product_id, quantity in zip(product_ids, quantities):
            if not quantity or int(quantity) <= 0:
                continue
            product_id = int(product_id)
            quantity = int(quantity)
            if product_id in product_quantities:
                product_quantities[product_id] += quantity
            else:
                product_quantities[product_id] = quantity
        
        # Registrar produtos na venda
        for product_id, total_quantity in product_quantities.items():
            product = Product.query.get(product_id)
            if not product:
                continue
                
            # Registrar produto na venda
            stmt = insert(sale_products).values(
                sale_id=sale.id,
                product_id=product.id,
                quantity=total_quantity,
                price_at_time=product.price
            )
            db.session.execute(stmt)
            
            # Atualizar estoque
            product.stock -= total_quantity
            
            # Adicionar ao valor total
            total_amount += product.price * total_quantity
        
        # Atualizar valor total e comissão
        sale.amount = total_amount
        sale.commission = total_amount * (reseller.commission_rate / 100)
        
        db.session.commit()
        
        flash('Venda registrada com sucesso!', 'success')
        return redirect(url_for('resellers.show', id=id))
    
    return render_template('resellers/create_sale.html', reseller=reseller, products=products, now=datetime.now())

@resellers_bp.route('/resellers/<int:id>/sales/monthly', methods=['GET', 'POST'])
@login_required
def monthly_sales(id):
    reseller = Reseller.query.get_or_404(id)
    
    if request.method == 'POST':
        # Obter dados do formulário
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        sales_data = request.form.getlist('sales_data[]')
        
        # Criar venda mensal
        sale = Sale(
            reseller_id=id,
            sale_date=datetime(year, month, 1),
            description=f"Venda mensal - {month}/{year}",
            amount=0,  # Será calculado com base nos produtos
            commission=0  # Será calculado com base no valor total
        )
        
        db.session.add(sale)
        db.session.flush()
        
        total_amount = 0
        # Processar produtos vendidos
        for data in sales_data:
            product_id, quantity = data.split(':')
            product_id = int(product_id)
            quantity = int(quantity)
            
            if quantity <= 0:
                continue
                
            product = Product.query.get(product_id)
            if not product:
                continue
            
            # Registrar produto na venda
            stmt = insert(sale_products).values(
                sale_id=sale.id,
                product_id=product.id,
                quantity=quantity,
                price_at_time=product.price
            )
            db.session.execute(stmt)
            
            # Atualizar estoque
            product.stock -= quantity
            
            # Adicionar ao valor total
            total_amount += product.price * quantity
        
        # Atualizar valor total e comissão
        sale.amount = total_amount
        sale.commission = total_amount * (reseller.commission_rate / 100)
        
        db.session.commit()
        
        flash('Venda mensal registrada com sucesso!', 'success')
        return redirect(url_for('resellers.show', id=id))
    
    # Para GET, mostrar formulário de registro mensal
    products = Product.query.filter_by(status='active').all()
    current_date = datetime.now()
    return render_template('resellers/monthly_sales.html', 
                         reseller=reseller, 
                         products=products,
                         current_month=current_date.month,
                         current_year=current_date.year)

@resellers_bp.route('/api/resellers')
@login_required
def api_index():
    resellers = Reseller.query.all()
    return jsonify([reseller.to_dict() for reseller in resellers])

@resellers_bp.route('/api/resellers/<int:id>')
@login_required
def api_show(id):
    reseller = Reseller.query.get_or_404(id)
    return jsonify(reseller.to_dict())

@resellers_bp.route('/resellers/<int:id>/orders/<int:order_id>/update_status', methods=['POST'])
@login_required
def update_order_status(id, order_id):
    reseller = Reseller.query.get_or_404(id)
    order = Order.query.get_or_404(order_id)
    
    if order.reseller_id != reseller.id:
        flash('Pedido não pertence a este revendedor.', 'danger')
        return redirect(url_for('resellers.show', id=id))
    
    new_status = request.form.get('status')
    if new_status not in ['pending', 'approved', 'delivered', 'cancelled']:
        flash('Status inválido.', 'danger')
        return redirect(url_for('resellers.show', id=id))
    
    # Se o pedido está sendo marcado como entregue, atualiza o estoque
    if new_status == 'delivered' and order.status != 'delivered':
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
        
        # Atualiza o estoque
        for product, quantity, price in products:
            # Verifica se o produto já está no estoque
            inventory = db.session.query(order_products).filter(
                order_products.c.product_id == product.id,
                order_products.c.order_id.in_(
                    db.session.query(Order.id).filter(
                        Order.reseller_id == reseller.id,
                        Order.status == 'delivered'
                    )
                )
            ).first()
            
            if inventory:
                # Atualiza a quantidade
                db.session.execute(
                    order_products.update().where(
                        order_products.c.product_id == product.id,
                        order_products.c.order_id == inventory.order_id
                    ).values(quantity=inventory.quantity + quantity)
                )
            else:
                # Cria um novo pedido para o estoque
                inventory_order = Order(
                    reseller_id=reseller.id,
                    status='delivered',
                    total_price=0
                )
                db.session.add(inventory_order)
                db.session.flush()  # Gera o ID do pedido
                
                # Adiciona o produto ao estoque
                db.session.execute(
                    order_products.insert().values(
                        product_id=product.id,
                        order_id=inventory_order.id,
                        quantity=quantity,
                        price_at_time=price
                    )
                )
    
    order.status = new_status
    db.session.commit()
    
    flash('Status do pedido atualizado com sucesso!', 'success')
    return redirect(url_for('resellers.show', id=id))

@resellers_bp.route('/resellers/<int:id>/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(id, order_id):
    reseller = Reseller.query.get_or_404(id)
    order = Order.query.get_or_404(order_id)
    
    if order.reseller_id != reseller.id:
        flash('Pedido não pertence a este revendedor.', 'danger')
        return redirect(url_for('resellers.show', id=id))
    
    try:
        # Remove os produtos do pedido
        db.session.execute(order_products.delete().where(order_products.c.order_id == order.id))
        # Remove o pedido
        db.session.delete(order)
        db.session.commit()
        flash('Pedido excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir pedido.', 'danger')
    
    return redirect(url_for('resellers.show', id=id))

@resellers_bp.route('/resellers/<int:id>/sales/<int:sale_id>/delete', methods=['POST'])
@login_required
def delete_sale(id, sale_id):
    reseller = Reseller.query.get_or_404(id)
    sale = Sale.query.get_or_404(sale_id)
    
    if sale.reseller_id != reseller.id:
        flash('Venda não pertence a este revendedor.', 'danger')
        return redirect(url_for('resellers.show', id=id))
    
    try:
        # Remove os produtos da venda
        db.session.execute(sale_products.delete().where(sale_products.c.sale_id == sale.id))
        # Remove a venda
        db.session.delete(sale)
        db.session.commit()
        flash('Venda excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir venda.', 'danger')
    
    return redirect(url_for('resellers.show', id=id))

@resellers_bp.route('/resellers/<int:id>/orders/delete', methods=['POST'])
@login_required
def delete_orders(id):
    reseller = Reseller.query.get_or_404(id)
    order_ids = request.form.get('order_ids')
    
    if not order_ids:
        flash('Nenhum pedido selecionado.', 'warning')
        return redirect(url_for('resellers.show', id=id))
    
    try:
        order_ids = json.loads(order_ids)
        orders = Order.query.filter(
            Order.id.in_(order_ids),
            Order.reseller_id == reseller.id
        ).all()
        
        for order in orders:
            # Remove os produtos do pedido
            db.session.execute(order_products.delete().where(order_products.c.order_id == order.id))
            # Remove o pedido
            db.session.delete(order)
        
        db.session.commit()
        flash(f'{len(orders)} pedido(s) excluído(s) com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir pedidos.', 'danger')
    
    return redirect(url_for('resellers.show', id=id))

@resellers_bp.route('/resellers/<int:id>/sales/delete', methods=['POST'])
@login_required
def delete_sales(id):
    reseller = Reseller.query.get_or_404(id)
    sale_ids = request.form.get('sale_ids')
    
    if not sale_ids:
        flash('Nenhuma venda selecionada.', 'warning')
        return redirect(url_for('resellers.show', id=id))
    
    try:
        sale_ids = json.loads(sale_ids)
        sales = Sale.query.filter(
            Sale.id.in_(sale_ids),
            Sale.reseller_id == reseller.id
        ).all()
        
        for sale in sales:
            # Remove os produtos da venda
            db.session.execute(sale_products.delete().where(sale_products.c.sale_id == sale.id))
            # Remove a venda
            db.session.delete(sale)
        
        db.session.commit()
        flash(f'{len(sales)} venda(s) excluída(s) com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir vendas.', 'danger')
    
    return redirect(url_for('resellers.show', id=id)) 