from flask import Blueprint, request, jsonify
from models.task import Task
from extensions import db

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'El título es obligatorio'}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat()
    }), 201

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'created_at': t.created_at.isoformat()
        } for t in tasks
    ])

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat()
    })

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat()
    })
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada correctamente'})
