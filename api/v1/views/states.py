#!/usr/bin/python3
from flask import jsonify, abort, make_response, request
from api.v1.views import app_view
from models import storage
from models.state import State


@app_view.route("/states", methods=['GET'], strict_slashes=False)
def states():
    all_states = storage.all("State")

    return jsonify([obj.to_dict() for obj in all_states.values()])

@app_view.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())

@app_view.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def del_state_by_id(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    
    state.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_view.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    
    state = State(**new_state)
    storage.new(state)
    storage.save()

    return make_response(jsonify(state.to_dict()), 201)

@app_view.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")

    for key, value in body_req.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)

