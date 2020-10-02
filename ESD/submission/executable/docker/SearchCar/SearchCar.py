from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ
import requests
import json

app = Flask(__name__)

CORS(app)

@app.route("/searchcar")
def get_all_cars():
    carResponse = requests.get('http://car:7000/car')
    return json.loads(carResponse.content)

@app.route("/searchcar/<int:cID>")
def get_car_by_cID(cID):
    carResponse = requests.get('http://car:7000/car/cid/' + str(cID))
    return json.loads(carResponse.content)

@app.route("/searchcar/<string:start_date>/<string:end_date>/<int:seating_capacity>/<string:transmissiontype>/<string:postalcode>")
def get_car_filter_options(start_date, end_date, seating_capacity, transmissiontype, postalcode):
    carResponse = requests.get('http://car:7000/car/capacity/' + str(seating_capacity) + "/" + transmissiontype)
    json.loads(carResponse.text)
    carList = json.loads(carResponse.text)['car']
    
    rentalTransactionResponse = requests.get('http://rentaltransactions:7300/rentaltransactions/' + start_date + "/" + end_date)
    rentalTransactionList = json.loads(rentalTransactionResponse.text)['rentalTransaction']

    carIDSet = set()
    for rentalTransaction in rentalTransactionList:
        carIDSet.add(rentalTransaction['carID'])

    availableCarList = []
    for car in carList:
        if car['cID'] not in carIDSet:
            distanceResult = requests.get("http://googlematrix:9000/getdistance/" + postalcode + "/" + str(car['postalCode']))
            if distanceResult.status_code == 400:
                distance = 0
            else:
                distance = json.loads(distanceResult.text)['distance_meters']
            # car['coordinates'] = coordinates
            car['distance'] = distance
            availableCarList.append(car)
    #sort car by furthest to closest
    availableCarList.sort(key=lambda x:x['distance'])
    #returns (car parameters, car coordinates, distance from renter)
    return jsonify({"car": availableCarList})


if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0',port=8200, debug=True) #need to use different port for each microservice. By default, it is 5000. Project need to use diff port no.s