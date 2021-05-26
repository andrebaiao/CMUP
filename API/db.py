from models import db, User, Patient, Pill
from utils import Day, PartOfDay
from werkzeug.security import generate_password_hash

# Create Tables
db.drop_all()
db.create_all()

# Create a User
user_1 = User(username='medic1', password=generate_password_hash('medic1', method='sha256'))

db.session.add(user_1)
db.session.commit()

# Create a user
user_id = User.query.filter_by(username='medic1').first().id
patient_1 = Patient(name='Luis', age=22, user_id=user_id)

db.session.add(patient_1)
db.session.commit()

# Create pills
patient_id = Patient.query.get(1).id
pill_1 = Pill(name='Isotretinoin', quantity=1, day=Day.MON, part_of_day=PartOfDay.DIN, patient_id=patient_id)
pill_2 = Pill(name='Isotretinoin', quantity=1, day=Day.WED, part_of_day=PartOfDay.DIN, patient_id=patient_id)
pill_3 = Pill(name='Isotretinoin', quantity=1, day=Day.FRI, part_of_day=PartOfDay.DIN, patient_id=patient_id)

db.session.add(pill_1)
db.session.add(pill_2)
db.session.add(pill_3)
db.session.commit()
