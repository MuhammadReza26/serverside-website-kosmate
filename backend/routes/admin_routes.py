from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Admin
from serializers import Serializer

bp = Blueprint('admin_routes', __name__)


@bp.route('/', methods=['GET'])
@jwt_required()
def get_admins():
    admins = Admin.query.all()
    return jsonify([Serializer.serialize_admin(admin) for admin in admins])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_admin(id):
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    return jsonify(Serializer.serialize_admin(admin))

@bp.route('/add', methods=['POST'])
@jwt_required()
def create_admin():
    data = request.get_json()
    admin = Admin(**data)
    db.session.add(admin)
    db.session.commit()
    return jsonify(Serializer.serialize_admin(admin)), 201

@bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    for key, value in data.items():
        setattr(admin, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_admin(admin))

@bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_admin(id):
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'message': 'Admin deleted'}), 200
