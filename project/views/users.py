from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.user_service import UsersService

from project.setup_db import db


users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):

    @users_ns.response(200, "OK")
    def get(self):
        """Get all users"""
        return UsersService(db.session).get_all_users()


@users_ns.route("/<int:user_id>")
class UserView(Resource):

    @users_ns.response(200, "OK")
    @users_ns.response(404, "User не найден")
    def get(self, user_id: int):
        """Get user by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User `не найден`")

    def patch(self, user_id: int):
        req_json = request.json
        if not req_json:
            abort(400)
        if not req_json.get("id"):
            req_json['id'] = user_id
        try:
            return UsersService(db.session).update(req_json)
        except ItemNotFound:
            abort(404)


@users_ns.route("/password/<int:user_id>")
class UserPatchView(Resource):

    @users_ns.response(200, "OK")
    @users_ns.response(404, "User не найден")
    def put(self, user_id: int):
        req_json = request.json
        password_1 = req_json.get("password_1", None)
        password_2 = req_json.get("password_2", None)
        if None in [password_1, password_2]:
            abort(400)
        if not password_1 or not password_2:
            abort(400)
        if not req_json.get("id"):
            req_json['id'] = user_id
        try:
            return UsersService(db.session).update_password(req_json)
        except ItemNotFound:
            abort(404)