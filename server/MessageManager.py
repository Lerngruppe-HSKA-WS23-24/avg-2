from shared.RabbitMQConnector import *
import uuid


class MessageManager:
    def __init__(self):
        self.rabbit = RabbitMQConnector("localhost")
        self.register_queue = str(uuid.uuid4())

        self.rabbit.create_queue(self.register_queue)
