from flask import request, abort
from flask_restx import Resource, Namespace

from project.exceptions import ItemNotFound

from project.services.user_service import UsersService
from project.setup_db import db
from project.tools.security import login_user, refresh_user_token

auth_ns = Namespace('auth')


@auth_ns.route("/register/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")
        return UsersService(db.session).create(req_json)


@auth_ns.route("/login/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None is [email, password]:
            return '', 400

        try:
            user = UsersService(db.session).get_item_by_email(email)
            tokens = login_user(request.json, user)

            return tokens, 201
        except ItemNotFound:
            abort(401, "ошибка авторизации")

    def put(self):
        req_json = request.json
        tokens = refresh_user_token(req_json)

        return tokens, 201
