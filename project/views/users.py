from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.user_service import UsersService
from project.helpers.decorators import auth_required
from project.setup_db import db


users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):
    @auth_required
    def get(self):
        users = UsersService(db.session).get_all_users()
        return users


@users_ns.route("/<int:user_id>/")
class UserView(Resource):
    @auth_required
    def get(self, user_id: int):
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404)

    @auth_required
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


@users_ns.route("/password/<int:user_id>/")
class UserPatchView(Resource):
    @auth_required
    def put(self, user_id: int):
        req_json = request.json
        old_password = req_json.get("old_password", None)
        new_password = req_json.get("new_password", None)

        if None in [old_password, new_password]:
            abort(400)

        if not req_json.get("id"):
            req_json['id'] = user_id
        try:
            return UsersService(db.session).update_password(req_json)
        except ItemNotFound:
            abort(404)
