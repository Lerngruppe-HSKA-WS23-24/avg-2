import pika

class RabbitMQConnector:
    """
    Ein Connector zur Vereinfachung der Kommunikation mit RabbitMQ. Erlaubt das Erstellen von Warteschlangen,
    das Senden von Nachrichten und das Warten auf Nachrichten aus einer Warteschlange.
    """

    def __init__(self, address):
        """
        Initialisiert eine Verbindung und einen Kanal zur gegebenen RabbitMQ-Adresse.

        :param address: Die Adresse des RabbitMQ-Servers.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(address))
        self.channel = self.connection.channel()
        self.queues = []

    def create_queue(self, queue_name):
        """
        Erstellt eine neue Warteschlange mit dem gegebenen Namen, sofern sie nicht bereits existiert.

        :param queue_name: Der Name der zu erstellenden Warteschlange.
        """
        self.channel.queue_declare(queue=queue_name)
        self.queues.append(queue_name)

    def queue_exists(self, queue_name):
        """
        Überprüft, ob eine Warteschlange mit dem gegebenen Namen bereits existiert.

        :param queue_name: Der Name der zu überprüfenden Warteschlange.
        :return: True, wenn die Warteschlange existiert, sonst False.
        """
        return self.queues.__contains__(queue_name)

    def send_message(self, queue_name, message):
        """
        Sendet eine Nachricht an die angegebene Warteschlange. Erstellt die Warteschlange, falls sie nicht existiert.

        :param queue_name: Der Name der Zielwarteschlange.
        :param message: Die zu sendende Nachricht.
        """
        if not self.queue_exists(queue_name):
            self.create_queue(queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)

    def wait_for_message(self, queue_name, auto_ack=False):
        """
        Wartet auf eine Nachricht aus der angegebenen Warteschlange und gibt sie zurück, wenn sie verfügbar ist.

        :param queue_name: Der Name der Warteschlange.
        :param auto_ack: Gibt an, ob die Nachricht automatisch bestätigt werden soll.
        :return: Die empfangene Nachricht und die Methode-Frame-Information oder (None, None) falls keine Nachricht verfügbar ist.
        """
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name, auto_ack=auto_ack)
        if method_frame:
            message = body.decode('utf-8')
            return message, method_frame
        else:
            return None, None

    def acknowledge_message(self, delivery_tag):
        """
        Bestätigt die Verarbeitung einer Nachricht mit einem Ack.

        :param delivery_tag: Die Lieferkennung (delivery tag) der Nachricht, die bestätigt werden soll.
        """
        self.channel.basic_ack(delivery_tag=delivery_tag)
