#!/usr/bin/python3
""" cities module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_of_state(state_id):
    """ Retrieves the list of all City objects of a State """

    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id=None):
    """ Retrieve a City object """

    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def remove_city(city_id):
    """ Deletes a City object """

    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def insert_new_city(state_id):
    """ Creates a City object """

    if storage.get(State, state_id):
        city = request.get_json()
        if city is not None:
            if 'name' not in city:
                abort(400, 'Missing name')
            new = City(**city, state_id=state_id)
            new.save()
            return jsonify(new.to_dict()), 201
        abort(400, 'Not a JSON')
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates a City object """

    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        if data is not None:
            for k, v in data.items():
                if k not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict())
        abort(400, 'Not a JSON')
    abort(404)
