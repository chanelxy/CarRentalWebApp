from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/car'


db = SQLAlchemy(app)
CORS(app)

class Car(db.Model):
    __tablename__ = 'car'

    cID = db.Column(db.Integer, primary_key=True)
    carPlateNo = db.Column(db.String(64), nullable=False)
    coUsername = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    colour = db.Column(db.String(64), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    transmissionType = db.Column(db.String(64), nullable=False)
    dailyRate = db.Column(db.Integer, nullable=False)
    postalCode = db.Column(db.Integer, nullable=False) #This is the postal code where the car renter will pick up the car.


    def __init__(self, carPlateNo, coUsername, brand, model, colour, capacity, transmissionType, dailyRate, postalCode, cID = None):
        self.cID = cID
        self.carPlateNo = carPlateNo
        self.coUsername = coUsername
        self.brand = brand
        self.model = model
        self.colour = colour
        self.capacity = capacity
        self.transmissionType = transmissionType
        self.dailyRate = dailyRate
        self.postalCode = postalCode

    # def __init__(self, carPlateNo, coUsername, brand, model, colour, capacity, transmissionType, hourlyRate,postalCode):
    #     self.carPlateNo = carPlateNo
    #     self.coUsername = coUsername
    #     self.brand = brand
    #     self.model = model
    #     self.colour = colour
    #     self.capacity = capacity
    #     self.transmissionType = transmissionType
    #     self.hourlyRate = hourlyRate
    #     self.postalCode = postalCode


    def json(self):
        return {"cID": self.cID, "carPlateNo": self.carPlateNo, "coUsername": self.coUsername, "brand": self.brand,
        "model": self.model,"colour": self.colour,"capacity": self.capacity,"transmissionType": self.transmissionType,"dailyRate": self.dailyRate
        ,"postalCode": self.postalCode}

'''
Functions for Car
'''
@app.route("/car")
def get_all_car():
    return jsonify({"car": [car.json() for car in Car.query.all()]})


@app.route("/car/cid/<string:cID>")
def get_car_by_cid(cID):
    car = Car.query.filter_by(cID=cID).first()
    if car:
        return jsonify(car.json())
    return jsonify({"message": "Car not found."}), 404

@app.route("/car/carplateno/<string:carPlateNo>")
def get_car_by_carplateno(carPlateNo):
    car = Car.query.filter_by(carPlateNo=carPlateNo).first()
    if car:
        return jsonify(car.json())
    return jsonify({"message": "Car not found."}), 404

@app.route("/car/cousername/<string:coUsername>")
def get_car_by_cousername(coUsername):
    car_result = Car.query.filter_by(coUsername=coUsername)
    if car_result:
        return jsonify({"car": [car.json() for car in car_result]})
    return jsonify({"message": "Car not found."}), 404

@app.route("/car/capacity/<int:capacity>")
def get_car_by_capacity(capacity):
    return jsonify({"car": [car.json() for car in Car.query.filter(Car.capacity >= capacity)]})

@app.route("/car/capacity/<int:capacity>/<string:transmissiontype>")
def get_car_by_capacity_and_transmissiontype(capacity, transmissiontype):
    result = Car.query.filter(Car.capacity >= capacity).filter(Car.transmissionType==transmissiontype)
    return jsonify({"car": [car.json() for car in result]})


@app.route("/car", methods=['POST'])
def add_car():
    data = request.get_json()
    carPlateNo = data['carPlateNo']
    if (Car.query.filter_by(carPlateNo=carPlateNo).first()):
        return jsonify({"message": "A car with carPlateNo '{}' already exists.".format(carPlateNo)}), 400

    car = Car(**data)

    try:
        db.session.add(car)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the car."}), 500

    return jsonify(car.json()), 201

if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    app.run(host='0.0.0.0',port=7000, debug=True) #need to use differen port for each microservice. By default, it is 5000. Project need to use diff port no.s
    