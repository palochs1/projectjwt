from flask import Flask, render_template, Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/')
def login():
    return render_template('base.html')

@bp.route('/register')
def register():
    return render_template('regis.html')

if __name__ == "__main":
    app.run(debug=True)
