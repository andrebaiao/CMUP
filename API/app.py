from flask import Flask, request, Response, session, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from utils import SUCCESS, CREATED, ERROR, FORBIDDEN, AlchemyEncoder, Day, PartOfDay
from models import User, Patient, Pill, TakingPills

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SECRET_KEY'] = 'dca3f75a-3590-4da6-a9bc-5ace72ad3129'
db = SQLAlchemy(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.get_json()['token']
        if not token:
            return jsonify({'ERROR': 'Token is missing', "status": FORBIDDEN})
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({'ERROR': 'Invalid token!', "status": FORBIDDEN})
        return func(*args, **kwargs)

    return decorated


@app.route('/signup', methods=['POST'])
def signup_post():
    body_data = request.get_json()
    username = body_data['username']
    password = body_data['password']

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    status = Response(status=CREATED)
    response = "User created with success"

    return jsonify({"message": response, "status": status})


@app.route('/login', methods=['POST'])
def login_post():
    body_data = request.get_json()
    username = body_data['username']
    password = body_data['password']

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Please check your login details and try again!", "status": FORBIDDEN})

    session['logged_in'] = True
    session['user_id'] = user.id

    token = jwt.encode({
        'username': user.username
    },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({"message": "Successfully logged in!", "token": token, "status": SUCCESS})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({"message": "Successfully logout!", "status": SUCCESS})


@app.route('/patients', methods=['POST'])
@token_required
def patients_get():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()

    # TODO: clean the fields
    patients = json.dumps(user.patients, cls=AlchemyEncoder)

    return jsonify({"message": patients, "status": SUCCESS})


# TODO: pode ser passado para um função, para se usar na função cronjob
@app.route('/patients/<user_id>', methods=['GET'])
def next_pill(user_id):

    last_took_pill = TakingPills.query.filter_by(patient_id=user_id)[-1]
    pills_to_take = Pill.query.filter_by(patient_id=user_id).all()
    print(last_took_pill)
    pills_to_take = sorted(pills_to_take, key=lambda d: (d.day, d.part_of_day))
    #print(pills_to_take)

    index = 0
    for pill in pills_to_take:
        if pill.day == last_took_pill.day and pill.part_of_day and last_took_pill.part_of_day:
            break
        index += 1

    # if last_took_pill was the last pill in the week
    if (index + 1) == len(pills_to_take):
        index = - 1

    print(pills_to_take[index + 1])
    return user_id


app.run(host='localhost', port=9000)



