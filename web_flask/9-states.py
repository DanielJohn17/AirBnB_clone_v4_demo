#!/usr/bin/python3

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    states = sorted(storage.all("State").values(), key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)

@app.route("/states/<string:id>", strict_slashes=False)
def states_by_id(id):
    states = sorted(storage.all("State").values(), key=lambda x: x.name)
    return render_template("9-states.html", states=states, id=id)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)