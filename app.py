from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
from routes.auth import auth_bp
from routes.doctors import doctors_bp
from routes.patients import patients_bp
from routes.appointments import appointments_bp
from routes.billing import billing_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
app.register_blueprint(patients_bp, url_prefix='/api/patients')
app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
app.register_blueprint(billing_bp, url_prefix='/api/billing')

@app.route('/api/health')
def health():
    return {'status': 'ok', 'message': 'Hospital API running'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)