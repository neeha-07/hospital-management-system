from flask import Blueprint, request, jsonify
from database import db, Doctor
from middleware import token_required

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/', methods=['GET'])
def get_doctors():
    search = request.args.get('search', '')
    specialization = request.args.get('specialization', '')

    query = Doctor.query.filter_by(is_active=True)
    if search:
        query = query.filter(Doctor.full_name.ilike(f'%{search}%'))
    if specialization:
        query = query.filter_by(specialization=specialization)

    doctors = query.all()
    return jsonify([d.to_dict() for d in doctors])

@doctors_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.to_dict())

@doctors_bp.route('/<int:doctor_id>', methods=['PUT'])
@token_required
def update_doctor(current_user, doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()

    for field in ['full_name', 'phone_number', 'specialization', 'qualification',
                  'experience', 'consultation_fee', 'available_days', 'available_timing']:
        if field in data:
            setattr(doctor, field, data[field])

    db.session.commit()
    return jsonify(doctor.to_dict())

@doctors_bp.route('/<int:doctor_id>', methods=['DELETE'])
@token_required
def delete_doctor(current_user, doctor_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_active = False
    db.session.commit()
    return jsonify({'message': 'Doctor deactivated'})

@doctors_bp.route('/<int:doctor_id>/slots', methods=['GET'])
def get_doctor_slots(doctor_id):
    date = request.args.get('date')
    doctor = Doctor.query.get_or_404(doctor_id)

    # Generate time slots from doctor's available_timing
    timing = doctor.available_timing or '09:00-17:00'
    slots = []
    try:
        start, end = timing.split('-')
        sh, sm = map(int, start.strip().split(':'))
        eh, em = map(int, end.strip().split(':'))
        current = sh * 60 + sm
        end_min = eh * 60 + em
        while current + 30 <= end_min:
            h, m = divmod(current, 60)
            next_h, next_m = divmod(current + 30, 60)
            slots.append(f"{h:02d}:{m:02d} - {next_h:02d}:{next_m:02d}")
            current += 30
    except Exception:
        slots = ['09:00 - 09:30', '09:30 - 10:00', '10:00 - 10:30', '10:30 - 11:00',
                 '11:00 - 11:30', '14:00 - 14:30', '14:30 - 15:00', '15:00 - 15:30']

    return jsonify({'slots': slots, 'doctor': doctor.to_dict()})