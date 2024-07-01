from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Gallery, User
from serializers import Serializer

bp = Blueprint('gallery_routes', __name__)

@bp.route('/', methods=['GET'])
def get_galleries():
    galleries = Gallery.query.all()
    return jsonify([Serializer.serialize_gallery(gallery) for gallery in galleries])

@bp.route('/<int:id>', methods=['GET'])
def get_gallery(id):
    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404
    return jsonify(Serializer.serialize_gallery(gallery))

@bp.route('/detail/<int:id_kos>', methods=['GET'])
def get_galleries_by_kos(id_kos):
    galleries = Gallery.query.filter_by(id_kos=id_kos).all()
    if not galleries:
        return jsonify({'message': 'Galleries not found for the given id_kos'}), 404
    return jsonify([Serializer.serialize_gallery(gallery) for gallery in galleries])

@bp.route('/add', methods=['POST'])
def create_gallery():
    data = request.get_json()

    # Membuat galeri jika pengguna memiliki peran yang sesuai
    gallery_data = {
        'id_kos': data.get('id_kos'),
        'foto_url': data.get('foto_url')
    }
    gallery = Gallery(**gallery_data)
    db.session.add(gallery)
    db.session.commit()
    return jsonify(Serializer.serialize_gallery(gallery)), 201

@bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_gallery(id):
    data = request.get_json()
    
    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404

    for key, value in data.items():
        setattr(gallery, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_gallery(gallery))

@bp.route('/update/detail/<int:id_kos>', methods=['PUT'])
@jwt_required()
def update_galleries_by_kos(id_kos):
    data = request.get_json()
    

    # Updating all galleries with the specified id_kos
    galleries = Gallery.query.filter_by(id_kos=id_kos).all()
    if not galleries:
        return jsonify({'message': 'Galleries not found for the given id_kos'}), 404

    for gallery in galleries:
        for key, value in data.items():
            setattr(gallery, key, value)
    db.session.commit()
    return jsonify({'message': 'Galleries updated successfully'}), 200

@bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_gallery(id):
    data = request.get_json()
    
    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404
    
    db.session.delete(gallery)
    db.session.commit()
    return jsonify({'message': 'Gallery deleted'}), 200

@bp.route('/delete/detail/<int:id_kos>', methods=['DELETE'])
# @jwt_required()
def delete_galleries_by_kos(id_kos):
    data = request.get_json()
    

    # Deleting all galleries with the specified id_kos
    galleries = Gallery.query.filter_by(id_kos=id_kos).all()
    if not galleries:
        return jsonify({'message': 'Galleries not found for the given id_kos'}), 404

    for gallery in galleries:
        db.session.delete(gallery)
    db.session.commit()
    return jsonify({'message': 'Galleries deleted successfully'}), 200


