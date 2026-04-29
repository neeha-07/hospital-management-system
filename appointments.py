from flask import Blueprint, request, jsonify

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify({"message": "Appointments route working"})