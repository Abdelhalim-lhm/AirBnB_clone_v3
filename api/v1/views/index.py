#!/usr/bin/python3
""" import app_views """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    """ return in JSON mode {status: OK} """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def stats():
    """ count the object by classes """
    count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(count)
