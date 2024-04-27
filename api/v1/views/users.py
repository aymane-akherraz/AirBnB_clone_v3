#!/usr/bin/python3
""" users module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    """ Retrieves the list of all User objects """

    if user_id:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        abort(404)

    return jsonify([user.to_dict() for user in
                    storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    """ Deletes a User object """

    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'])
def insert_new_user():
    """ Creates an User object """

    user = request.get_json()
    if user:
        if 'email' not in user:
            abort(400, 'Missing email')
        if 'password' not in user:
            abort(400, 'Missing password')
        new = User(**user)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates an User object """

    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if data is not None:
            for k, v in data.items():
                if k not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict())
        abort(400, 'Not a JSON')
    abort(404)
