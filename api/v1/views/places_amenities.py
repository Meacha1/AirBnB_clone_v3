#!/usr/bin/python3
"""Module for Place-Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = []
    if storage.__class__.__name__ == 'DBStorage':
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Links a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
    return jsonify(amenity.to_dict()), 201

