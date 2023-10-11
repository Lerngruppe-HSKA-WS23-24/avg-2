from client.MessageManager import *


# Einlesen der Daten vom Nutzer
user_input = input("Land: ") + ";"

user_input += input("Stadt: ") + ";"
user_input += input("Straße: ") + ";"
user_input += input("Hausnummer: ")

print(user_input)

m = MessageManager()
m.sync_with_server()
m.send_request(user_input)
m.rabbit.connection.close()
