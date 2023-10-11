import pika


class RabbitMQConnector:
    def __init__(self, address):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(address))
        self.channel = self.connection.channel()
        self.queues = []

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)
        self.queues.append(queue_name)

    def queue_exists(self, queue_name):
        return self.queues.__contains__(queue_name)
