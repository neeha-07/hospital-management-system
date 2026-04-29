from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'doctor', 'patient'), nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat()
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    specialization = db.Column(db.Enum('Cardiology','Neurology','Gynecology','Pediatrics','Dermatology'), nullable=False)
    qualification = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    consultation_fee = db.Column(db.Numeric(10, 2))
    available_days = db.Column(db.String(100))
    available_timing = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'specialization': self.specialization,
            'qualification': self.qualification,
            'experience': self.experience,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else 0,
            'available_days': self.available_days,
            'available_timing': self.available_timing,
            'is_active': self.is_active
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    blood_group = db.Column(db.Enum('A+','A-','B+','B-','AB+','AB-','O+','O-'))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    document_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'age': self.age,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'medical_history': self.medical_history
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50))
    status = db.Column(db.Enum('Scheduled','Completed','Cancelled','Rescheduled'), default='Scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient_name': self.patient.full_name if self.patient else '',
            'doctor_name': self.doctor.full_name if self.doctor else '',
            'specialization': self.doctor.specialization if self.doctor else '',
            'appointment_date': self.appointment_date.isoformat(),
            'time_slot': self.time_slot,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class Billing(db.Model):
    __tablename__ = 'billing'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medicine_name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    total_medicine_charges = db.Column(db.Numeric(10, 2), default=0)
    consultation_charges = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    payment_mode = db.Column(db.Enum('Cash','Card','UPI','Insurance'), default='Cash')
    payment_status = db.Column(db.Enum('Pending','Paid','Partial'), default='Pending')
    bill_date = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='bills')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.full_name if self.patient else '',
            'medicine_name': self.medicine_name,
            'quantity': self.quantity,
            'total_medicine_charges': float(self.total_medicine_charges) if self.total_medicine_charges else 0,
            'consultation_charges': float(self.consultation_charges) if self.consultation_charges else 0,
            'discount': float(self.discount) if self.discount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'payment_mode': self.payment_mode,
            'payment_status': self.payment_status,
            'bill_date': self.bill_date.isoformat()
        }