#!/usr/bin/python3
"""
Place_amenities Module
This module defines the API routes for handling amenities in the Flask app.
It includes route handlers for retrieving all amenities for a place,
deleting an amenity from a place, and adding an amenity to a place.
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
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
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
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
    return jsonify(amenity.to_dict()), 201
