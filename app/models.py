from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    otp = db.Column(db.String(50), nullable=True)
    token = db.Column(db.String(200), nullable=True)

def create_table():
    db.create_all()