#!/usr/bin/python3
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_view
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_view)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.errorhandler(404)
def error(exception):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT

    app.run(host=host, port=port, threaded=True, debug=True)