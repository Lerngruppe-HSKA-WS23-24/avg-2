import pika


def message_callback(method, properties, body):
    print(body)
    return body


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

    def send_message(self, queue_name, message):
        if not self.queue_exists(queue_name):
            self.create_queue(queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)

    def wait_for_message(self, queue_name):
        return self.channel.basic_consume(queue=queue_name, on_message_callback=message_callback, auto_ack=True)
