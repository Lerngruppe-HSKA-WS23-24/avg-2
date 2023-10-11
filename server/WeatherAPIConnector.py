import requests
import datetime
import time

class WeatherAPIConnector:
    def __init__(self):
        self.api_url = "https://api.forecast.solar/"
        self.blocked_until = datetime.datetime.now()

    def call_api(self):
        if self.blocked_until <= datetime.datetime.now():
            response = requests.get(self.api_url)

            # Wenn der Statuscode 200 (OK) ist, geben Sie die Antwort zurück.
            if response.status_code == 200:
                return response.json()

            # Wenn die Anfrage fehlschlägt, warten Sie, bevor Sie erneut versuchen.
            else:

                print(f"Received HTTP status code {response.status_code}: {response.text}")

                # Pfad zum "retry-at" Feld in der JSON-Antwort aktualisiert
                zeit_aus_api = response.json().get('message', {}).get('ratelimit', {}).get('retry-at', None)
                zeit_aus_api = zeit_aus_api.split('+')[0]

                print(f"zeit_aus_api: {zeit_aus_api}")  # Druckt den Wert von zeit_aus_api



                if zeit_aus_api and isinstance(zeit_aus_api, str):
                    self.blocked_until = datetime.datetime.fromisoformat(zeit_aus_api)
                    print(self.blocked_until)
                    return None
                else:
                    # Hier können Sie zusätzliche Fehlerbehandlungen oder Protokolle hinzufügen,
                    # falls "retry-at" nicht gefunden wird oder nicht im erwarteten Format ist.
                    raise ValueError("Unexpected value for 'retry-at' in API response.")

# Beispielaufruf
if __name__ == "__main__":
    connector = WeatherAPIConnector()
    data = connector.call_api()
    print(data)
