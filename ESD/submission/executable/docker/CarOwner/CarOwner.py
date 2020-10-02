from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/carowner'

db = SQLAlchemy(app)
CORS(app)


class CarOwner(db.Model):
    __tablename__ = 'carowner'

    coID = db.Column(db.Integer, primary_key=True)
    coUsername = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    telegramID = db.Column(db.String(64), nullable=False)
    coPassword = db.Column(db.String(64), nullable=False)

    def json(self):
        return {"coID": self.coID, "coUsername": self.coUsername, "name": self.name, "email": self.email , "telegramID": self.telegramID}

@app.route("/carowner")
def get_all():
	return jsonify({"carowners": [carowner.json() for carowner in carowner.query.all()]})

@app.route("/carowner/<int:coID>")
def getcarownerByID(coID):
    carowner = CarOwner.query.filter_by(coID=coID).first()
    if carowner:
        return jsonify(carowner.json())
    return jsonify({"message": "Car Owner not found."}), 404

@app.route("/carowner/<string:coUsername>")
def getcarownerByUsername(coUsername):
    result = CarOwner.query.filter_by(coUsername=coUsername).first()
    if result:
        return jsonify(result.json())
    return jsonify({"message": "Car Owner not found."}), 404

@app.route("/carowner", methods=['POST'])
def addcarowner():
    data = request.get_json()
    coUsername = data['coUsername']
    
    if (CarOwner.query.filter_by(coUsername=coUsername).first()):
        return jsonify({"message": "A Car Owner with username '{}' already exists.".format(coUsername)}), 400

    carowner = CarOwner(**data)

    try:
        db.session.add(carowner)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the Car Owner."}), 500

    return jsonify(carowner.json()), 201

def get_email(coID):
    carowner = CarOwner.query.filter_by(coID=coID).first()
    if carowner:
        return jsonify(carowner['email'].json()) 
    return jsonify({"message": "Car Owner not found."}), 404


@app.route("/carowner/login", methods=["POST"])
def authenticate():
    data = request.get_json()
    coUsername = data['coUsername']
    coPassword = data['coPassword']
    car_owner = CarOwner.query.filter_by(coUsername=coUsername, coPassword=coPassword).first()
    
    if car_owner:
        return jsonify({"message": "Welcome, {} ".format(coUsername)}), 201

    return jsonify({"message": "Invalid username or password."}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7100, debug=True)
    
# by default port is 5000 for flask
# debug = true will display all the error messages,
# it will also auto rerun flask when file is saved (else we have to ctrl enter to rerun)