#!/usr/bin/python3
from api.v1.views import app_view
from models import storage
from models.place import Place
from flask import jsonify, make_response, abort, request


@app_view.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def places(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    
    return jsonify([obj.to_dict() for obj in city.places])

@app_view.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    
    return jsonify(place.to_dict())

@app_view.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    
    place.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_view.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")

    user_id = new_place['user_id']    
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)

    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_view.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    
    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")
    
    for key, value in body_req.items():
        if key != "id" and key != "created_at" and key != "updated_at" \
        and key != "user_id" and key != "city_id":
            setattr(place, key, value)
    
    return make_response(jsonify(place.to_dict()), 200)

@app_view.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all("Place").values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get("State", s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get("City", c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all("Place").values()
        amenities_obj = [storage.get("Amenity", a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

    