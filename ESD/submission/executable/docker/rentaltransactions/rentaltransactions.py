from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import update
from os import environ
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/rentaltransaction'

 
db = SQLAlchemy(app)
CORS(app)
 
class RentalTransaction(db.Model):
    __tablename__ = 'rentaltransaction'
    transactionID  = db.Column(db.Integer(), primary_key=True)
    crID = db.Column(db.Integer(), nullable= False)
    coID = db.Column(db.Integer(), nullable= False)
    carID = db.Column(db.Integer(), nullable = False)
    rentalDate = db.Column(db.Date, nullable= False)
    price = db.Column(db.Float(precision=2), nullable = False)
    rentalStatus = db.Column(db.String(64),nullable=False)

    def __init__(self, crID, coID, carID, rentalDate, price, rentalStatus, transactionID = None):
        self.transactionID = transactionID
        self.crID = crID
        self.coID = coID
        self.carID= carID
        self.rentalDate = rentalDate
        self.price = price
        self.rentalStatus = rentalStatus
    
    # def __init__(self, crID, coID, carID, rentalDate, price, rentalStatus):
    #     self.crID = crID
    #     self.coID = coID
    #     self.carID= carID
    #     self.rentalDate = rentalDate
    #     self.price = price
    #     self.rentalStatus = rentalStatus
    
    def json(self):
        return {"transactionID": self.transactionID, "crID": self.crID, "coID": self.coID, "carID": self.carID, "rentalDate": self.rentalDate, "price": self.price, "rentalStatus" : self.rentalStatus}

@app.route("/rentaltransactions")
def get_all():
    return jsonify({"Rental Transactions": [RentalTransaction.json() for RentalTransaction in RentalTransaction.query.all()]})

# @app.route("/rentaltransactions/<string:start_date>/<string:end_date>")
# def get_rental_transaction_between_dates(start_date, end_date):
#     #reconstruct str datetime from dd/mm/yyyy to yyyy/mm/dd
#     start_date = datetime.strptime(start_date, r"%d-%m-%Y")
#     start_date = str(start_date.year) + "/" + str(start_date.month) + "/" + str(start_date.day)
#     end_date = datetime.strptime(end_date, r"%d-%m-%Y")
#     end_date = str(end_date.year) + "/" + str(end_date.month) + "/" + str(end_date.day)
#     return jsonify({"rentalTransaction": [rt.json() for rt in RentalTransaction.query.filter(RentalTransaction.rentalDate.between(start_date, end_date))]})

@app.route("/rentaltransactions/<string:start_date>/<string:end_date>")
def get_rental_transaction_between_dates(start_date, end_date):
    # #reconstruct str datetime from dd/mm/yyyy to yyyy/mm/dd
    # start_date = datetime.strptime(start_date, r"%d-%m-%Y")
    # start_date = str(start_date.year) + "/" + str(start_date.month) + "/" + str(start_date.day)
    # # end_date = datetime.strptime(end_date, r"%d-%m-%Y")
    # end_date = str(end_date.year) + "/" + str(end_date.month) + "/" + str(end_date.day)
    return jsonify({"rentalTransaction": [rt.json() for rt in RentalTransaction.query.filter(RentalTransaction.rentalDate.between(start_date, end_date))]})


@app.route("/rentaltransactions/<int:carID>/<string:start_date>/<string:end_date>")
def verify_car_available_between_dates(carID, start_date, end_date):
    #reconstruct str datetime from dd/mm/yyyy to yyyy/mm/dd
    start_date = datetime.strptime(start_date, r"%Y-%m-%d")
    start_date = str(start_date.year) + "/" + str(start_date.month) + "/" + str(start_date.day)
    end_date = datetime.strptime(end_date, r"%Y-%m-%d")
    end_date = str(end_date.year) + "/" + str(end_date.month) + "/" + str(end_date.day)
    result = [rt.json() for rt in RentalTransaction.query.filter(RentalTransaction.rentalDate.between(start_date, end_date), (RentalTransaction.carID==carID))]
    if len(result)==0:
        return jsonify({"message": "Car is available"}), 200
    else:
        return jsonify({"message": "Car is not available."}), 400

@app.route("/rentaltransactions" , methods=['POST'])
def create_transaction():
    status = 201
    result = {}

    data = request.get_json()

    transaction=RentalTransaction(**data)

    try:
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        status = 500
        result={"status": status, "message": "An error occurred when creating Rental Transaction in DB.", "error": str(e)}

    return jsonify(result),status


@app.route("/rentaltransactions/<int:transactionID>" , methods=['PUT'])
def update_transaction(transactionID):
    transaction = RentalTransaction.query.filter_by(transactionID=transactionID).first()
    if transaction!= None:
        status = 201 
        result={}
        try:
            setattr(transaction, 'rentalStatus', "paid")
            db.session.commit()
        except Exception as e:
            status = 500
            result={"status": status, "message": "An error occurred when updating Rental Transaction in DB.", "error": str(e)}
        if status == 201:
            result= transaction.json()

        return jsonify(result),status
    

@app.route("/rentaltransactions/<string:transactionID>")
def find_by_transactionID(transactionID):
    transaction = RentalTransaction.query.filter_by(transactionID=transactionID).first()
    if transaction:
        return transaction.json()
    return {'message': 'Transaction not found for transactionID ' + str(transactionID)}, 404    

@app.route("/rentaltransactions/cr/<string:crID>")
def find_by_crID(crID):
    transaction = {"RentalTransaction": [rentalDate.json() for rentalDate in RentalTransaction.query.filter_by(crID=crID).all()]}
    if transaction != {"RentalTransaction": []}:
        return jsonify(transaction)
    # return {'message': 'Transaction not found for crID ' + str(crID)}, 404  
    return jsonify({"Message": "No transactions found."}), 404   


@app.route("/rentaltransactions/co/<string:coID>")
def find_by_coID(coID):
    transaction = RentalTransaction.query.filter_by(coID=coID).first()
    if transaction:
        return transaction.json()
    return {'message': 'Transaction not found for coID ' + str(coID)}, 404     

@app.route("/rentaltransactions/date/<string:rentalDate>")
def find_by_rentalDate(rentalDate):
    transaction = {"RentalTransaction": [rentalDate.json() for rentalDate in RentalTransaction.query.filter_by(rentalDate=rentalDate).all()]}
    if transaction != {"RentalTransaction": []}:
        return jsonify(transaction)
    return jsonify({"message": "No transactions found."}), 404   

@app.route("/rentaltransactions/return/<string:transactionID>")
def return_car(transactionID):
    transaction = RentalTransaction.query.filter_by(transactionID=transactionID).first()
    if transaction != None:
        status = 201 
        result={}
        try:
            setattr(transaction, 'rentalStatus', "completed")
            db.session.commit()
        except Exception as e:
            status = 500
            result={"status": status, "message": "An error occurred when updating Rental Transaction in DB.", "error": str(e)}
        if status == 201:
            result= transaction.json()

        return jsonify(result),status

    return {'message': 'Transaction not found for transactionID ' + str(transactionID)}, 404        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7300, debug=True)
    # app.run(port=6300, debug=True)

