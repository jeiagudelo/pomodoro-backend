from flask import Blueprint, request, jsonify
from extensions import db
from models.session import Session
from datetime import datetime

session_bp = Blueprint('session_bp', __name__)

# Crear una sesión
@session_bp.route('/tasks/<int:task_id>/sessions', methods=['POST'])
def create_session(task_id):
    data = request.get_json()
    session_type = data.get('type')
    end_time = data.get('end_time')  # formato ISO: '2025-04-09T15:00:00'

    valid_types = ['trabajo', 'descanso', 'lectura', 'entrenamiento']
    if session_type not in valid_types:
        return jsonify({'error': f'Tipo inválido. Usa: {", ".join(valid_types)}'}), 400

    session = Session(
        task_id=task_id,
        type=session_type,
        end_time=datetime.fromisoformat(end_time) if end_time else None
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({
        'id': session.id,
        'task_id': session.task_id,
        'type': session.type,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'completed': session.completed
    }), 201


# Obtener historial de sesiones
@session_bp.route("/sessions/history", methods=["GET"])
def get_history():
    sessions = Session.query.order_by(Session.start_time.desc()).all()
    result = []
    for s in sessions:
        result.append({
            "task_id": s.task_id,
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat() if s.end_time else None,
            "duration": (s.end_time - s.start_time).seconds // 60 if s.end_time else None,
            "type": s.type
        })
    return jsonify(result)


@session_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)

    if not session:
        return jsonify({'error': 'Sesión no encontrada'}), 404

    db.session.delete(session)
    db.session.commit()

    return jsonify({'message': 'Sesión eliminada correctamente'})

@session_bp.route('/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Sesión no encontrada'}), 404

    data = request.get_json()

    # Actualizar campos si vienen en la solicitud
    if 'end_time' in data:
        session.end_time = datetime.fromisoformat(data['end_time'])

    if 'type' in data:
        valid_types = ['trabajo', 'descanso', 'lectura', 'entrenamiento']
        if data['type'] not in valid_types:
            return jsonify({'error': f'Tipo inválido. Usa: {", ".join(valid_types)}'}), 400
        session.type = data['type']

    if 'completed' in data:
        session.completed = data['completed']

    db.session.commit()

    return jsonify({
        'id': session.id,
        'task_id': session.task_id,
        'type': session.type,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'completed': session.completed
    })
