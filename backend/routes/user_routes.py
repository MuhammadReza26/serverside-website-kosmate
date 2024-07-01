# routes/user_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import User, db
from serializers import Serializer

bp = Blueprint('user_routes', __name__)

@bp.route('/', methods=['GET'])
# @jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([Serializer.serialize_user(user) for user in users])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(Serializer.serialize_user(user))

@bp.route('/add', methods=['POST'])
@jwt_required()
def create_user():
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

@bp.route('/update/<int:id>', methods=['PUT'])
# @jwt_required()
def update_user(id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    user.phone = data.get('phone')
    user.password = data.get('password')
    db.session.commit()
    return jsonify(Serializer.serialize_user(user)), 200

@bp.route('/delete/<int:id>', methods=['DELETE'])
# @jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
