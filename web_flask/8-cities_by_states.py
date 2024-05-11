#!/usr/bin/python3

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    states = sorted(storage.all("State").values(), key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)

@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    states = sorted(storage.all("State").values(), key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)