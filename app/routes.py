from flask import Flask, app, jsonify, render_template, Blueprint
import redis

bp = Blueprint('routes', __name__)
redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)

@bp.route('/')
def login():
    return render_template('base.html')

@bp.route('/register')
def register():
    return render_template('regis.html')

@bp.route('/redis-keys', methods=['GET'])
def get_redis_keys():
    keys = redis_client.keys('*')
    values = {key: redis_client.get(key) for key in keys}
    return jsonify(values)

if __name__ == "__main":
    app.run(debug=True)
