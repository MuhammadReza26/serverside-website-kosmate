# init_db.py
from flask import Flask
from config import Config
from models import db, User  # Pastikan mengimpor model yang diperlukan

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Database has been created!")

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)
