#!/usr/bin/python3
from api.v1.views import app_view
from flask import jsonify
from models import storage


@app_view.route("/status", methods=['GET'],strict_slashes=False)
def status():
    return jsonify({"Status": "OK"})


@app_view.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    return jsonify(amenities=storage.count("Amenity"), 
                    cities=storage.count("City"), 
                    places=storage.count("Place"), 
                    reviews=storage.count("Review"), 
                    states=storage.count("State"), 
                    users=storage.count("User"))