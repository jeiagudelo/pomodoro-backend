from extensions import db

class PomodoroConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    work_sessions_completed = db.Column(db.Integer, default=0)
    long_break_after = db.Column(db.Integer, default=4)
    long_break_duration = db.Column(db.Integer, default=15)  # o 30

    def reset(self):
        self.work_sessions_completed = 0
