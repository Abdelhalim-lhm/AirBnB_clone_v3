#!/usr/bin/python3
""" import modules """
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """ get all amenities def """
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route(
        '/amenities/<amenity_id>', methods=["GET"], strict_slashes=False)
def get_amenity_id(amenity_id):
    """ get amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route(
        'amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity def """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ create amenity def """
    amenity_request = request.get_json(silent=True)
    if amenity_request is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_request:
        abort(400, 'Missing name')
    new_amenity = Amenity(**amenity_request)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",  methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity def """
    amenity_request = request.get_json(silent=True)
    if amenity_request is None:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, val in amenity_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())
