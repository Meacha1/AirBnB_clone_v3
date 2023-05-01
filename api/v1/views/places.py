#!/usr/bin/python3
"""Module for City objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    place = Place(**request.get_json())
    storage.new(place)
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects depending of the JSON in the body of the
    request
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    all_places = storage.all('Place').values()

    if not data:
        return jsonify([place.to_dict() for place in all_places])

    if 'states' in data:
        states = set(data['states'])
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                for city in state.cities:
                    all_places |= set(city.places)

    if 'cities' in data:
        cities = set(data['cities'])
        for city_id in cities:
            city = storage.get('City', city_id)
            if city:
                all_places |= set(city.places)

    if 'amenities' in data:
        amenities = set(data['amenities'])
        for place in list(all_places):
            place_amenities = {a.id for a in place.amenities}
            if not amenities.issubset(place_amenities):
                all_places.remove(place)

    return jsonify([place.to_dict() for place in all_places])
