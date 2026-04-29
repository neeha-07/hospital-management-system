from flask import Blueprint, request, jsonify
from database import db, User, Doctor, Patient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
import secrets

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-hospital')

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(email=email, role=role).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = generate_token(user.id, user.role)

    # Get profile id
    profile_id = None
    if role == 'doctor':
        doc = Doctor.query.filter_by(user_id=user.id).first()
        profile_id = doc.id if doc else None
    elif role == 'patient':
        pat = Patient.query.filter_by(user_id=user.id).first()
        profile_id = pat.id if pat else None

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role,
            'profile_id': profile_id
        }
    })

@auth_bp.route('/register/patient', methods=['POST'])
def register_patient():
    data = request.get_json()
    email = data.get('email')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = generate_password_hash(data['password'])
    user = User(
        full_name=data['full_name'],
        email=email,
        password_hash=hashed_pw,
        role='patient',
        phone_number=data.get('phone_number')
    )
    db.session.add(user)
    db.session.flush()

    patient = Patient(
        user_id=user.id,
        full_name=data['full_name'],
        email=email,
        phone_number=data.get('phone_number'),
        gender=data.get('gender'),
        date_of_birth=data.get('date_of_birth'),
        address=data.get('address')
    )
    db.session.add(patient)
    db.session.commit()

    token = generate_token(user.id, 'patient')
    return jsonify({'message': 'Patient registered successfully', 'token': token, 'user': user.to_dict()}), 201

@auth_bp.route('/register/doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()
    email = data.get('email')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = generate_password_hash(data.get('password', 'doctor123'))
    user = User(
        full_name=data['full_name'],
        email=email,
        password_hash=hashed_pw,
        role='doctor',
        phone_number=data.get('phone_number')
    )
    db.session.add(user)
    db.session.flush()

    doctor = Doctor(
        user_id=user.id,
        full_name=data['full_name'],
        email=email,
        phone_number=data.get('phone_number'),
        specialization=data['specialization'],
        qualification=data.get('qualification'),
        experience=data.get('experience'),
        consultation_fee=data.get('consultation_fee'),
        available_days=data.get('available_days'),
        available_timing=data.get('available_timing')
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor registered successfully'}), 201

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email not found'}), 404

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    db.session.commit()

    # In production, send email with reset link
    return jsonify({'message': 'Password reset link sent to your email', 'reset_token': token})

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.datetime.utcnow():
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'})