from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pika
import requests
import paypalrestsdk

app = Flask(__name__)
CORS(app)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "",
  "client_secret": "" })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():
    '''
    takes in item description and price of the rental transaction
    '''
    data = request.get_json()
    itemDescription = data['itemDescription']
    price = data['price']
    # TODO retrieve payment details
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:7400/payment/execute",
            "cancel_url": "http://localhost:7400"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": itemDescription,
                    "sku": "12345",
                    "price": price,
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": price,
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    '''
    crID
    '''

    data = request.get_json()
    crID = data['crID']

    success = False

    payment = paypalrestsdk.Payment.find(data['paymentID'])

    if payment.execute({'payer_id' : data['payerID']}):
        print('Execute success!')
        success = True
        send_notification(crID)

    else:
        print(payment.error)

    return jsonify({'success' : success})

def send_notification(crID):
    """takes in crID"""
    # retrieve customer email and telegram id from carrenter
    carRenterResponse = requests.get('http://localhost:7200/carrenter/' + str(crID))
    carRenter = json.loads(carRenterResponse)
    email = carRenter['email']
    telegram_id = carRenter['telegramID']

    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    channel.exchange_declare(exchange="notification", exchange_type="topic")

    channel.queue_declare(queue="notification", durable=True)
    channel.queue_bind(exchange="notification", queue='notification', routing_key='notification') # make sure the queue is bound to the exchange

    json_dict = {'receiverEmail': email, 'receiverTelegramId': telegram_id, 'emailSubject':"TESTING NOTIFICATION LMAO", 'content':"Hello! Your payment has been successfully processed."}
    channel.basic_publish(exchange="notification", routing_key="notification", body=json.dumps(json_dict))

    print("Sent")
    connection.close()


if __name__ == '__main__':
    app.run(debug=True, port = 7400)