from flask import Blueprint, request, jsonify
from database import db, Patient
from middleware import token_required
import os

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['GET'])
@token_required
def get_patients(current_user):
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])

@patients_bp.route('/<int:patient_id>', methods=['GET'])
@token_required
def get_patient(current_user, patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())

@patients_bp.route('/<int:patient_id>', methods=['PUT'])
@token_required
def update_patient(current_user, patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()

    for field in ['full_name', 'phone_number', 'age', 'gender', 'blood_group',
                  'address', 'emergency_contact', 'medical_history']:
        if field in data:
            setattr(patient, field, data[field])

    db.session.commit()
    return jsonify(patient.to_dict())

@patients_bp.route('/register', methods=['POST'])
def register_patient_direct():
    data = request.get_json()
    from database import User
    from werkzeug.security import generate_password_hash

    email = data.get('email')
    if Patient.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    patient = Patient(
        full_name=data['full_name'],
        email=email,
        phone_number=data.get('phone_number'),
        age=data.get('age'),
        gender=data.get('gender'),
        blood_group=data.get('blood_group'),
        address=data.get('address'),
        emergency_contact=data.get('emergency_contact'),
        medical_history=data.get('medical_history')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201