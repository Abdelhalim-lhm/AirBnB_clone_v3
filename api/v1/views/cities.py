#!/usr/bin/python3
""" import modules """
from models.state import State
from models.city import City
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """ get cities by state id def """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def get_city_id(city_id):
    """ get city by id """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return abort(404)


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ delete city def """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ create city by state id def """
    city_request = request.get_json(silent=True)
    if city_request is None:
        abort(400, 'Not a JSON')
    if "name" not in city_request:
        abort(400, 'Missing name')
    city_request['state_id'] = state_id
    new_city = City(**city_request)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ update state """
    city_request = request.get_json(silent=True)
    if city_request is None:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, val in city_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict())
