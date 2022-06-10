import base64
import hashlib
import hmac

from flask_restx import abort

from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.helpers.constant import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.schemas.user import UserSchema

from project.services.base import BaseService


class UsersService(BaseService):
    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        print(UserSchema(many=True).dump(users))
        return UserSchema(many=True).dump(users)

    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email=email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def create(self, new_pd):
        user_password = new_pd.get("password")
        if user_password:
            new_pd["password"] = self.generate_password_digest(user_password)
        user = UserDAO(self._db_session).create(new_pd)
        return UserSchema().dump(user)

    def update(self, new_pd):
        user = UserDAO(self._db_session).update(new_pd)
        return UserSchema().dump(user)

    def update_password(self, new_pd):
        print(new_pd)
        old_password = new_pd.get("old_password")
        print(old_password)
        new_password = new_pd.get("new_password")

        user = self.get_item_by_id(new_pd.get("id"))
        if not self.compare_passwords(old_password, new_password):
            abort(400, 'Старый и новый пароль совпадают')

        user_update = {
            "email": user.get('email'),
            "password": self.generate_password_digest(new_password)
        }
        print(user_update)
        UserDAO(self._db_session).update(user_update)


    def generate_password_digest(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=PWD_HASH_SALT,
            iterations=PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)

