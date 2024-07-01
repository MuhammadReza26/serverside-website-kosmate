from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, DetailKos, User
from serializers import Serializer

bp = Blueprint('detail_kos_routes', __name__)

@bp.route('/', methods=['GET'])
def get_detail_kos():
    kos_list = DetailKos.query.all()
    return jsonify([Serializer.serialize_detail_kos(kos) for kos in kos_list])

@bp.route('/<int:id>', methods=['GET'])
def get_kos(id):
    kos = DetailKos.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404
    return jsonify(Serializer.serialize_detail_kos(kos))

@bp.route('/by_pengelola/<int:id_pengelola_kos>', methods=['GET'])
@jwt_required()
def get_kos_by_pengelola(id_pengelola_kos):
    kos_list = DetailKos.query.filter_by(id_pengelola_kos=id_pengelola_kos).all()
    return jsonify([Serializer.serialize_detail_kos(kos) for kos in kos_list])


@bp.route('/add', methods=['POST'])
@jwt_required()
def create_kos():
    data = request.get_json()
    
    # Ensure data is not empty
    if not data:
        print("No data provided")
        return jsonify({'message': 'No data provided'}), 400

    # Get user_id from JWT token
    user_identity = get_jwt_identity()
    user_id = user_identity['id']
    print(f"Received user_id from JWT: {user_id}")

    # Check if the user making the request is a manager
    user = User.query.get(user_id)
    if user is None:
        print(f"User with id {user_id} not found.")
        return jsonify({'message': 'User not found'}), 404
    print(f"Queried user: {user}")

    # Create DetailKos if the user is a manager
    kos_data = {
        'id_pengelola_kos': user_id,
        'kos_name': data.get('kos_name'),
        'kos_type': data.get('kos_type'),
        'room_size': data.get('room_size'),
        'price': data.get('price'),
        'address': data.get('address'),
        'shared_facilities': data.get('shared_facilities'),
        'room_facilities': data.get('room_facilities'),
        'available_room': data.get('available_room')
    }
    
    try:
        kos = DetailKos(**kos_data)
        db.session.add(kos)
        db.session.commit()
        print(f"DetailKos created: {kos}")
        return jsonify(Serializer.serialize_detail_kos(kos)), 201
    except Exception as e:
        print(f"Error creating kos: {e}")
        return jsonify({'message': 'Error creating kos', 'error': str(e)}), 500

@bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_kos(id):
    data = request.get_json()
    
    # Get user_id from JWT token
    user_identity = get_jwt_identity()
    user_id = user_identity['id']
    print(f"Received user_id from JWT: {user_id}")

    kos = DetailKos.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404

    for key, value in data.items():
        setattr(kos, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_detail_kos(kos))

@bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_kos(id):
    
    # Get user_id from JWT token
    user_identity = get_jwt_identity()
    user_id = user_identity['id']
    print(f"Received user_id from JWT: {user_id}")

    kos = DetailKos.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404
    
    db.session.delete(kos)
    db.session.commit()
    return jsonify({'message': 'Kos deleted'}), 200
