from client.MessageManager import *

m = MessageManager()
m.sync_with_server()


def check_input(s):
    return bool(s) and all(char.isalpha() or char.isspace() for char in s)


while True:
    # Einlesen der Daten vom Nutzer
    while True:
        while True:
            user_input = input("Land: ")
            if check_input(user_input):
                daten = user_input + ";"
                break
            else:
                print("Die Eingabe darf nur Buchstaben und Leerzeichen enthalten.")

        while True:
            user_input = input("Stadt: ")
            if check_input(user_input):
                daten += user_input + ";"
                break
            else:
                print("Die Eingabe darf nur Buchstaben und Leerzeichen enthalten.")

        while True:
            user_input = input("Straße: ")
            if check_input(user_input):
                daten += user_input + ";"
                break
            else:
                print("Die Eingabe darf nur Buchstaben und Leerzeichen enthalten.")

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

    # Eingaben in daten gespeichert
    m.send_request(daten)
    data = m.await_response()
    for key in data.keys():
        print(key)
        for hourKey in data[key]:
            print(hourKey + ": " + str(data[key][hourKey]))

m.rabbit.connection.close()
