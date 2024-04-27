#!/usr/bin/python3
""" states module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """ Retrieves the list of all State objects """

    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        abort(404)

    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def remove_state(state_id):
    """ Deletes a State object """

    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'])
def insert_new_state():
    """ Creates a State """

    state = request.get_json()
    if state:
        if 'name' not in state:
            abort(400, 'Missing name')
        new = State(**state)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """

    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if data:
            for k, v in data.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict())
        abort(400, 'Not a JSON')
    abort(404)
