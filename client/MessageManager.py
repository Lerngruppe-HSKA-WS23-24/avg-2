from shared.RabbitMQConnector import *

import uuid
import json


class MessageManager:
    def __init__(self):
        self.rabbit = RabbitMQConnector("localhost")
        self.waiting = False
        self.queue_name = None
    
    def sync_with_server(self):
        if self.queue_name is None:
            self.queue_name = str(uuid.uuid4())
        self.rabbit.create_queue(self.queue_name)
        self.rabbit.send_message("waitinglist", self.queue_name)
        print("Synced with server with id " + self.queue_name)

    def send_request(self, message):
        print("Send message: " + message)
        self.rabbit.send_message(self.queue_name, "client:" + message)

    def await_response(self):
        message, method_frame = self.rabbit.wait_for_message(self.queue_name, auto_ack=False)
        if message and method_frame:
            sender_message = message.split(":")
            if sender_message[0] == "server":
                self.rabbit.acknowledge_message(method_frame.delivery_tag)
                data = json.loads(sender_message[1])
                try:
                    return data.result.watts
                except Exception as e:
                    print("Fehler: " + str(e))
