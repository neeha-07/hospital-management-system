import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hospital-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:neeha%402004@localhost/hospital_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-hospital')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload