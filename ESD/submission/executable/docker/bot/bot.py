import os
import json
import pika
import requests
import datetime
import telegram
import time

hostname = "rabbitmq" # default hostname
port = 5672 # default port
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = hostname, port = port))
        print("connected")
        break
    except:
        print("error")
        time.sleep(60)
# connect to the broker and set up a communication channel in the connection
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="notification"
channel.exchange_declare(exchange=exchangename, exchange_type='topic')

def receiveTele():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="telegram", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.telegram') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print(body, "received in telegram")
    # print(body)
    # exit()
    message = json.loads(body)
    print(message['content'], message['receiverTelegramId'])
    result = send_msg(message['content'], message['receiverTelegramId'],)
    if (result): 
         channel.basic_ack(delivery_tag=method.delivery_tag)
    

def send_msg(msg,username):
    update_userlist()
    r=open("userlog.txt",'r')
    for lists in r:
        if username in lists:
            sent = lists.split(',')
            userid = sent[1]
    carma_bot = create_bot()
    try:
        result = carma_bot.sendMessage(chat_id = userid, text = msg)
    except: # if chat_id does not exist in userlog
        return False

    if (result):
        print("Message Sent")
        return True
    else:
        return False
    
def update_userlist():
    updateid = 0
    file = open("userlog.txt", "a+")
    carma_bot = create_bot()
    updates = carma_bot.get_updates()
    for update in updates:
        updateid = update.update_id
        message = update.message
        user = message.from_user
        telegramid = user.id
        username = user.username
        line_exist = False
        with open("userlog.txt", "r") as file:
            for line in file:
                if str(telegramid) in line and username in line:
                    line_exist = True
        with open("userlog.txt", "a+") as file:
            if not line_exist:
                file.write(username + "," + str(telegramid) + "\n")

    #confirm all updates by calling get_updates with offset last updateid+1
    carma_bot.get_updates(offset=updateid+1)


def create_bot():
    bot = telegram.Bot(token = '')
    return bot

                
if __name__ == '__main__':
    # try:
    # except KeyboardInterrupt:
    print("Listening for telegram")
    receiveTele()
    