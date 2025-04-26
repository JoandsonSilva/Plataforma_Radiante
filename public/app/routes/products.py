from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.product import Product
from app import db
import os
from werkzeug.utils import secure_filename

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
@login_required
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)

@products_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category = request.form.get('category')
        brand = request.form.get('brand')
        
        # Upload da imagem
        image = request.files.get('image')
        image_url = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename=f'uploads/{filename}')
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            brand=brand,
            image_url=image_url,
            creator_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('products.index'))
    
    return render_template('products/create.html')

@products_bp.route('/products/<int:id>')
@login_required
def show(id):
    product = Product.query.get_or_404(id)
    return render_template('products/show.html', product=product)

@products_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category = request.form.get('category')
        product.brand = request.form.get('brand')
        
        # Upload da nova imagem
        image = request.files.get('image')
        if image and image.filename:
            # Remover imagem antiga se existir
            if product.image_url:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                            os.path.basename(product.image_url))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Salvar nova imagem
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            product.image_url = url_for('static', filename=f'uploads/{filename}')
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products.show', id=product.id))
    
    return render_template('products/edit.html', product=product)

@products_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    
    # Remover imagem se existir
    if product.image_url:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                os.path.basename(product.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Produto removido com sucesso!', 'success')
    return redirect(url_for('products.index'))

@products_bp.route('/api/products')
@login_required
def api_index():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@products_bp.route('/api/products/<int:id>')
@login_required
def api_show(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()) 