import requests
import datetime
import time


class WeatherAPIConnector:
    def __init__(self):
        self.base_url = "https://api.forecast.solar/"
        self.blocked_until = datetime.datetime.now()

    def call_api(self, lat, lon, kwp, dec=0, az=0):
        return "{'result': {'watts': {'2023-10-12 07:41:40': 0, '2023-10-12 08:00:00': 118, '2023-10-12 09:00:00': 202, '2023-10-12 10:00:00': 246, '2023-10-12 11:00:00': 311, '2023-10-12 12:00:00': 286, '2023-10-12 13:00:00': 273, '2023-10-12 14:00:00': 268, '2023-10-12 15:00:00': 245, '2023-10-12 16:00:00': 204, '2023-10-12 17:00:00': 161, '2023-10-12 18:00:00': 93, '2023-10-12 18:42:59': 0, '2023-10-13 07:43:12': 0, '2023-10-13 08:00:00': 256, '2023-10-13 09:00:00': 443, '2023-10-13 10:00:00': 599, '2023-10-13 11:00:00': 805, '2023-10-13 12:00:00': 1154, '2023-10-13 13:00:00': 1296, '2023-10-13 14:00:00': 1184, '2023-10-13 15:00:00': 977, '2023-10-13 16:00:00': 605, '2023-10-13 17:00:00': 386, '2023-10-13 18:00:00': 184, '2023-10-13 18:40:57': 0}, 'watt_hours_period': {'2023-10-12 07:41:40': 0, '2023-10-12 08:00:00': 18, '2023-10-12 09:00:00': 160, '2023-10-12 10:00:00': 224, '2023-10-12 11:00:00': 279, '2023-10-12 12:00:00': 299, '2023-10-12 13:00:00': 280, '2023-10-12 14:00:00': 271, '2023-10-12 15:00:00': 257, '2023-10-12 16:00:00': 225, '2023-10-12 17:00:00': 183, '2023-10-12 18:00:00': 127, '2023-10-12 18:42:59': 33, '2023-10-13 07:43:12': 0, '2023-10-13 08:00:00': 36, '2023-10-13 09:00:00': 350, '2023-10-13 10:00:00': 521, '2023-10-13 11:00:00': 702, '2023-10-13 12:00:00': 980, '2023-10-13 13:00:00': 1225, '2023-10-13 14:00:00': 1240, '2023-10-13 15:00:00': 1081, '2023-10-13 16:00:00': 791, '2023-10-13 17:00:00': 496, '2023-10-13 18:00:00': 285, '2023-10-13 18:40:57': 63}, 'watt_hours': {'2023-10-12 07:41:40': 0, '2023-10-12 08:00:00': 18, '2023-10-12 09:00:00': 178, '2023-10-12 10:00:00': 402, '2023-10-12 11:00:00': 681, '2023-10-12 12:00:00': 980, '2023-10-12 13:00:00': 1260, '2023-10-12 14:00:00': 1531, '2023-10-12 15:00:00': 1788, '2023-10-12 16:00:00': 2013, '2023-10-12 17:00:00': 2196, '2023-10-12 18:00:00': 2323, '2023-10-12 18:42:59': 2356, '2023-10-13 07:43:12': 0, '2023-10-13 08:00:00': 36, '2023-10-13 09:00:00': 386, '2023-10-13 10:00:00': 907, '2023-10-13 11:00:00': 1609, '2023-10-13 12:00:00': 2589, '2023-10-13 13:00:00': 3814, '2023-10-13 14:00:00': 5054, '2023-10-13 15:00:00': 6135, '2023-10-13 16:00:00': 6926, '2023-10-13 17:00:00': 7422, '2023-10-13 18:00:00': 7707, '2023-10-13 18:40:57': 7770}, 'watt_hours_day': {'2023-10-12': 2356, '2023-10-13': 7770}}, 'message': {'code': 0, 'type': 'success', 'text': '', 'pid': 'HIi0yjDF', 'info': {'latitude': 49.2419, 'longitude': 8.5544, 'distance': 0, 'place': 'Moltkestraße 20, 68753 Waghäusel, Germany', 'timezone': 'Europe/Berlin', 'time': '2023-10-12T12:31:24+02:00', 'time_utc': '2023-10-12T10:31:24+00:00'}, 'ratelimit': {'period': 3600, 'limit': 12, 'remaining': 0}}}"
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