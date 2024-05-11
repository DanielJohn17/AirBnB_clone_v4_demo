#!/usr/bin/python3
from api.v1.views import app_view
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City


@app_view.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def cities(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])

@app_view.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())

@app_view.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    
    city.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_view.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def post_city(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")

    city = City(**new_city)
    setattr(city, 'state_id', state_id)

    storage.new(city)
    storage.save()

    return make_response(jsonify(city.to_dict()), 201)

@app_view.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    
    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")
    
    for key, value in body_req.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
