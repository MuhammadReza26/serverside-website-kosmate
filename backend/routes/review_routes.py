from flask import Blueprint, request, jsonify
from models import db, Review, User
from serializers import Serializer

bp = Blueprint('review_routes', __name__)

@bp.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([Serializer.serialize_review(review) for review in reviews])

@bp.route('/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    return jsonify(Serializer.serialize_review(review))

@bp.route('/add', methods=['POST'])
def create_review():
    data = request.get_json()
    
    # Memastikan data yang diterima tidak kosong
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Membuat ulasan jika pengguna memiliki peran yang sesuai
    review_data = {
        'id_kos': data.get('id_kos'),
        'name' : data.get('name'),
        'review': data.get('review')
    }
    review = Review(**review_data)
    db.session.add(review)
    db.session.commit()
    return jsonify(Serializer.serialize_review(review)), 201


@bp.route('/update/<int:id>', methods=['PUT'])
def update_review(id):
    data = request.get_json()
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_review(review))

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200
