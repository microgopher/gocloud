from run import db
from passlib.hash import pbkdf2_sha256 as sha256


class AppointmentModel(db.Model):
    __tablename__ = 'appointments'
   
    id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.String, nullable=False)
    patient_id = db.Column(db.String, nullable=False)
    probable_date = db.Column(db.DateTime, nullable=True)
    actual_start_date = db.Column(db.DateTime, nullable=False)
    actual_end_date = db.Column(db.DateTime, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    

class AvailabilityModel(db.Model):
    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.String, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time_hours = db.Column(db.Integer, nullable=False)
    start_time_mins = db.Column(db.Integer, nullable=False)
    end_time_hours = db.Column(db.Integer, nullable=False)
    end_time_mins = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    reason_of_unavailability = db.Column(db.String(256), nullable=True)
    