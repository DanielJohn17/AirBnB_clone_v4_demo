#!/usr/bin/python3
from api.v1.views import app_view
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response


@app_view.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    all_amenities = storage.all("Amenity")

    return jsonify([obj.to_dict() for obj in all_amenities.values()])

@app_view.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    
    return jsonify(amenity.to_dict())

@app_view.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    
    amenity.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_view.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    
    amenity = Amenity(**new_amenity)

    storage.new(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)

@app_view.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    
    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")
    
    for key, value in body_req.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(amenity, key, value)
    
    storage.save()
    
    return make_response(jsonify(amenity.to_dict()), 200)
