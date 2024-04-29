#!/usr/bin/python3
""" Place_amenities module: This module defines the API routes
for handling amenities in the Flask app.
It includes route handlers for retrieving all amenities for a place,
deleting an amenity from a place, and adding an amenity to a place.

Routes:
- GET /places/<place_id>/amenities: Retrieve all amenities for a place.
- DELETE /places/<place_id>/amenities/<amenity_id>: Delete an amenity
  from a place.
- POST /places/<place_id>/amenities/<amenity_id>: Add an amenity to a place.
"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_Amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
