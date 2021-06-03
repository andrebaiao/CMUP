from models import db, User, Patient, Pill, TakingPills
from utils import Day, PartOfDay, convertHourToPartOfDay, getDayOnWeek
from werkzeug.security import generate_password_hash
import datetime

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
pill_4 = Pill(name='Isotretinoin', quantity=1, day=Day.FRI, part_of_day=PartOfDay.NIG, patient_id=patient_id)
pill_3 = Pill(name='Isotretinoin', quantity=1, day=Day.FRI, part_of_day=PartOfDay.DIN, patient_id=patient_id)

db.session.add(pill_1)
db.session.add(pill_2)
db.session.add(pill_3)
db.session.add(pill_4)
db.session.commit()

datetime1 = datetime.datetime(2021, 5, 31, 21, 33, 30, 62371)
part_of_day_1 = convertHourToPartOfDay(datetime1)
day_1 = getDayOnWeek(datetime1)
takingPill_1 = TakingPills(patient_id=patient_id, date=datetime1, part_of_day=part_of_day_1, day=day_1)

datetime2 = datetime.datetime(2021, 6, 2, 21, 33, 30, 62371)
part_of_day_2 = convertHourToPartOfDay(datetime2)
day_2 = getDayOnWeek(datetime2)
takingPill_2 = TakingPills(patient_id=patient_id, date=datetime2, part_of_day=part_of_day_2, day=day_2)

db.session.add(takingPill_1)
db.session.add(takingPill_2)
db.session.commit()
