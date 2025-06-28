from flask import Blueprint, request, jsonify
from src.service import create_doctor, get_doctors_df
from src.interface.api.schemas import DoctorIn
from pydantic import ValidationError

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    df = get_doctors_df()
    return jsonify(df.to_dict(orient='records'))

@doctor_bp.route('/doctors', methods=['POST'])
def post_doctor():
    try:
        data = DoctorIn(**request.json)
        create_doctor(data.dict())
        return jsonify({"message": "Doctor added successfully"}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
