from flask import Blueprint, request, jsonify
from database import db, Billing, Patient
from middleware import token_required

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/', methods=['GET'])
@token_required
def get_bills(current_user):
    bills = Billing.query.order_by(Billing.bill_date.desc()).all()
    return jsonify([b.to_dict() for b in bills])

@billing_bp.route('/<int:bill_id>', methods=['GET'])
@token_required
def get_bill(current_user, bill_id):
    bill = Billing.query.get_or_404(bill_id)
    return jsonify(bill.to_dict())

@billing_bp.route('/create', methods=['POST'])
@token_required
def create_bill(current_user):
    data = request.get_json()
    patient_id = data.get('patient_id')
    medicine_charges = float(data.get('total_medicine_charges', 0))
    consultation_charges = float(data.get('consultation_charges', 0))
    discount = float(data.get('discount', 0))
    total = medicine_charges + consultation_charges - discount

    bill = Billing(
        patient_id=patient_id,
        medicine_name=data.get('medicine_name'),
        quantity=data.get('quantity'),
        total_medicine_charges=medicine_charges,
        consultation_charges=consultation_charges,
        discount=discount,
        total_amount=total,
        payment_mode=data.get('payment_mode', 'Cash'),
        payment_status='Pending'
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify(bill.to_dict()), 201

@billing_bp.route('/<int:bill_id>/pay', methods=['PUT'])
@token_required
def confirm_payment(current_user, bill_id):
    bill = Billing.query.get_or_404(bill_id)
    data = request.get_json()
    bill.payment_status = 'Paid'
    bill.payment_mode = data.get('payment_mode', bill.payment_mode)
    db.session.commit()
    return jsonify(bill.to_dict())