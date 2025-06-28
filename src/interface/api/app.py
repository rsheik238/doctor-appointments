from flask import Flask
from src.interface.api.routes.doctor_routes import doctor_bp
from src.interface.api.routes.patient_routes import patient_bp
from src.interface.api.routes.appointment_routes import appointment_bp
from src.data import init_db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)
    return app

app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
