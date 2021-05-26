from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils import Day, PartOfDay

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    patients = db.relationship('Patient', backref='User', lazy=True)

    def __repr__(self):
        return f"Users ({self.id}, {self.username}, {self.patients})"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    pills = db.relationship('Pill', backref='Pill', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Patients ({self.id}, {self.name}, {self.pills})"


class Pill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Enum(Day), nullable=False)
    part_of_day = db.Column(db.Enum(PartOfDay), nullable=False)  # BREAKFAST, LUNCH, DIN, NIGHT(BEFORE SLEEP)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return f"Pills ({self.id}, {self.name}, {self.day}, {self.part_of_day}, " \
               f"{self.quantity})"
