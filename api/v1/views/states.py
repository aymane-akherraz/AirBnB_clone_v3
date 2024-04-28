#!/usr/bin/python3
""" State module:  This module defines the API routes
for handling states in the Flask app.
It includes route handlers for retrieving all states,
retrieving a specific state by ID, creating a new state,
updating an existing state, and deleting a state.

Routes:
- GET /states: Retrieve all states.
- GET /states/<state_id>: Retrieve a specific state by ID.
- DELETE /states/<state_id>: Delete a state.
- POST /states/: Create a new state.
- PUT /states/<state_id>: Update an existing state.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ Retrieves the list of all State objects """
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())

    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def insert_new_state():
    """ Creates a State """
    state = request.get_json(silent=True)
    if state is None:
        abort(400, 'Not a JSON')
    if 'name' not in state:
        abort(400, 'Missing name')
    new = State(**state)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
