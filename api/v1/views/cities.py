#!/usr/bin/python3
"""Module for City objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201
