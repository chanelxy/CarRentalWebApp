import os
import json
import pika
import sys
import time

hostname = "rabbitmq" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = hostname, port = port))
        print("connected")
        break
    except:
        print("error")
        time.sleep(60)

    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="notification"
channel.exchange_declare(exchange=exchangename, exchange_type='topic')

def receiveNotification():
      # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="notification", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*notification') # bind the queue to the exchange via the key
        # any routing_key with two words and ending with '.order' will be matched

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print(body, "received in notification")
    sendToEmail(body)
    sendToTele(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print()
    print()

def sendToEmail(body):
    """inform email wrapper to send email"""
    print("Sending to Email..")
    channel.exchange_declare(exchange=exchangename, exchange_type="topic")

    channel.queue_declare(queue="email", durable=True)
    channel.queue_bind(exchange=exchangename, queue='email', routing_key='*.email')

    channel.basic_publish(exchange="notification", routing_key="notification.email", body=body,
    properties=pika.BasicProperties(delivery_mode = 2)
    )
    print ("Email Sent")

def sendToTele(body):
    """inform email wrapper to send email"""
    print("Sending to Telegram..")
    channel.exchange_declare(exchange=exchangename, exchange_type="topic")

    channel.queue_declare(queue="telegram", durable=True)
    channel.queue_bind(exchange=exchangename, queue='telegram', routing_key='*.telegram')

    channel.basic_publish(exchange=exchangename, routing_key="notification.telegram", body=body,
    properties=pika.BasicProperties(delivery_mode = 2)
    )
    print ("Telegram Message Sent")
    
if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    print("Listening for notifications")
    receiveNotification()
    # app.run(port=7600, debug=True)