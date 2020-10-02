from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

CORS(app)

@app.route("/bookcar", methods=['POST'])
def bookcar():
    '''
    Receives data via post in the form of a JSON object
    expected parameters are crUsername, coUsername, cID, startDate, endDate
    '''
    data = request.get_json()
    
    cID = data['cID']
    crUsername = data['crUsername']
    startDate = data['startDate']
    endDate = data['endDate']

	#TODO add validation for crID, coID and carID, retrieve price from car microservice

    available, message = verify_car_available(cID, startDate, endDate)
    if not available:
        return message, 400
    else:
         #retrieve crID
        carRenterResponse = requests.get('http://carrenter:7200/carrenter/' + crUsername)
        crID = json.loads(carRenterResponse.text)['crID']

        #retrieve car details
        carResponse = requests.get('http://car:7000/car/cid/' + str(cID))
        car = json.loads(carResponse.text)
        dailyRate = car['dailyRate']
        #retrieve coID
        if carResponse.status_code == 404:
            return message, 400

        carOwnerResponse = requests.get('http://carowner:7100/carowner/' + car['coUsername'])
        coID = json.loads(carOwnerResponse.text)['coID']
		#reconstruct str datetime from dd/mm/yyyy to yyyy/mm/dd
        start_date = datetime.strptime(data['startDate'], r"%Y-%m-%d") # datetime object
        end_date = datetime.strptime(data['endDate'], r"%Y-%m-%d") # datetime object
        # construct the different rows to insert into rental transaction (different dates)
        delta = end_date - start_date       # as timedelta

        #debugging
        # return jsonify(car)
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            insert_date_str = str(day.year) + "-" + str(day.month) + "-" + str(day.day)
            row_data = {"crID": crID, "coID": coID, "carID": cID, "rentalDate": insert_date_str, "price": dailyRate, "rentalStatus": "reserved"}
            requests.post('http://rentaltransactions:7300/rentaltransactions', json = row_data)
        return jsonify({"message": "rental_transactions_inserted"}), 200

def verify_car_available(cID, startDate, endDate):
    response = requests.get('http://rentaltransactions:7300/rentaltransactions/' + str(cID) + "/" + startDate + "/" + endDate)
    if response.status_code == 200:
        return True, response.text
    else:
        return False, response.text


if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0',port=8300, debug=True) #need to use different port for each microservice. By default, it is 5000. Project need to use diff port no.s