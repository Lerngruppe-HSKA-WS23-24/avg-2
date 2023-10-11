import datetime
import time


class WeatherAPIConnector:
    def __init__(self):
        pass
    def call_api(self):
        apiCall = False
        if apiCall == False:
            next_call = (datetime.datetime.fromisoformat(zeit_aus_api) - datetime.datetime.now()).total_seconds() + 10
            time.sleep(next_call)
            return self.call_api()
        else:
            return apiCall
