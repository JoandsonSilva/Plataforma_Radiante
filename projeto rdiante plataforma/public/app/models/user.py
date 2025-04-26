from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)  # Permitir nulo inicialmente
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, reseller, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relacionamentos simplificados
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    products = db.relationship('Product', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_display_name(self):
        return self.username or self.email
    
    def __repr__(self):
        return f'<User {self.get_display_name()}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 