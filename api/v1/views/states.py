#!/usr/bin/python3
""" import modules """
from models.state import State
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ get all states def """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_state_id(state_id):
    """ get state by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ delete state def """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ create state def """
    state_request = request.get_json(silent=True)
    if state_request is None:
        abort(400, 'Not a JSON')
    if "name" not in state_request:
        abort(400, 'Missing name')
    new_state = State(**state_request)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ update state """
    state_request = request.get_json(silent=True)
    if state_request is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, val in state_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict())
