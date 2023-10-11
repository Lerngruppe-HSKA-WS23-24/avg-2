from shared.RabbitMQConnector import *

rabbit = RabbitMQConnector("localhost")
while True:
    # Hier muss vom Nutzer die Adresse abgefragt werden
    daten = "Deutschland:Karlsruhe:Bahnhofsstrasse 4a:0:0"
    message = rabbit.send_message("waitinglist", daten)
    response = rabbit.wait_for_message("waitinglist")
