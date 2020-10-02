from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/reviews'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Reviews(db.Model):
    __tablename__ = 'reviews'
 
    RID = db.Column(db.Integer(), primary_key=True)
    crUsername = db.Column(db.String(128), nullable=False)
    cID = db.Column(db.Integer(), nullable=False)
    reviewContents = db.Column(db.String(1000), nullable=False)

 
    def json(self):
        return {
            "RID": self.RID, 
            "crUsername": self.crUsername, 
            "cID": self.cID, 
            "reviewContents": self.reviewContents
        }

@app.route("/reviews")
def get_all():
    return jsonify({"Reviews": [RID.json() for RID in Reviews.query.all()]})

@app.route("/reviews", methods=["POST"])
def create_review():
    data = request.get_json()
    RID = data['RID']

    if (Reviews.query.filter_by(RID=RID).first()):
        return jsonify({"message": "A review with RID '{}' already exists.".format(RID)}), 400

    reviews = Reviews(**data)

    try:
        db.session.add(reviews)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when creating the review."}), 500

    return jsonify(reviews.json()), 201


@app.route("/reviews/<string:cID>")
def find_by_cID(cID):
    reviews = {"Reviews": [RID.json() for RID in Reviews.query.filter_by(cID=cID).all()]}
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7500, debug=True)