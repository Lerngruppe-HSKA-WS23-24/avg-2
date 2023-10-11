from shared.RabbitMQConnector import *

import uuid


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