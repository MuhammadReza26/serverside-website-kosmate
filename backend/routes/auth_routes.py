from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import User, Admin, db
from serializers import Serializer

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:  # Perbandingan password langsung
        access_token = create_access_token(identity={'id': user.id, 'email': user.email})
        return jsonify(access_token=access_token, user_id = user.id), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401

@bp.route('/loginAdmin', methods=['POST'])
def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.password == password:  # Perbandingan password langsung
        access_token = create_access_token(identity={ 'email': admin.email, 'role': 'admin'})
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid admin credentials"}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    

    new_user = User()
    new_user.first_name = data.get('first_name')
    new_user.last_name = data.get('last_name')
    new_user.email = data.get('email')
    new_user.phone = data.get('phone')
    new_user.password = data.get('password')
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(Serializer.serialize_user(new_user)), 201
