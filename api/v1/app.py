#!/usr/bin/python3
""" Flask web app: This module sets up a Flask web server
that handles API requests.
It registers the necessary routes and configurations
to respond to HTTP requests.
The server listens on the specified host and port,
which can be customized through environment variables.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handles not found pages """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", '5000'))
    app.run(host=host, port=port, threaded=True)
