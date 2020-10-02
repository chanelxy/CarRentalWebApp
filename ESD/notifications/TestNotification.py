import json
import sys
import os
import random
import datetime

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.

def send_order():
    """inform Shipping/Monitoring/Error as needed"""
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

    json_dict = {'receiverEmail': 'fionaaoye@gmail.com', 'receiverTelegramId':'porcupie', 'emailSubject':"TESTING NOTIFICATION LMAO", 'content':"Hello! Your payment has been successfully processed."}
    channel.basic_publish(exchange="notification", routing_key="notification", body=json.dumps(json_dict))

    print("Sent")
    connection.close()

send_order()