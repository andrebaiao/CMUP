from flask import Flask, request, Response, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from utils import SUCCESS, CREATED, ERROR, FORBIDDEN
from models import User, Patient, Pill

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SECRET-KEY'] = 'dca3f75a-3590-4da6-a9bc-5ace72ad3129'
db = SQLAlchemy(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'ERROR': 'Token is missing'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'ERROR': 'Invalid token!'})


@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    password = request.form.get('password')

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    status = Response(status=CREATED)
    response = "User created with success"

    return jsonify({"message": response, "status": status})


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Please check your login details and try again!", "status": FORBIDDEN})

    session['logged_in'] = True
    token = jwt.encode({
        username: user.username
    },
        app.config['SECRET-KEY']
    )

    return jsonify({"message": "Successfully logged in!", "token": token.decode('utf-8'), "status": SUCCESS})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session['logged_in'] = False
    return jsonify({"message": "Successfully logout!", "status": SUCCESS})


app.run(host='localhost', port=9000)
