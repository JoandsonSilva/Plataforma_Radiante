from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/produtos')
@login_required
def produtos():
    from app.models.product import Product
    products = Product.query.all()
    return render_template('main/produtos.html', products=products)

@main_bp.route('/revendedores')
@login_required
def revendedores():
    from app.models.reseller import Reseller
    resellers = Reseller.query.all()
    return render_template('main/revendedores.html', resellers=resellers)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    from app.models.product import Product
    from app.models.reseller import Reseller
    from app.models.task import Task
    from app.models.sale import Sale

    # Total de produtos
    total_products = Product.query.count()
    
    # Total de revendedores
    total_resellers = Reseller.query.count()
    
    # Tarefas pendentes
    pending_tasks = Task.query.filter_by(status='pending').count()
    
    # Vendas do mês
    first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales = db.session.query(db.func.sum(Sale.amount)).filter(
        Sale.sale_date >= first_day_of_month
    ).scalar() or 0
    
    # Últimas tarefas
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    
    # Últimos produtos
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
        total_products=total_products,
        total_resellers=total_resellers,
        pending_tasks=pending_tasks,
        monthly_sales=monthly_sales,
        recent_tasks=recent_tasks,
        recent_products=recent_products
    ) 