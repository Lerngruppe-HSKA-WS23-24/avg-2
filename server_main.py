from WeatherAPIConnector import *
from shared.RabbitMQConnector import *

weather = WeatherAPIConnector()
rabbit = RabbitMQConnector("localhost")
while True:
    rabbit.create_queue("waitinglist")
    message = rabbit.wait_for_message("waitinglist")
