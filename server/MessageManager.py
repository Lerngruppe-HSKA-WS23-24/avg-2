from shared.RabbitMQConnector import *
from server.WeatherAPIConnector import *


def expand_file(connection, line):
    path = "./logs/" + str(connection) + ".txt"
    try:
        with open(path, 'a') as datei:
            datei.write(line + '\n')
        print(f'Die Zeile "{line}" wurde erfolgreich zur Datei "{path}" hinzugefügt.')
    except Exception as e:
        print(f'Fehler beim Hinzufügen der Zeile zur Datei "{path}": {str(e)}')


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
            value = self.weather.call_api()
            print("Anfrage für " + message + " von " + queue + " mit Wert " + str(value))
            expand_file(queue, message + " --> " + str(value))

