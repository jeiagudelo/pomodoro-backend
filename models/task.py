from extensions import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con sesión (aquí agregamos el cascade)
    sessions = db.relationship('Session', backref='task', lazy=True, cascade="all, delete-orphan")
