import os
import json
import pika
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="notification"
channel.exchange_declare(exchange=exchangename, exchange_type='topic')


def receiveEmail():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="email", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.email') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print(body, "received in email")
    # print(body)
    # exit()
    message = json.loads(body)
    print(message['receiverEmail'], message['emailSubject'], message['content'])
    result = email(message['receiverEmail'], message['emailSubject'], message['content'])
    if (result): #ack if email sent successfully
        channel.basic_ack(delivery_tag=method.delivery_tag)

def email(receiverEmail, emailSubject, messageContent):
    message = Mail(
        from_email='carmaesdg2t6@gmail.com',    #SenderEmail on sendgrid
        to_emails=receiverEmail,  #TODO replace with parameter
        subject=emailSubject,
        html_content=messageContent)
    try:
        # hard coded API key for SendGrid
        sg = SendGridAPIClient("")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        if (response.status_code == 202):
            print("sent")
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

    
if __name__ == '__main__': #this allows us to run flask app without explicitly using python -m flask run. Can just run python filename.py in terminal
    print("Listening for emails")
    receiveEmail()
    # app.run(port=7600, debug=True)
