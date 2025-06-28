from flask import Blueprint, request, jsonify
from src.service import create_appointment, get_appointments_df
from src.interface.api.schemas import AppointmentIn
from pydantic import ValidationError

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/appointments', methods=['GET'])
def get_appointments():
    df = get_appointments_df()
    return jsonify(df.to_dict(orient='records'))

@appointment_bp.route('/appointments', methods=['POST'])
def post_appointment():
    try:
        data = AppointmentIn(**request.json)
        create_appointment(data.dict())
        return jsonify({"message": "Appointment added successfully"}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
