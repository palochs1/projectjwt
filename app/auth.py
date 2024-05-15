from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db
import random
import string


bp = Blueprint('auth', __name__)

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
    email = data.get('email')

    otp = ''.join(random.choices(string.digits, k=6))

    user = User(username=username, password=password, email=email, otp=otp)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered. OTP generated and stored."}), 201

@bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    username = data.get('username')
    user_input_otp = data.get('otp')

    # Query the database to get the user's stored OTP
    user = User.query.filter_by(username=username).first()
    if user:
        stored_otp = user.otp

        # Compare the OTP entered by the user with the stored OTP
        if user_input_otp == stored_otp:
            return jsonify({"msg": "OTP verified successfully."}), 200
        else:
            return jsonify({"msg": "Invalid OTP. Please try again."}), 400
    else:
        return jsonify({"msg": "User not found."}), 404