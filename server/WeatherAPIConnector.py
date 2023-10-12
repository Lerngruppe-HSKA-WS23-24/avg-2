import requests
import datetime
import time


class WeatherAPIConnector:
    def __init__(self):
        self.base_url = "https://api.forecast.solar/"
        self.blocked_until = datetime.datetime.now()

    def call_api(self, lat, lon, kwp, dec=0, az=0):
        api_url = self.base_url + f"estimate/{lat}/{lon}/{dec}/{az}/{kwp}"

        if self.blocked_until <= datetime.datetime.now():
            response = requests.get(api_url)

            if response.status_code == 200:
                return response.json()

            # Wenn die Anfrage fehlschlägt, warten Sie, bevor Sie erneut versuchen.
            else:
                print(f"Received HTTP status code {response.status_code}: {response.text}")

                #Wartezeit bis zum nächsten Versuch speichern
                zeit_aus_api = response.json().get('message', {}).get('ratelimit', {}).get('retry-at', None)
                zeit_aus_api = zeit_aus_api.split('+')[0]
                print(f"zeit_aus_api: {zeit_aus_api}")

                #Es muss String zurückkommen, sonst Fehler. Abfrageblockade auf retry-at Zeit einsetzten.
                if zeit_aus_api and isinstance(zeit_aus_api, str):
                    self.blocked_until = datetime.datetime.fromisoformat(zeit_aus_api)
                    print(self.blocked_until)
                    return None
                else:
                    raise ValueError("Unexpected value for 'retry-at' in API response.")