#!/usr/bin/python3
''' Flask app '''
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r'/api/*': {'origins': app_host}})


@app.errorhandler(404)
def error():
    ''' error '''
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(self):
    ''' close storage '''
    storage.close()


if __name__ == '__main__':
    ''' Main Function '''
    port = int(os.getenv('HBNB_API_PORT', 5000))
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app.run(host=host, port=port, threaded=True)
