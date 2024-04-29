# api/v1/views/places.py
from flask import jsonify, abort, request
from models import storage, City, Place

@app.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
