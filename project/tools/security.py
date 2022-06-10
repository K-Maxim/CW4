import base64
import hashlib
import hmac
import datetime
import calendar
import jwt

from project.exceptions import ItemNotFound
from project.helpers.constant import PWD_HASH_SALT, PWD_HASH_ITERATIONS

secret = 's3cR$eT'
algo = 'HS256'


def generate_passwords(password):  # хешируем пароль у создающего пользователя
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return base64.b64encode(hash_digest)


def login_user(reg_json, user):
    user_email = reg_json.get("email")
    user_password = reg_json.get("password")
    if user_email and user_password:
        password_hashed = user["password"]
        if compare_password(password_hashed, user_password):
            return generate_tokens(reg_json)
    raise ItemNotFound


def compare_password(password_hash, other_password) -> bool:
    decoded_digest = base64.b64decode(password_hash)

    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        other_password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return hmac.compare_digest(decoded_digest, hash_digest)


def generate_tokens(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algorithm=algo)

    tokens = {"access_token": access_token,
              "refresh_token": refresh_token}
    return tokens, 201


def refresh_user_token(reg_json):
    refresh_token = reg_json.get("refresh_token")
    data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
    if data:
        tokens = generate_tokens(data)
        return tokens
    raise ItemNotFound
