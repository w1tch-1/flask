from flask_sqlalchemy import SQLAlchemy
from __init__ import app

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
