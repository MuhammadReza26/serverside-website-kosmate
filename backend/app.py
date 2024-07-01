from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from init_db import init_db
from routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi JWT
    jwt = JWTManager(app)

    # Inisialisasi database
    init_db(app)

    # Register blueprint
    app.register_blueprint(routes_bp)

    return app
