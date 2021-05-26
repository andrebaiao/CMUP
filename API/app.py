from flask import Flask, request, Response, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from utils import SUCCESS, CREATED, ERROR
from models import User, Patient, Pill

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


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

    return {"message": response, "status": status}


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"message": "Please check your login details and try again!", "status": ERROR}

    session['username'] = username

    return {"message": "Successfully logged in!", "status": SUCCESS}


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return {"message": "Successfully logout!", "status": SUCCESS}


def user_logged_in(username):
    if username in session:
        return True
    return False


app.run(host='localhost', port=9000)
