from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    def __repr__(self):
        return f'<User {self.email}>'

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Item {self.name}>'

