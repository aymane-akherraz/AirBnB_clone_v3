#!/usr/bin/python3
""" Place module: This module defines the API routes
for handling places in the Flask app.
It includes route handlers for retrieving all places in a city,
retrieving a specific place by ID, creating a new place,
updating an existing place, and deleting a place.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """ Retrieves the list of all Place objects of a city """
    city = storage.get("City", city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """ Retrieve a Place object """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search():
    """ Retrieves all Place objects depending of the
        JSON in the body of the request
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    state_ids = data.get('states', [])
    city_ids = data.get('cities', [])
    amenity_ids = data.get('amenities', [])

    if not data or (not state_ids and not city_ids and not amenity_ids):
        return jsonify([place.to_dict()
                        for place in storage.all(Place).values()])

    all_places = list(storage.all(Place).values())
    places_list = []

    for state_id in state_ids:
        state = storage.get("State", state_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    places_list.append(place)

    for city_id in city_ids:
        city = storage.get("City", city_id)
        if city:
            for place in city.places:
                if place not in places_list:
                    places_list.append(place)

    if amenity_ids:
        if not places_list:
            places_list = all_places
        for place in places_list:
            for amenity_id in amenity_ids:
                amenity = storage.get("Amenity", amenity_id)
                if amenity and amenity not in place.amenities:
                    places_list.remove(place)
                    break

    places_list = [place.to_dict() for place in places_list]
    for k, v in places_list.items():
        if k == 'amenities':
            del places_list[k]

    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def insert_new_place(city_id):
    """ Creates a Place object """
    if storage.get("City", city_id):
        place = request.get_json(silent=True)
        if place is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in place:
            abort(400, 'Missing user_id')
        if storage.get("User", place['user_id']) is None:
            abort(404)
        if 'name' not in place:
            abort(400, 'Missing name')
        my_dict = place.copy()
        my_dict['city_id'] = city_id
        new = Place(**my_dict)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ["id", "user_id", "city_id", "created_at",
                         "updated_at"]:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict())
    abort(404)
