#!/usr/bin/python3
"""
Place-Amenity link objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('places/<place_id>/amenities',
                     methods=['GET'])
    def get_amenities(place_id):
        """Retrieves the list of all Amenity objects"""
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities_list = []
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_amenity(place_id, amenity_id):
        """Deletes an Amenity object"""
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if place.amenities.count(amenity) == 0:
            abort(404)
        place.amenities.delete(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_amenity(place_id, amenity_id):
        """Creates an Amenity object"""
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if place.amenities.count(amenity) != 0:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
