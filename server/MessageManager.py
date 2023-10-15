from shared.RabbitMQConnector import *
from server.WeatherAPIConnector import *
from server.GeocodingConnector import *

def expand_file(connection, line):
    """
    Fügt eine Zeile zu einer Datei hinzu, die auf der Grundlage der übergebenen Verbindung benannt ist.

    :param connection: Die Verbindungsinformationen, die zur Namensgebung der Datei verwendet werden.
    :param line: Die Zeile, die der Datei hinzugefügt werden soll.
    """
    path = "./logs/" + str(connection) + ".txt"
    try:
        with open(path, 'a') as datei:
            datei.write(line + '\n')
        print(f'Die Log-Datei "{path}" wurde bearbeitet.')
    except Exception as e:
        print(f'Fehler beim Hinzufügen der Zeile zur Datei "{path}": {str(e)}')

class MessageManager:
    """
    Ein Manager zum Behandeln von Nachrichten zwischen Clients und Servern mit RabbitMQ, WetterAPI und Geocoding.
    """

    def __init__(self):
        """
        Initialisiert die RabbitMQ, WeatherAPI und Geocoding Verbindungen.
        """
        print("Server.init: Start")
        self.rabbit = RabbitMQConnector("localhost")
        self.rabbit.create_queue("waitinglist")
        self.weather = WeatherAPIConnector()
        self.geo = GeocodingConnector()
        print("Server.init: Done")

    def await_new_messages(self):
        """
        Überwacht kontinuierlich eingehende Nachrichten und verarbeitet sie entsprechend.
        """
        self.proceed_message_waitinglist()

        for qi in range(len(self.rabbit.queues)):
            self.proceed_client_requests(self.rabbit.queues[qi])

    def proceed_message_waitinglist(self):
        """
        Überprüft die Warteschlange auf neue Nachrichten und erstellt gegebenenfalls eine neue Warteschlange.
        """
        message, message_frame = self.rabbit.wait_for_message("waitinglist")
        if message:
            self.rabbit.create_queue(message)
            print("Connection established with " + message)

    def proceed_client_requests(self, queue):
        """
        Bearbeitet eingehende Client-Anfragen, holt die notwendigen Daten über die APIs und sendet Antworten zurück.

        :param queue: Der Name der Warteschlange, aus der die Nachrichten abgerufen werden sollen.
        """
        message, method_frame = self.rabbit.wait_for_message(queue, auto_ack=False)
        if message:
            # Anfrage verarbeiten mit Call an WeatherAPI und senden an Channel
            sender_message = message.split("$")
            if sender_message[0] == "client":
                self.rabbit.acknowledge_message(method_frame.delivery_tag)
                message_contents = sender_message[1].split(";")
                if isinstance(message_contents, list) and len(message_contents) >= 4:
                    geo_data = self.geo.get_coordinates_from_address(message_contents[0], message_contents[1], message_contents[2], message_contents[3])
                    solar_data = self.weather.call_api(geo_data[0], geo_data[1], message_contents[4])
                    expand_file(queue, message + " --> " + str(solar_data))
                    self.rabbit.send_message(queue, "server$" + str(solar_data))
