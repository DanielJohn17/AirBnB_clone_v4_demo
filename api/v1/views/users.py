#!/usr/bin/python3
from api.v1.views import app_view
from models import storage
from models.user import User
from flask import jsonify, request, abort, make_response


@app_view.route("/users", methods=['GET'], strict_slashes=False)
def users():
    all_users = storage.all("User")

    return jsonify([obj.to_dict() for obj in all_users.values()])

@app_view.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    
    return jsonify(user.to_dict())

@app_view.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get("User",user_id)
    if not user:
        abort(404)
    
    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_view.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    user = User(**new_user)

    storage.new(user)
    storage.save()

    return make_response(jsonify(user.to_dict()), 201)

@app_view.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    
    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")
    
    for key, value in body_req.items():
        if key != "id" and key != "created_at" and key != "updated_at" and key != "email":
            setattr(user, key, value)
    
    storage.save()
    
    return make_response(jsonify(user.to_dict()), 200)

