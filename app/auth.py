from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db

bp = Blueprint('auth', __name__,url_prefix="/auth")

@bp.route('/', methods=['POST'])
def login():
    print("THIS IS TEST")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/register', methods=['POST'])
def register():
    print("TEST TEST")
    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered"}), 201