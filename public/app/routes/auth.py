from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.firebase_config import auth_firebase, verify_token, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            # Verificar se é um login com token do Firebase
            if request.is_json:
                data = request.get_json()
                token = data.get('token')
                
                if token:
                    # Verificar token do Firebase
                    user_info = verify_token(token)
                    print(f"Informações do usuário: {user_info}")  # Log para debug
                    
                    if not user_info:
                        return jsonify({'error': 'Token inválido'}), 401
                    
                    email = user_info.get('email')
                    if not email:
                        return jsonify({'error': 'Email não encontrado no token'}), 401
                    
                    # Verificar se o usuário existe no banco local
                    user = User.query.filter_by(email=email).first()
                    if not user:
                        # Criar usuário local se não existir
                        user = User(
                            email=email,
                            username=email.split('@')[0],  # Usar parte do email como username
                            role='user'
                        )
                        db.session.add(user)
                        db.session.commit()
                    
                    # Fazer login do usuário
                    login_user(user, remember=True)
                    return jsonify({
                        'success': True,
                        'redirect': url_for('main.dashboard')
                    })
            
            # Login tradicional com email/senha
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Por favor, preencha todos os campos.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Autenticar com Firebase
            user_firebase = auth_firebase.sign_in_with_email_and_password(email, password)
            
            # Verificar se o usuário existe no banco local
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Criar usuário local se não existir
                user = User(email=email)
                db.session.add(user)
                db.session.commit()
            
            # Fazer login do usuário
            login_user(user, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            print(f"Erro no login: {str(e)}")  # Log do erro para debug
            if request.is_json:
                return jsonify({'error': str(e)}), 401
            flash('Email ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        username = request.form.get('username')
        
        # Validações básicas
        if not all([email, password, confirm_password, username]):
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('auth.register'))
            
        if len(password) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            # Verificar se o email já existe no banco local
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Este email já está cadastrado.', 'danger')
                return redirect(url_for('auth.register'))
            
            # Criar usuário no Firebase
            user_firebase = auth_firebase.create_user_with_email_and_password(email, password)
            
            # Criar usuário local
            user = User(email=email, username=username)
            db.session.add(user)
            db.session.commit()
            
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            print(f"Erro no registro: {str(e)}")  # Log do erro para debug
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                flash('Este email já está cadastrado.', 'danger')
            elif "WEAK_PASSWORD" in error_message:
                flash('A senha é muito fraca. Use uma senha mais forte.', 'danger')
            elif "INVALID_EMAIL" in error_message:
                flash('Email inválido.', 'danger')
            else:
                flash('Erro ao criar conta. Tente novamente.', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/login/google', methods=['POST'])
def login_google():
    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'Token não fornecido'}), 400
    
    try:
        # Verificar token do Google
        decoded_token = verify_token(token)
        if not decoded_token:
            return jsonify({'error': 'Token inválido'}), 401
        
        email = decoded_token.get('email')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    if username:
        current_user.username = username
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
    return redirect(url_for('auth.profile'))

@auth_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([current_password, new_password, confirm_password]):
        flash('Todos os campos são obrigatórios.', 'danger')
        return redirect(url_for('auth.profile'))
    
    if new_password != confirm_password:
        flash('As senhas não coincidem.', 'danger')
        return redirect(url_for('auth.profile'))
    
    try:
        # Verificar senha atual
        auth_firebase.sign_in_with_email_and_password(current_user.email, current_password)
        
        # Atualizar senha no Firebase
        user = auth_firebase.get_user_by_email(current_user.email)
        auth_firebase.update_user(user['localId'], password=new_password)
        
        flash('Senha alterada com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao alterar senha. Verifique sua senha atual.', 'danger')
    
    return redirect(url_for('auth.profile')) 