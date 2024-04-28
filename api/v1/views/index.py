#!/usr/bin/python3
""" Index module: This module contains route handlers for the Flask app.
It defines the various routes and their corresponding functions
to handle incoming HTTP requests.
Each route is responsible for a specific endpoint or functionality of the app.

Routes:
- GET /status: Returns the status of the API.
- GET /stats: Retrieves the number of each object by type
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ Return the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats_count():
    """ Retrieves the number of each objects by type """
    my_classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
                  "reviews": "Review", "states": "State", "users": "User"}

    return jsonify({k: storage.count(v) for k, v in my_classes.items()})
