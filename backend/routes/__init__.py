# routes/__init__.py

from flask import Blueprint
from .admin_routes import bp as admin_bp
from .detail_kos_routes import bp as detail_kos_bp
from .gallery_routes import bp as gallery_bp
from .review_routes import bp as review_bp
from .user_routes import bp as user_bp
from .auth_routes import bp as auth_bp
bp = Blueprint('api', __name__)

# Register Blueprints
bp.register_blueprint(admin_bp, url_prefix='/api/admins')
bp.register_blueprint(detail_kos_bp, url_prefix='/api/detail_kos')
bp.register_blueprint(gallery_bp, url_prefix='/api/galleries')
bp.register_blueprint(review_bp, url_prefix='/api/reviews')
bp.register_blueprint(user_bp, url_prefix='/api/users')
bp.register_blueprint(auth_bp, url_prefix='/auth')
