from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))  # Panjang string untuk mendukung hashing yang aman

class DetailKos(db.Model):
    __tablename__ = 'detail_kos'

    id = db.Column(db.Integer, primary_key=True)
    id_pengelola_kos = db.Column(db.ForeignKey('user.id'))
    kos_name = db.Column(db.String(100))
    kos_type = db.Column(db.String(20))
    room_size = db.Column(db.String(20))    
    price = db.Column(db.Integer)
    address = db.Column(db.String(200))
    shared_facilities = db.Column(db.String(200))
    room_facilities = db.Column(db.String(200))
    available_room = db.Column(db.Integer)


    user = db.relationship('User', primaryjoin='DetailKos.id_pengelola_kos == User.id', backref='detail_kos')

class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    id_kos = db.Column(db.ForeignKey('detail_kos.id'))
    foto_url = db.Column(db.String(200))

    detail_kos = db.relationship('DetailKos', primaryjoin='Gallery.id_kos == DetailKos.id', backref='galleries')

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    id_kos = db.Column(db.ForeignKey('detail_kos.id'))
    name = db.Column(db.String(100))
    review = db.Column(db.String(500))

    detail_kos = db.relationship('DetailKos', primaryjoin='Review.id_kos == DetailKos.id', backref='reviews')

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))  # Panjang string untuk nomor telepon mungkin perlu disesuaikan
    password = db.Column(db.String(255))  # Panjang string untuk mendukung hashing yang aman

