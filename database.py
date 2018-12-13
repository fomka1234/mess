
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(80), unique=False, nullable=False)
    parent_id = db.Column(db.Integer(), unique=False, nullable=True)

    def __repr__(self):
        return self.as_dict().__repr__()

    def as_dict(self):
        return { 'id': self.id,
                 'text': self.text,
                 'parent_id': self.parent_id }