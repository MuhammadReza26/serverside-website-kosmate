import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Kos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Ambil dari variabel lingkungan atau gunakan nilai default
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Ambil dari variabel lingkungan atau gunakan nilai default
