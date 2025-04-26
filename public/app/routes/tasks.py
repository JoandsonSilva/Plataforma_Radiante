from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.task import Task
from app.models.user import User
from app import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
@login_required
def index():
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('tasks/index.html', tasks=tasks, users=users)

@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        user_id = request.form.get('assigned_to')
        completed = request.form.get('completed') == 'on'
        
        # Se user_id for vazio, define como None
        user_id = int(user_id) if user_id else None
        
        task = Task(
            title=title,
            description=description,
            due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
            priority=priority,
            user_id=user_id,
            status='todo'  # Status padrão para novas tarefas
        )
        
        db.session.add(task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tasks.index'))
    
    users = User.query.all()
    return render_template('tasks/create.html', users=users)

@tasks_bp.route('/tasks/<int:id>')
@login_required
def show(id):
    task = Task.query.get_or_404(id)
    return render_template('tasks/show.html', task=task)

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status')
        
        # Tratamento da data de vencimento
        due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        
        # Tratamento do usuário atribuído
        user_id = request.form.get('assigned_to')
        task.user_id = int(user_id) if user_id else None
        
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('tasks.show', id=task.id))
    
    users = User.query.all()
    return render_template('tasks/edit.html', task=task, users=users)

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    
    flash('Tarefa removida com sucesso!', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    task = Task.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['todo', 'in_progress', 'done']:
        task.status = new_status
        db.session.commit()
        
        return jsonify({'success': True, 'status': new_status})
    
    return jsonify({'success': False, 'error': 'Status inválido'})

@tasks_bp.route('/api/tasks')
@login_required
def api_index():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/api/tasks/<int:id>')
@login_required
def api_show(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict()) 