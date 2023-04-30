#!/usr/bin/python3
''' Flask app '''
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.route('/status', methods=["GET"])
def index():
    '''index'''
    return jsonify({'status': 'OK'})


@app.route('/stats', methods=["GET"])
def stats():
    ''' Get stats '''
    return jsonify({'amenities': storage.count('Amenity'),
                    'cities': storage.count('City'),
                    'places': storage.count('Place'),
                    'reviews': storage.count('Review'),
                    'states': storage.count('State'),
                    'users': storage.count('User')})
