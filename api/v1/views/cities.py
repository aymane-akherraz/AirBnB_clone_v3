#!/usr/bin/python3
""" City module: This module defines the API routes
for handling cities in the Flask app.
It includes route handlers for retrieving all cities of a state,
retrieving a specific city by ID, creating a new city,
updating an existing city, and deleting a city.

Routes:
- GET /states/<state_id>/cities: Retrieve all cities for a specific state.
- GET /cities/<city_id>: Retrieve a specific city by ID.
- DELETE /cities/<city_id>: Delete a city.
- POST /states/<state_id>/cities: Create a new city for a specific state.
- PUT /cities/<city_id>: Update an existing city.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_of_state(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get("State", state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """ Retrieve a City object """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def remove_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def insert_new_city(state_id):
    """ Creates a City object """
    if storage.get("State", state_id):
        city = request.get_json(silent=True)
        if city is None:
            abort(400, 'Not a JSON')
        if 'name' not in city:
            abort(400, 'Missing name')
        my_dict = {**city, 'state_id': state_id}
        new = City(**my_dict)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if city:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
    abort(404)
