from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis import Redis
from flask_migrate import Migrate
from config import Config
import redis

db = SQLAlchemy()
jwt = JWTManager()
redis_client = Redis.from_url(Config.REDIS_URL)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    from app import models

    with app.app_context():  # สร้าง Application Context
        models.create_table()  # เรียกใช้งานเพื่อสร้างตาราง

    jwt.init_app(app)
    migrate = Migrate(app, db)

    app.redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'], decode_responses=True)

    from app import routes, auth
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)

    return app

from app import models