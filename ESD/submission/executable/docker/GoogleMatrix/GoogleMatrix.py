import os
import json
import googlemaps
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

app = Flask(__name__)
 
CORS(app)

def create_client():
	client = googlemaps.Client(key="")
	return client

@app.route("/getcoordinates/<string:postalcode>")
def getCoordinatesByPostalCode(postalcode):
    client = create_client()
    results = client.geocode(address = "singapore " + postalcode) #googlemaps api methods takes in args and kwargs
    if len(results) == 0:
        return jsonify({'message':'No such address'}), 400
    return jsonify({'message':'address found', 'coordinates': results[0]['geometry']['location']}), 200

@app.route("/getdistance/<string:renterpostalcode>/<string:carpostalcode>")
def getDistanceByPostalCodes(renterpostalcode, carpostalcode): 
    client = create_client()
    results = client.distance_matrix(origins = "singapore " + renterpostalcode, destinations = "singapore" + carpostalcode) #googlemaps api methods takes in args and kwargs
    if  results['destination_addresses'][0] == '' or  results['origin_addresses'][0] == '':
        return jsonify({'message':'Addresses not found'}), 400
    else:
        distance_text = results['rows'][0]['elements'][0]['distance']['text']
        distance_meters = results['rows'][0]['elements'][0]['distance']['value']
        return jsonify({'message':'address found', 'distance_text': distance_text, 'distance_meters': distance_meters}), 200
    
if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0', port=9000, debug=True)