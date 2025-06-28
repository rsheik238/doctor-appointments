from flask import Blueprint, request, jsonify
from src.service import create_patient, get_patients_df
from src.interface.api.schemas import PatientIn
from pydantic import ValidationError

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    df = get_patients_df()
    return jsonify(df.to_dict(orient='records'))

@patient_bp.route('/patients', methods=['POST'])
def post_patient():
    try:
        data = PatientIn(**request.json)
        create_patient(data.dict())
        return jsonify({"message": "Patient added successfully"}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
