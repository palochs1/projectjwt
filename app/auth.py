from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db
import random
import string
import smtplib
import redis
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import User
from . import db
  
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

        send_otp_email(user.email, user.otp)

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

    redis_client = current_app.redis_client
    redis_client.setex(f"otp:{username}", 300, otp)

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
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"msg": "Invalid OTP. Please try again."}), 400
    else:
        return jsonify({"msg": "User not found."}), 404
    
def send_otp_email(email, otp):
    # Email configuration for Gmail
    sender_email = "paloch54@gmail.com"
    sender_password = "bsgm nvgc xjzr erhe"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "OTP Verification"
    
    # Email body
    body = f"Your OTP for verification is: {otp}"
    msg.attach(MIMEText(body, 'plain'))
    
    # Establish a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    
    # Login to the SMTP server
    server.login(sender_email, sender_password)
    
    # Send the email
    server.sendmail(sender_email, email, msg.as_string())
    
    # Close the connection
    server.quit()

