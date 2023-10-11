from shared.RabbitMQConnector import *
from server.WeatherAPIConnector import *


class MessageManager:
    def __init__(self):
        print("Server.init: Start")
        self.rabbit = RabbitMQConnector("localhost")
        self.weather = WeatherAPIConnector()
        self.rabbit.wait_for_message("waitinglist", self.callback_message_waitinglist)
        self.waiting = True
        print("Server.init: Done")

    def callback_message_waitinglist(self, method, properties, body):
        self.rabbit.create_queue(body)
        self.waiting = False
        print("Connection established with " + body)
        self.rabbit.wait_for_message("waitinglist", self.callback_message_waitinglist)
        self.waiting = True

    def callback_message_requests(self, method, properties, body):
        indexQueues = 0
        while indexQueues < self.rabbit.queues:
            
