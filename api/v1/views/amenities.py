#!/usr/bin/python3
""" Amenity module: This module defines the API routes
for handling amenities in the Flask app.
It includes route handlers for retrieving all amenities,
retrieving a specific amenity by ID, creating a new amenity,
updating an existing amenity, and deleting an amenity.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """ Retrieves the list of all Amenity objects """
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        abort(404)

    return jsonify([amenity.to_dict() for amenity in
                    storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def insert_new_amenity():
    """ Creates an Amenity object """
    amenity = request.get_json(silent=True)
    if amenity is None:
        abort(400, 'Not a JSON')
    if 'name' not in amenity:
        abort(400, 'Missing name')
    new = Amenity(**amenity)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict())
    abort(404)
