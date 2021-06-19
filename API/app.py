from flask import Flask, request, Response, session, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from flask_cors import CORS, cross_origin
from utils import SUCCESS, CREATED, ERROR, FORBIDDEN, AlchemyEncoder, Day, PartOfDay, convertHourToPartOfDay
from models import User, Patient, Pill, TakingPills
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SECRET_KEY'] = 'dca3f75a-3590-4da6-a9bc-5ace72ad3129'
cors = CORS(app)
db = SQLAlchemy(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'ERROR': 'Token is missing', "status": FORBIDDEN})
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({'ERROR': 'Invalid token!', "status": FORBIDDEN})
        return func(*args, **kwargs)

    return decorated


@app.route('/signup', methods=['POST'])
@cross_origin()
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
@cross_origin()
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
    print(session)
    return jsonify({"message": "Successfully logged in!", "user_id": user.id ,"token": token, "status": SUCCESS})


@app.route('/logout')
@cross_origin()
@token_required
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({"message": "Successfully logout!", "status": SUCCESS})


@app.route('/patients/medic/<medic_id>', methods=['GET'])
@cross_origin()
@token_required
def patients_get(medic_id):
    
    #user_id = session['user_id']
    user = User.query.filter_by(id=medic_id).first()

    # TODO: clean the fields
    patients = json.dumps(user.patients, cls=AlchemyEncoder)
    
    return jsonify({"message": patients, "status": SUCCESS})


@app.route('/patients/<patient_id>', methods=['GET'])
@token_required
@cross_origin()
def patient_pill(patient_id):
    
    name_patient = Patient.query.filter_by(id=patient_id).first().name

    pills_to_take = Pill.query.filter_by(patient_id=patient_id).all()

    pills = []

    for pill in pills_to_take:
        pills.append({"id": pill.id, "name": pill.name, "quantity": pill.quantity, \
                        "day": Day(pill.day).value, "part_of_day": PartOfDay(pill.part_of_day).value})

    pills_took = TakingPills.query.filter_by(patient_id=patient_id).all()
    total_pills_took = 0
    pills_not_took = []
    
    for pill in pills_took:
        if pill.take:
            total_pills_took += 1
        else:
            pills_not_took.append({"patient_id" : pill.patient_id, "date": pill.date.strftime("%d %B %Y %A %H:%M:%S")})

    pills = json.dumps(pills, cls=AlchemyEncoder)
    pills_not_took = json.dumps(pills_not_took, cls=AlchemyEncoder)

    return jsonify({"message": { "treatment": pills, "total_pills_took": total_pills_took, "pills_not_took": pills_not_took, "name": name_patient }, "status": SUCCESS})


# TODO: pode ser passado para um função, para se usar na função cronjob
@app.route('/patients/nextpill/<patient_id>', methods=['GET'])
@cross_origin()
def next_pill(patient_id):

    pills_to_take = Pill.query.filter_by(patient_id=patient_id).all()
    #print(last_took_pill)
    pills_to_take = sorted(pills_to_take, key=lambda d: (d.day, d.part_of_day))
    #print(pills_to_take)



    pills_took = TakingPills.query.filter_by(patient_id=patient_id).all()

    print(pills_took)
    print(type(pills_took))

    if len(pills_took) == 0:
        index = -1
    else:
        last_took_pill = pills_took[-1]

        index = 0
        for pill in pills_to_take:
            if pill.day == last_took_pill.day and pill.part_of_day and last_took_pill.part_of_day:
                break
            index += 1

        # if last_took_pill was the last pill in the week
        if (index + 1) == len(pills_to_take):
            index = - 1

    #print(pills_to_take[index + 1])
    pills_to_take = {"id": pills_to_take[index + 1].id, "name": pills_to_take[index + 1].name, "quantity": pills_to_take[index + 1].quantity, \
                        "day": Day(pills_to_take[index + 1].day).value, "part_of_day": PartOfDay(pills_to_take[index + 1].part_of_day).value}

    pills_to_take = json.dumps(pills_to_take, cls=AlchemyEncoder)

    return jsonify({"message": pills_to_take, "status": SUCCESS})


@app.route('/new_patient', methods=['POST'])
@token_required
@cross_origin()
def create_new_treatment():

    body_data = request.get_json()
    name = body_data['name']
    age = body_data['age']
    medic_id = body_data['user_id']
    pills = body_data['pills']

    # create patient
    new_patient = Patient(name=name, age=age, user_id=medic_id)

    db.session.add(new_patient)
    db.session.commit()

    # add his pills
    patient_id = Patient.query.order_by(Patient.id.desc()).first().id
    
    for pill in pills:
        pill["day"] = Day(pill["day"])
        pill["part_of_day"] = PartOfDay(pill["part_of_day"])
        new_pill = Pill(name=pill["name"], quantity=pill["quantity"], \
                        day=pill["day"], part_of_day=pill["part_of_day"], \
                        patient_id=patient_id)

        db.session.add(new_pill)

    db.session.commit()

    return jsonify({"message": "New patient added with success", "status": SUCCESS})


@app.route('/takepill', methods=['POST'])
@cross_origin()
def takepill():

    body_data = request.form
    patient_id = body_data["patient_id"]
    day = Day( int(body_data["day"]) )
    hour = int(body_data["hour"])
    minu = int(body_data["minu"])
    take = body_data["take"]
    
    date_today = datetime.date.today()
    time_took_pill = datetime.datetime(date_today.year, date_today.month, date_today.day,
										hour, minu, 0, 62371)

    part_of_day = convertHourToPartOfDay(time_took_pill)

    taking_pill = TakingPills(patient_id=patient_id, date=time_took_pill, part_of_day=part_of_day, day=day)
    
    db.session.add(taking_pill)
    db.session.commit()

    return jsonify({"message": " Take Pill Record with success!", "status": SUCCESS})

app.run(host='localhost', port=9000)



