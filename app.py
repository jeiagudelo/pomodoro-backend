from flask import Flask
from config import Config
from extensions import db

# Crear app y configurar
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Importar modelos después de inicializar db
from models.task import Task
from models.session import Session
from routes.task import task_bp
from routes.session import session_bp

app.register_blueprint(session_bp)
app.register_blueprint(task_bp)


# Crear base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
