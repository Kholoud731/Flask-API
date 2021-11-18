from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String( 250), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    completed = db.Column(db.Boolean , default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()  