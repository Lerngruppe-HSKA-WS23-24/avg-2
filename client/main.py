from shared.RabbitMQConnector import *

# Hier muss vom Nutzer die Adresse abgefragt werden
userinput =


rabbit = RabbitMQConnector("localhost")

while True:

    daten = "Deutschland:Karlsruhe:Bahnhofsstrasse 4a:0:0"
    message = rabbit.send_message("waitinglist", daten)
    response = rabbit.wait_for_message("waitinglist")
