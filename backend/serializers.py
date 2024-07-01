class Serializer:
    @staticmethod
    def serialize_user(user):
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'password': user.password
            }

    @staticmethod
    def serialize_detail_kos(kos):
        return {
            'id': kos.id,
            'id_pengelola_kos': kos.id_pengelola_kos,
            'kos_name': kos.kos_name,
            'kos_type': kos.kos_type,
            'room_size': kos.room_size,
            'price': kos.price,
            'address': kos.address,
            'shared_facilities': kos.shared_facilities,
            'room_facilities': kos.room_facilities,
            'available_room': kos.available_room
        }

    @staticmethod
    def serialize_gallery(gallery):
        return {
            'id': gallery.id,
            'id_kos': gallery.id_kos,
            'foto_url': gallery.foto_url,
        }

    @staticmethod
    def serialize_review(review):
        return {
            'id': review.id,
            'id_kos': review.id_kos,
            'name' : review.name,
            'review': review.review,
        }

    @staticmethod
    def serialize_admin(admin):
        return {
            'id': admin.id,
            'admin_name': admin.admin_name,
            'email': admin.email,
            'password': admin.password,
        }
