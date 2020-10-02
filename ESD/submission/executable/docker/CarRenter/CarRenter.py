from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class CarRenter(db.Model):
    __tablename__ = 'carrenter'

    crID = db.Column(db.Integer, primary_key=True)
    crUsername = db.Column(db.String(64), nullable=False)
    crPassword = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    telegramID = db.Column(db.String(64), nullable=False)

    def json(self):
        return {
            "crID": self.crID, 
            "crUsername": self.crUsername,
            "crPassword": self.crPassword,
            "name": self.name, 
            "email": self.email, 
            "telegramID": self.telegramID
            }

@app.route("/carrenter")
def get_all():
    return jsonify({"CarRenter": [crID.json() for crID in CarRenter.query.all()]})

@app.route("/carrenter/<int:crID>")
def getCarRenterByID(crID):
    car_renter = CarRenter.query.filter_by(crID=crID).first()
    if car_renter:
        return jsonify(car_renter.json())
    return jsonify({"message": "car renter ID not found."}), 404

@app.route("/carrenter/<string:crUsername>")
def getCarRenterByUsername(crUsername):
    car_renter = CarRenter.query.filter_by(crUsername=crUsername).first()
    if car_renter:
        return jsonify(car_renter.json())
    return jsonify({"message": "car renter username not found."}), 404

@app.route("/carrenter", methods=["POST"])
def createCarRenter():
    # status in 2xx indicates success
    status = 201
    result = {}

    data = request.get_json()
    crUsername = data['crUsername']
    car_renter = CarRenter.query.filter_by(crUsername=crUsername).first()

    if car_renter:
        status = 404
        result = {"message": "An error occurred in creation."}
        return jsonify(result), status

    if status==201:
        user = CarRenter(**data)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occurred when creating Car Renter in DB.", "error": str(e)}
        
        if status==201:
            result = user.json()
    
    return jsonify(result), status

@app.route("/carrenterlogin", methods=["POST"])
def authenticate():
    details = request.get_json()
    crUsername = details['crUsername']
    crPassword = details['crPassword']
    car_renter = carrenter.query.filter_by(crUsername=crUsername, crPassword=crPassword).first()
    
    if car_renter:
        return jsonify({"message": "Welcome {}!".format(crUsername)}), 201

    return  jsonify({"message": "Invalid username or password."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7200, debug=True)