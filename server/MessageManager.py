from shared.RabbitMQConnector import *
from server.WeatherAPIConnector import *


class MessageManager:
    def __init__(self):
        print("Server.init: Start")
        self.rabbit = RabbitMQConnector("localhost")
        self.weather = WeatherAPIConnector()
        print("Server.init: Done")

    def await_new_messages(self):
        self.proceed_message_waitinglist()

        for qi in range(len(self.rabbit.queues)):
            self.proceed_client_requests(self.rabbit.queues[qi])

    def proceed_message_waitinglist(self):
        message = self.rabbit.wait_for_message("waitinglist")
        if message:
            self.rabbit.create_queue(message)
            print("Connection established with " + message)

    def proceed_client_requests(self, queue):
        message = self.rabbit.wait_for_message(queue, auto_ack=True)
        if message:
            # Anfrage verarbeiten mit Call an WeatherAPI und senden an Channel
            print("Anfrage für " + message + " von " + queue)
