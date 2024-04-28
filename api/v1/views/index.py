#!/usr/bin/python3
""" import app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """ return in JSON mode {status: OK} """
    response = {"status": "OK"}
    return jsonify(response)
