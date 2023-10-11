from client.MessageManager import *

# Einlesen der Daten vom Nutzer
while True:

    while True:
        user_input = input("Land: ")
        if user_input.isalpha():
            daten = user_input + ";"
            break
        else:
            print("Die Eingabe darf nur Buchstaben enthalten.")

    while True:
        user_input = input("Stadt: ")
        if user_input.isalpha():
            daten += user_input + ";"
            break
        else:
            print("Die Eingabe darf nur Buchstaben enthalten.")

    while True:
        user_input = input("Straße: ")
        if user_input.isalpha():
            daten += user_input + ";"
            break
        else:
            print("Die Eingabe darf nur Buchstaben enthalten.")

    while True:
        user_input = input("Hausnummer: ")
        if user_input.isdigit():
            daten += user_input + ";"
            break
        else:
            print("Die Eingabe darf nur Zahlen enthalten.")
    while True:
        user_input = input("kWh: ")
        if user_input.isdigit():
            daten += user_input
            break
        else:
            print("Die Eingabe darf nur Zahlen enthalten.")

    print(daten)

    user_input = input("Stimmen die Eingaben so? (J/N)")

    if user_input == "J":
        break
    if user_input == "N":
        print("Versuchen sie es nochmal :)")


# Eingaben in 'daten' gespeichert print(daten)

m = MessageManager()
m.sync_with_server()
m.send_request(daten)
m.rabbit.connection.close()
