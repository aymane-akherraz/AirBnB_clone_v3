#!/usr/bin/python3
""" amenities module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id=None):
    """ Retrieves the list of all Amenity objects """

    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        abort(404)

    return jsonify([amenity.to_dict() for amenity in
                    storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def remove_amenity(amenity_id):
    """ Deletes a Amenity object """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def insert_new_amenity():
    """ Creates an Amenity object """

    amenity = request.get_json()
    if amenity:
        if 'name' not in amenity:
            abort(400, 'Missing name')
        new = Amenity(**amenity)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates an Amenity object """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if data:
            for k, v in data.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, k, v)
            amenity.save()
            return jsonify(amenity.to_dict())
        abort(400, 'Not a JSON')
    abort(404)
