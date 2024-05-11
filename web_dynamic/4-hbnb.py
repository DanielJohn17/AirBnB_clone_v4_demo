#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
import uuid


app = Flask('web_dynamic')
app.url_map.strict_slashes=False

@app.route("/4-hbnb")
def hbnb():
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    cache_id = uuid.uuid4()

    return render_template("4-hbnb.html", states=states,
                            amenities=amenities,
                            places=places,
                            cache_id=cache_id)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
